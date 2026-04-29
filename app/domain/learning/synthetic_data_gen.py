"""
app/domain/learning/synthetic_data_gen.py

Gerçekçi eğitim verileri üreteç.
Ajanları eğitmek için 1000+ senaryo hazırlıyor.
"""

import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class ScenarioType(str, Enum):
    """Senaryo kategorileri"""
    STARTUP_LAUNCH = "startup_launch"
    MARKET_EXPANSION = "market_expansion"
    PRODUCT_DEVELOPMENT = "product_development"
    COST_REDUCTION = "cost_reduction"
    M_AND_A = "mergers_acquisitions"


@dataclass
class SyntheticScenario:
    """Oluşturulan senaryonun veri modeli"""
    scenario_id: int
    name: str
    scenario_type: ScenarioType

    budget_million_usd: float
    expected_roi_percent: float
    risk_level: int
    team_readiness: int

    # Ground truth (expert consensus)
    expert_decision: str  # "APPROVE", "REVISE", "REJECT"
    expert_confidence: float  # 0.0-1.0

    # Simulated real-world outcome (after 12 months)
    actual_roi_percent: float
    completion_months: int
    team_burnout_rate: float
    market_success: bool

    # Metadata
    created_at: datetime
    industry: str  # "Tech", "Finance", "Manufacturing", etc.
    seasonality_factor: float  # Q1=0.8, Q2=1.0, Q3=1.1, Q4=0.9


