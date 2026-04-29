"""
app/domain/learning/agent_calibrator.py

Ajanların decision weights'ini veri tabanlı olarak öğrenen sistem.
Gradient descent / Bayesian optimization ile ajan doğruluğunu artırır.
"""

import numpy as np
from typing import Dict, List, Callable, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from abc import ABC, abstractmethod


class StanceType(str, Enum):
    """Ajan kararları"""
    SUPPORT = "support"
    NEUTRAL = "neutral"
    OPPOSE = "oppose"


class DecisionType(str, Enum):
    """Final kararlar"""
    APPROVE = "APPROVE"
    REVISE = "REVISE"
    REJECT = "REJECT"


@dataclass
class AgentWeights:
    """Ajan karar ağırlıkları (learnable parameters)"""
    agent_name: str  # "CEO", "CFO", "HR"

    # Feature weights (her feature'ın nihai kararında ağırlığı)
    roi_weight: float = 0.50
    risk_weight: float = 0.30
    team_weight: float = 0.20

    # Behavioral parameters
    confidence_base: float = 0.65  # Başlangıç güven düzeyi
    confidence_scaling: float = 1.0  # Güven artırma çarpanı

    def to_dict(self) -> Dict:
        return {
            "agent_name": self.agent_name,
            "roi_weight": self.roi_weight,
            "risk_weight": self.risk_weight,
            "team_weight": self.team_weight,
            "confidence_base": self.confidence_base,
            "confidence_scaling": self.confidence_scaling,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class LossFunction(ABC):
    """Loss function interface"""

    @abstractmethod
    def compute(self, prediction: str, ground_truth: str) -> float:
        pass


class CrossEntropyLoss(LossFunction):
    """Classification loss: predicted stance vs ground truth decision"""

    def compute(self, prediction: str, ground_truth: str) -> float:
        """
        prediction: "APPROVE", "REVISE", "REJECT"
        ground_truth: "APPROVE", "REVISE", "REJECT"

        Returns: scalar loss (0 = perfect, 1 = worst)
        """

        if prediction == ground_truth:
            return 0.0
        else:
            # Partial credit: REVISE is "between" APPROVE and REJECT
            if (prediction == "REVISE" and ground_truth in ["APPROVE", "REJECT"]):
                return 0.3  # Partial credit
            elif (ground_truth == "REVISE" and prediction in ["APPROVE", "REJECT"]):
                return 0.4  # Closer to ground truth
            else:
                return 1.0  # Completely wrong


class ConfidenceCalibrationLoss(LossFunction):
    """Confidence 'sincerity' loss: predicted confidence should match accuracy"""

    def compute(self, predicted_confidence: float, was_correct: bool) -> float:
        """
        High confidence on wrong prediction = high loss
        Low confidence on correct prediction = slight loss (penalty)
        """

        target_confidence = 1.0 if was_correct else 0.0
        return (predicted_confidence - target_confidence) ** 2


class AgentCalibrator:
    """
    Ajan ağırlıklarını training data'dan öğrenme sistemi.

    Stratejisi:
    1. Initial weights load et (default)
    2. Training dataset döngüsü:
       a. Her scenario için forward pass
       b. Loss calculate et
       c. Gradient calculate et (numerical differentiation)
       d. Weights update et
    3. Validation set'te test et
    4. Best weights'i kaydet
    """

    def __init__(
        self,
        agent_name: str,
        learning_rate: float = 0.01,
        l2_regularization: float = 0.001,
        verbose: bool = True
    ):
        self.agent_name = agent_name
        self.learning_rate = learning_rate
        self.l2_reg = l2_regularization
        self.verbose = verbose

        # Initialize weights
        self.weights = self._init_weights()

        # Loss tracking
        self.train_losses = []
        self.val_losses = []

    def _init_weights(self) -> AgentWeights:
        """Initialize agent-specific weights"""

        if self.agent_name == "CEO":
            return AgentWeights(
                agent_name="CEO",
                roi_weight=0.60,
                risk_weight=0.25,
                team_weight=0.15,
                confidence_base=0.65,
            )

        elif self.agent_name == "CFO":
            return AgentWeights(
                agent_name="CFO",
                roi_weight=0.50,
                risk_weight=0.35,
                team_weight=0.15,
                confidence_base=0.60,
            )

        elif self.agent_name == "HR":
            return AgentWeights(
                agent_name="HR",
                roi_weight=0.20,
                risk_weight=0.20,
                team_weight=0.60,
                confidence_base=0.70,
            )

        else:
            raise ValueError(f"Unknown agent: {self.agent_name}")

    def train(
        self,
        training_data: List[Dict],
        validation_data: List[Dict],
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Agent weights'i training data üzerinde öğren

        training_data format:
        [
            {
                "budget_million_usd": 5.0,
                "expected_roi_percent": 45.0,
                "risk_level": 6,
                "team_readiness": 7,
                "ground_truth_decision": "APPROVE",
                "expert_confidence": 0.92
            },
            ...
        ]

        Returns: training history
        """

        best_val_loss = float('inf')
        patience = 10
        patience_counter = 0

        for epoch in range(epochs):
            # Shuffle training data
            np.random.shuffle(training_data)

            epoch_train_loss = 0
            num_batches = len(training_data) // batch_size

            # Training batches
            for batch_idx in range(num_batches):
                batch = training_data[
                    batch_idx * batch_size:(batch_idx + 1) * batch_size
                ]

                batch_loss = 0
                gradients = self._init_gradients()

                for sample in batch:
                    # Forward pass
                    prediction, confidence = self._predict(sample)

                    # Calculate loss
                    loss = self._calculate_loss(
                        sample, prediction, confidence
                    )
                    batch_loss += loss

                    # Backward pass (numerical gradient)
                    batch_gradients = self._calculate_gradients(
                        sample, prediction
                    )

                    # Accumulate gradients
                    for key in batch_gradients:
                        gradients[key] += batch_gradients[key]

                # Update weights
                self._update_weights(gradients, len(batch))
                epoch_train_loss += batch_loss / len(batch)

            # Average train loss
            avg_train_loss = epoch_train_loss / num_batches
            self.train_losses.append(avg_train_loss)

            # Validation
            val_loss = self._validate(validation_data)
            self.val_losses.append(val_loss)

            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                best_weights = self.weights
            else:
                patience_counter += 1

            if patience_counter >= patience:
                if self.verbose:
                    print(f"Early stopping at epoch {epoch}")
                self.weights = best_weights
                break

            if self.verbose and (epoch + 1) % 10 == 0:
                print(
                    f"Epoch {epoch+1}/{epochs} | "
                    f"Train Loss: {avg_train_loss:.4f} | "
                    f"Val Loss: {val_loss:.4f}"
                )

        return {
            "final_train_loss": self.train_losses[-1],
            "final_val_loss": self.val_losses[-1],
            "best_weights": self.weights.to_dict(),
            "epochs_trained": epoch + 1
        }

    def _predict(self, scenario: Dict) -> Tuple[str, float]:
        """
        Forward pass: Scenario'yu ajan özelinde analiz et

        Mevcut weights kullanarak stance ve confidence hesapla
        """

        # Normalize features
        roi_norm = np.clip(scenario["expected_roi_percent"] / 100.0, 0, 1)
        risk_norm = scenario["risk_level"] / 10.0
        team_norm = scenario["team_readiness"] / 10.0

        # Agent-specific scoring
        if self.agent_name == "CEO":
            # CEO: Growth & ROI focused
            score = (
                self.weights.roi_weight * roi_norm +
                self.weights.risk_weight * (1 - risk_norm) +
                self.weights.team_weight * team_norm
            )

        elif self.agent_name == "CFO":
            # CFO: Risk & ROI focused
            score = (
                self.weights.roi_weight * roi_norm +
                self.weights.risk_weight * (1 - risk_norm) * 1.2 +  # Risk weighted higher
                self.weights.team_weight * team_norm * 0.5
            )

        elif self.agent_name == "HR":
            # HR: Team focused
            score = (
                self.weights.roi_weight * (roi_norm * 0.5) +  # ROI less important
                self.weights.risk_weight * (1 - risk_norm) +
                self.weights.team_weight * team_norm * 1.5
            )

        # Convert score to decision
        if score >= 0.75:
            decision = "APPROVE"
        elif score >= 0.50:
            decision = "REVISE"
        else:
            decision = "REJECT"

        # Confidence scaling
        confidence = self.weights.confidence_base * self.weights.confidence_scaling
        confidence = np.clip(confidence, 0.3, 0.95)

        return decision, confidence

    def _calculate_loss(
        self,
        scenario: Dict,
        prediction: str,
        confidence: float
    ) -> float:
        """
        Total loss = classification loss + confidence calibration loss + regularization
        """

        ground_truth = scenario["ground_truth_decision"]

        # Classification loss
        clf_loss = CrossEntropyLoss().compute(prediction, ground_truth)

        # Confidence calibration loss
        was_correct = (prediction == ground_truth)
        conf_loss = ConfidenceCalibrationLoss().compute(confidence, was_correct)

        # L2 regularization
        weight_magnitude = (
            self.weights.roi_weight ** 2 +
            self.weights.risk_weight ** 2 +
            self.weights.team_weight ** 2
        )
        reg_loss = self.l2_reg * weight_magnitude

        total_loss = clf_loss + 0.3 * conf_loss + reg_loss

        return total_loss

    def _calculate_gradients(
        self,
        scenario: Dict,
        current_prediction: str
    ) -> Dict:
        """
        Numerical differentiation ile gradients hesapla

        ∇f ≈ (f(x+ε) - f(x)) / ε
        """

        epsilon = 0.01
        gradients = self._init_gradients()

        # ROI weight gradient
        self.weights.roi_weight += epsilon
        loss_plus = self._calculate_loss(
            scenario, *self._predict(scenario)
        )
        self.weights.roi_weight -= 2 * epsilon
        loss_minus = self._calculate_loss(
            scenario, *self._predict(scenario)
        )
        self.weights.roi_weight += epsilon
        gradients["roi_weight"] = (loss_plus - loss_minus) / (2 * epsilon)

        # Risk weight gradient
        self.weights.risk_weight += epsilon
        loss_plus = self._calculate_loss(
            scenario, *self._predict(scenario)
        )
        self.weights.risk_weight -= 2 * epsilon
        loss_minus = self._calculate_loss(
            scenario, *self._predict(scenario)
        )
        self.weights.risk_weight += epsilon
        gradients["risk_weight"] = (loss_plus - loss_minus) / (2 * epsilon)

        # Team weight gradient
        self.weights.team_weight += epsilon
        loss_plus = self._calculate_loss(
            scenario, *self._predict(scenario)
        )
        self.weights.team_weight -= 2 * epsilon
        loss_minus = self._calculate_loss(
            scenario, *self._predict(scenario)
        )
        self.weights.team_weight += epsilon
        gradients["team_weight"] = (loss_plus - loss_minus) / (2 * epsilon)

        return gradients

    def _update_weights(self, gradients: Dict, batch_size: int):
        """SGD ile weights update et: w = w - α * ∇L"""

        self.weights.roi_weight -= (
            self.learning_rate * gradients["roi_weight"] / batch_size
        )
        self.weights.risk_weight -= (
            self.learning_rate * gradients["risk_weight"] / batch_size
        )
        self.weights.team_weight -= (
            self.learning_rate * gradients["team_weight"] / batch_size
        )

        # Normalize weights to sum=1
        total = (
            self.weights.roi_weight +
            self.weights.risk_weight +
            self.weights.team_weight
        )
        self.weights.roi_weight /= total
        self.weights.risk_weight /= total
        self.weights.team_weight /= total

    def _validate(self, validation_data: List[Dict]) -> float:
        """Validation set üzerinde accuracy test et"""

        total_loss = 0

        for sample in validation_data:
            prediction, confidence = self._predict(sample)
            loss = self._calculate_loss(sample, prediction, confidence)
            total_loss += loss

        return total_loss / len(validation_data)

    def _init_gradients(self) -> Dict:
        """Gradient accumulator initialize"""
        return {
            "roi_weight": 0.0,
            "risk_weight": 0.0,
            "team_weight": 0.0,
        }

    def save_weights(self, filepath: str):
        """Trained weights'i dosyaya kaydet"""
        with open(filepath, 'w') as f:
            json.dump(self.weights.to_dict(), f, indent=2)

        print(f"✅ Weights saved to {filepath}")

    def load_weights(self, filepath: str):
        """Dosyadan trained weights yükle"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.weights = AgentWeights.from_dict(data)
        print(f"✅ Weights loaded from {filepath}")


# Usage Example
if __name__ == "__main__":
    import json

    # Load training data
    with open("training_scenarios.json", 'r') as f:
        all_scenarios = json.load(f)

    # Split into train/val (80/20)
    train_data = all_scenarios[:800]
    val_data = all_scenarios[800:]

    # Train CEO agent
    print("\n🤖 Training CEO Agent...")
    ceo_calibrator = AgentCalibrator(
        agent_name="CEO",
        learning_rate=0.01,
        verbose=True
    )

    history = ceo_calibrator.train(
        training_data=train_data,
        validation_data=val_data,
        epochs=100,
        batch_size=32
    )

    print("\n📊 Training Results:")
    print(json.dumps(history, indent=2))

    # Save trained weights
    ceo_calibrator.save_weights("ceo_weights.json")