class SyntheticDataGenerator:
    """
    1000+ realistic scenario üretici

    Stratejisi:
    1. Base distributions oluştur (Lognormal, Normal, etc.)
    2. Realistic correlations inject et
    3. Industry patterns ekle
    4. Ground truth labels oluştur
    5. Simulated outcomes attach et
    """

    def __init__(self, random_seed: int = 42):
        np.random.seed(random_seed)
        self.scenario_counter = 0

    def generate_dataset(
        self,
        n_scenarios: int = 1000,
        distribution: str = "realistic"  # "uniform", "realistic", "edge_cases"
    ) -> List[SyntheticScenario]:
        """
        Main method: n_scenarios adet senaryo üret

        distribution:
          - "uniform": Random values (testing için)
          - "realistic": Real-world patterns (training için)
          - "edge_cases": Extreme values (robustness testing için)
        """

        scenarios = []
        industries = ["Tech", "Finance", "Manufacturing", "Healthcare", "Retail"]

        for i in range(n_scenarios):
            industry = np.random.choice(industries)
            scenario_type = np.random.choice(list(ScenarioType))

            # Step 1: Generate base features
            if distribution == "uniform":
                budget = np.random.uniform(0.1, 50)
                roi = np.random.uniform(-30, 100)
                risk = np.random.randint(1, 11)
                team = np.random.randint(1, 11)

            elif distribution == "realistic":
                # Lognormal: Most projects are small, few are huge
                budget = np.random.lognormal(mean=1.5, sigma=1.2)
                budget = np.clip(budget, 0.1, 100)

                # Normal: ROI centered around 25%
                roi = np.random.normal(loc=25, scale=20)
                roi = np.clip(roi, -50, 150)

                # Risk & Team more uniform
                risk = np.random.randint(1, 11)
                team = np.random.randint(1, 11)

            # Step 2: Inject realistic correlations
            budget, roi, risk, team = self._inject_correlations(
                budget, roi, risk, team, industry, scenario_type
            )

            # Step 3: Generate ground truth decision
            expert_decision, expert_confidence = self._expert_consensus(
                budget, roi, risk, team, industry
            )

            # Step 4: Simulate real-world outcome
            actual_roi, completion_months, burnout, success = self._simulate_outcome(
                budget, roi, risk, team, expert_decision
            )

            # Step 5: Seasonality factor
            quarter = (i % 4)  # Q1, Q2, Q3, Q4
            seasonality = [0.8, 1.0, 1.1, 0.9][quarter]

            scenario = SyntheticScenario(
                scenario_id=self.scenario_counter,
                name=f"{industry}_{scenario_type}_{i}",
                scenario_type=scenario_type,
                budget_million_usd=budget,
                expected_roi_percent=roi,
                risk_level=risk,
                team_readiness=team,
                expert_decision=expert_decision,
                expert_confidence=expert_confidence,
                actual_roi_percent=actual_roi,
                completion_months=completion_months,
                team_burnout_rate=burnout,
                market_success=success,
                created_at=datetime.now() + timedelta(days=i),
                industry=industry,
                seasonality_factor=seasonality
            )

            scenarios.append(scenario)
            self.scenario_counter += 1

        return scenarios

    def _inject_correlations(
        self,
        budget: float,
        roi: float,
        risk: int,
        team: int,
        industry: str,
        scenario_type: ScenarioType
    ) -> tuple:
        """
        Gerçekçi korelasyonlar enjekte et:
        - Büyük bütçe → daha yüksek risk (execution risk)
        - Düşük team readiness → daha düşük ROI
        - Tech → daha yüksek ROI & risk
        - Manufacturing → daha düşük ROI ama stable
        """

        # Correlation 1: Big budget → higher risk
        if budget > 10:
            risk += int(np.random.normal(2, 1))  # +1 to +3 risk level

        # Correlation 2: Low team → lower ROI
        if team < 4:
            roi -= np.random.normal(15, 5)

        # Correlation 3: Very low team + high risk = disaster
        if team < 3 and risk > 7:
            roi -= 20

        # Correlation 4: Industry patterns
        if industry == "Tech":
            roi *= 1.3  # Tech projects have higher ROI
            risk += 1   # But more risky
        elif industry == "Manufacturing":
            roi *= 0.8  # Manufacturing more conservative
            risk -= 1
        elif industry == "Finance":
            roi *= 1.1
            risk += 0.5

        # Correlation 5: Scenario type
        if scenario_type == ScenarioType.STARTUP_LAUNCH:
            risk += 2
            roi += 15  # High risk, high reward
        elif scenario_type == ScenarioType.COST_REDUCTION:
            risk -= 1  # Lower risk
            roi *= 0.6  # Lower ROI (but more predictable)

        # Bounds check
        budget = np.clip(budget, 0.1, 150)
        roi = np.clip(roi, -50, 200)
        risk = int(np.clip(risk, 1, 10))
        team = int(np.clip(team, 1, 10))

        return budget, roi, risk, team

    def _expert_consensus(
        self,
        budget: float,
        roi: float,
        risk: int,
        team: int,
        industry: str
    ) -> tuple:
        """
        Expert consensus decision logic:
        - ROI-to-risk ratio important
        - Team capacity critical
        - Budget vs ROI alignment

        Returns: (decision_string, confidence_0_to_1)
        """

        # Normalize features to 0-1
        roi_norm = np.clip(roi / 100, 0, 1)
        risk_norm = risk / 10.0
        team_norm = team / 10.0
        budget_norm = np.clip(budget / 10, 0, 1)

        # Expert scoring (weighted combination)
        # Weights reflect typical business priorities
        score = (
            roi_norm * 0.40 +           # ROI is critical
            (1 - risk_norm) * 0.30 +    # Risk avoidance
            team_norm * 0.20 +          # Team capability
            budget_norm * 0.10          # Budget efficiency
        )

        # Industry adjustments
        if industry == "Tech":
            score *= 1.1  # Tech projects valued higher
        elif industry == "Manufacturing":
            score *= 0.95  # More conservative

        # Decision thresholds
        if score >= 0.75:
            decision = "APPROVE"
            # Confidence based on agreement among factors
            confidence_factors = [
                roi_norm >= 0.40,
                risk_norm <= 0.60,
                team_norm >= 0.60
            ]
            confidence = min(0.95, 0.7 + np.mean(confidence_factors) * 0.25)

        elif score >= 0.50:
            decision = "REVISE"
            confidence = 0.65  # Moderate confidence

        else:
            decision = "REJECT"
            confidence = min(0.95, 0.5 + (0.5 - score) * 0.5)

        return decision, round(confidence, 2)

    def _simulate_outcome(
        self,
        budget: float,
        roi: float,
        risk: int,
        team: int,
        decision: str
    ) -> tuple:
        """
        Simulate real-world outcome (12 months sonrası).

        Expert consensus'e karşı gerçek dünya:
        - Overestimation: %70 of projects miss ROI targets by 15%
        - Team burnout: 0.0-0.5 (0=healthy, 0.5=burned out)
        - Success: Boolean (market acceptance)
        """

        # Base: Expert karar doğruysa, outcome daha iyi
        if decision == "APPROVE":
            actual_roi = roi * np.random.normal(0.85, 0.15)  # 15% optimism bias
            burnout = np.random.uniform(0.05, 0.30)  # Generally healthier
            success_prob = 0.75

        elif decision == "REVISE":
            actual_roi = roi * np.random.normal(0.70, 0.25)  # High variance
            burnout = np.random.uniform(0.20, 0.45)
            success_prob = 0.50

        else:  # REJECT
            actual_roi = roi * np.random.normal(0.50, 0.30)  # Worse outcomes
            burnout = np.random.uniform(0.30, 0.60)
            success_prob = 0.25

        # Risk affects outcome variance
        if risk > 7:
            actual_roi *= np.random.normal(1.0, 0.3)  # High variance
        else:
            actual_roi *= np.random.normal(1.0, 0.15)  # More stable

        # Team readiness affects burnout
        if team < 4:
            burnout += 0.15  # Inexperienced teams burn out more

        completion_months = int(np.random.normal(12, 3))
        completion_months = np.clip(completion_months, 3, 36)

        market_success = np.random.rand() < success_prob

        return (
            round(actual_roi, 1),
            completion_months,
            round(burnout, 2),
            market_success
        )


def export_to_json(scenarios: List[SyntheticScenario], filename: str):
    """Export scenarios to JSON for database import"""
    import json

    data = [
        {
            "scenario_id": s.scenario_id,
            "name": s.name,
            "scenario_type": s.scenario_type,
            "budget_million_usd": s.budget_million_usd,
            "expected_roi_percent": s.expected_roi_percent,
            "risk_level": s.risk_level,
            "team_readiness": s.team_readiness,
            "expert_decision": s.expert_decision,
            "expert_confidence": s.expert_confidence,
            "actual_roi_percent": s.actual_roi_percent,
            "completion_months": s.completion_months,
            "team_burnout_rate": s.team_burnout_rate,
            "market_success": s.market_success,
            "industry": s.industry,
            "seasonality_factor": s.seasonality_factor,
        }
        for s in scenarios
    ]

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ {len(scenarios)} scenarios exported to {filename}")


# Usage Example
if __name__ == "__main__":
    gen = SyntheticDataGenerator(random_seed=42)

    # Generate 1000 realistic training scenarios
    scenarios = gen.generate_dataset(n_scenarios=1000, distribution="realistic")

    # Print sample
    sample = scenarios[0]
    print(f"\n📊 Sample Scenario:")
    print(f"  ID: {sample.scenario_id}")
    print(f"  Name: {sample.name}")
    print(f"  Budget: ${sample.budget_million_usd:.1f}M")
    print(f"  Expected ROI: {sample.expected_roi_percent:.1f}%")
    print(f"  Risk: {sample.risk_level}/10")
    print(f"  Team: {sample.team_readiness}/10")
    print(f"  Expert Decision: {sample.expert_decision} ({sample.expert_confidence*100:.0f}%)")
    print(f"  Actual ROI: {sample.actual_roi_percent:.1f}%")
    print(f"  Market Success: {sample.market_success}")

    # Export
    export_to_json(scenarios, "training_scenarios.json")
