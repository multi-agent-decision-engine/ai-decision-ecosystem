# 📊 Veri Bilimi Odaklı Akıllı Ajan Eğitim Framework

## 🎯 Hedef
Ajanlar veri tabanlı öğrenmesi yoluyla:
1. **Daha akıllı hale gelecek** (accuracy ↑, bias ↓)
2. **Kendi aralarında tartışabilecek** (multi-round debate)
3. **Gerçek sonuçlardan öğrenecek** (feedback loop)

---

## BÖLÜM 1: VERİ SETİ TASARIMI

### 1.1 Synthetic Training Data Pipeline

**Amaç:** 1000+ realistic scenario üretmek

```
Phase 1: Base Distribution
├─ budget_million_usd: Lognormal(μ=1.5, σ=1.2) [0.1M - 100M]
├─ expected_roi_percent: Normal(μ=25%, σ=20%) [-50% - 100%+]
├─ risk_level: Discrete Uniform(1-10) OR Beta distribution
└─ team_readiness: Normal(μ=6, σ=2.5) [1-10]

Phase 2: Correlation Injection
├─ IF budget > 10M THEN risk_level tendency ↑
├─ IF team_readiness < 4 THEN roi_percent expected_lower
└─ IF risk_level = 1 THEN roi_percent expected_lower (safe projects)

Phase 3: Real-World Patterns
├─ Seasonal effects (Q1 = more risk-averse)
├─ Industry clusters (Tech = higher ROI, Manufacturing = lower)
└─ Historical success rate patterns
```

**Output:** 1000 scenarios with realistic correlations

---

### 1.2 Ground Truth Labels (İdeal Kararlar)

Her synthetic scenario'ya expert consensus label ekle:

```json
{
  "scenario_id": 1,
  "input": {
    "budget_million_usd": 5.0,
    "expected_roi_percent": 45.0,
    "risk_level": 6,
    "team_readiness": 7
  },
  "ground_truth": {
    "decision": "APPROVE",  // Expert consensus
    "confidence": 0.92,     // Agreement rate among experts
    "reasoning": "High ROI offsets moderate risk; team ready"
  },
  "outcome": {  // Simulated real-world outcome after 12 months
    "actual_roi": 42.0,
    "time_to_completion": 14,
    "team_burnout_rate": 0.15,
    "market_success": true
  }
}
```

---

### 1.3 Agent Historical Performance DB

```sql
CREATE TABLE agent_decisions (
  id UUID PRIMARY KEY,
  scenario_id INT,
  agent_name VARCHAR (CEO, CFO, HR),
  round_number INT,
  stance VARCHAR (support, neutral, oppose),
  confidence FLOAT,
  metrics JSONB,
  accuracy FLOAT,  -- 1.0 if matched ground_truth, 0.0 otherwise
  timestamp TIMESTAMPTZ
);
```

---

## BÖLÜM 2: AGENT TRAINING PIPELINE

### 2.1 Agent Scoring Function (Öğrenebilir Ağırlıklar)

**Mevcut:** Sabit kurallar (if-else)
```python
raw_score = growth_potential * 0.6 + market_alignment * 0.4
```

**Hedef:** Öğrenebilir ağırlıklar (weights learnable)
```python
raw_score = w1*growth_potential + w2*market_alignment + w3*budget_fit + w4*team_efficiency
```

### 2.2 Training Loop (Gradient Descent / Bayesian Optimization)

```
Step 1: Initialize Agent Weights
├─ CEO: {growth_weight: 0.6, risk_weight: 0.3, budget_weight: 0.1}
├─ CFO: {roi_weight: 0.5, risk_weight: 0.35, budget_weight: 0.15}
└─ HR: {team_weight: 0.6, burnout_weight: 0.4}

Step 2: Forward Pass (Prediction)
├─ For each scenario in training_set:
│  ├─ agent.analyze(scenario) → predicted_stance, confidence
│  ├─ Calculate accuracy vs ground_truth
│  └─ Store prediction

Step 3: Loss Calculation
├─ Classification Loss (cross-entropy for stance)
├─ Confidence Calibration Loss (predicted vs actual confidence)
└─ Multi-agent Disagreement Penalty (promote consensus)

Step 4: Backward Pass (Weight Update)
├─ Gradient descent: w = w - α * ∇L(w)
├─ Or Bayesian: Update weight posterior via MCMC
└─ Regularization: L2 penalty to prevent overfitting

Step 5: Validation
├─ Test on hold-out test set (20%)
├─ Monitor: Accuracy, Precision, Recall, F1-Score
└─ Early stopping if val_loss plateaus
```

### 2.3 Implementation Architecture

```
app/domain/agents/
├─ learning/
│  ├─ agent_calibrator.py      # Weight optimization
│  ├─ synthetic_data_gen.py    # Scenario generation
│  └─ performance_tracker.py   # Historical accuracy tracking
├─ reinforced_agent.py         # Agent with learnable weights
└─ debate_orchestrator.py      # Multi-round debate with feedback

app/application/use_cases/
├─ agent_training_service.py   # Orchestrate training pipeline
└─ debate_service.py           # Multi-round orchestration
```

---

## BÖLÜM 3: MULTI-ROUND DEBATE MEKANIZMI

### 3.1 Current State (Single Round)
```
Round 1:
├─ CEO analyzes → score: 75
├─ CFO analyzes → score: 60
└─ HR analyzes → score: 80
→ Average: 71.67 → REVISE (kaide: 50-74)
```

### 3.2 Enhanced Multi-Round (Tartışma)

```
Round 1: Initial Positions
├─ CEO: "SUPPORT" (75/100) - High ROI
├─ CFO: "NEUTRAL" (60/100) - Risk concerns
└─ HR: "SUPPORT" (80/100) - Team capable

Round 2: Rebuttal & Cross-Analysis
├─ CEO analyzes CFO's risk concern:
│  ├─ IF risk > 6 AND roi < 30% → CEO reduces confidence by 10%
│  └─ CEO confidence: 75 → 68
├─ CFO analyzes CEO's ROI confidence:
│  ├─ "CFO counters: Historical projects with this ROI overestimate by 15%"
│  └─ CFO confidence: 60 → 50
└─ HR reads both:
│  ├─ "If budget cuts happen (CFO concern), burnout ↑"
│  └─ HR confidence: 80 → 72

Updated Scores:
├─ CEO: 68
├─ CFO: 50
└─ HR: 72
Average: 63.33 → REVISE (converging to reality)

Round 3: Consensus Building
├─ CEO: "Agree with CFO on risk, lower to 62"
├─ CFO: "HR's burnout warning valid, increase to 55"
└─ HR: "All concerns addressed, maintain 72"
Average: 63 → REVISE

Final Consensus: REVISE (with detailed debate trace)
├─ Why REVISE? CEO and CFO identified real risks
├─ Recommendations: Reduce scope OR improve risk mitigation
└─ Confidence: 0.65 (well-calibrated due to debate)
```

### 3.3 Debate Protocol (Algorithm)

```python
class DebateOrchestrator:
    """
    Multi-round debate with agent learning and consensus building
    """
    
    def orchestrate_debate(
        self,
        scenario: ScenarioInput,
        agents: List[Agent],
        max_rounds: int = 3,
        convergence_threshold: float = 0.05
    ) -> DebateResult:
        """
        Debate phases:
        1. Round 1: Initial analysis (no prior knowledge)
        2. Round 2+: Cross-analysis (agents read others' outputs)
        3. Consensus: Aggregate with learned weights
        """
        
        messages = []
        scores_history = []
        
        for round_num in range(1, max_rounds + 1):
            round_messages = []
            round_scores = []
            
            # Each agent analyzes with previous messages
            for agent in agents:
                msg = agent.analyze(scenario, messages)
                round_messages.append(msg)
                round_scores.append(msg.confidence)
            
            messages.extend(round_messages)
            scores_history.append(round_scores)
            
            # Check convergence
            if len(scores_history) > 1:
                score_variance = np.std(round_scores)
                if score_variance < convergence_threshold:
                    break  # Consensus reached
        
        # Final aggregation with learned weights
        consensus = self.aggregate_with_learned_weights(messages)
        
        return DebateResult(
            messages=messages,
            consensus=consensus,
            rounds_taken=len(scores_history),
            trace=[...] # Full debate history
        )
```

---

## BÖLÜM 4: AGENT LEARNING MECHANISMS

### 4.1 Supervised Learning (Accuracy Improvement)

**Source:** Historical decisions + real outcomes

```python
# Training data example
training_data = [
    {
        "scenario": {...},
        "agent_prediction": {"stance": "support", "confidence": 0.75},
        "actual_outcome": {"success": True},
        "label": 1  # Correct prediction
    },
    ...
]

# Model: Logistic Regression or Random Forest
model = train_agent_classifier(training_data)
# Now: agent can have learned feature importance
```

### 4.2 Reinforcement Learning (Debate Strategy)

**Reward:** Accuracy of final consensus decision

```
Episode 1: Scenario X
├─ CEO: 70, CFO: 60, HR: 80
├─ Average: 70 → REVISE
└─ True outcome: REJECT
└─ Reward: -1.0 (wrong decision)

Agent learns: "My initial high confidence was wrong.
For similar future scenarios, reduce confidence"

Episode 2: Similar Scenario
├─ CEO: 65 (learned to reduce), CFO: 58, HR: 75
├─ Average: 66 → REVISE ✓
└─ Reward: +1.0 (correct)
```

### 4.3 Bayesian Learning (Uncertainty Quantification)

```python
# Agent maintains posterior distribution over weights
agent_weights_posterior = BetaDistribution(α=2, β=2)

# After each decision:
if prediction_correct:
    α += 1  # Success
else:
    β += 1  # Failure

# Confidence becomes adaptive
confidence = α / (α + β)
```

---

## BÖLÜM 5: VERI PIPELINE IMPLEMENTATION

### 5.1 Synthetic Data Generation

```python
# app/domain/learning/synthetic_data_gen.py

class SyntheticScenarioGenerator:
    """Generate realistic training scenarios with correlations"""
    
    def generate_dataset(self, n_scenarios: int = 1000) -> List[Dict]:
        scenarios = []
        
        for _ in range(n_scenarios):
            # Base distributions
            budget = np.random.lognormal(1.5, 1.2)
            roi = np.random.normal(25, 20)
            risk = np.random.randint(1, 11)
            team = np.random.normal(6, 2.5)
            
            # Inject correlations
            if budget > 10:
                risk += np.random.normal(1.5, 0.5)  # Higher risk for big projects
            
            if team < 4:
                roi -= np.random.normal(5, 2)  # Lower ROI if team unready
            
            # Generate ground truth (expert consensus)
            ground_truth = self._expert_consensus(budget, roi, risk, team)
            
            scenarios.append({
                "id": len(scenarios),
                "budget_million_usd": budget,
                "expected_roi_percent": roi,
                "risk_level": min(10, max(1, risk)),
                "team_readiness": min(10, max(1, team)),
                "ground_truth_decision": ground_truth,
                "created_at": datetime.now()
            })
        
        return scenarios
    
    def _expert_consensus(self, budget, roi, risk, team) -> str:
        """Simulate expert decision logic"""
        score = (roi/100) * 0.4 + (1 - risk/10) * 0.3 + (team/10) * 0.3
        if score >= 0.75:
            return "APPROVE"
        elif score >= 0.5:
            return "REVISE"
        else:
            return "REJECT"
```

### 5.2 Agent Calibration Service

```python
# app/domain/learning/agent_calibrator.py

class AgentCalibrator:
    """Learn agent weights from historical performance"""
    
    async def train_agent_weights(
        self,
        agent_name: str,
        training_scenarios: List[Dict],
        iterations: int = 100
    ) -> Dict[str, float]:
        """
        Use gradient descent to optimize agent weights
        """
        
        # Initialize weights
        weights = self._get_initial_weights(agent_name)
        learning_rate = 0.01
        
        for iteration in range(iterations):
            total_loss = 0
            gradients = {w: 0 for w in weights}
            
            for scenario in training_scenarios:
                # Forward pass with current weights
                prediction = self._predict_with_weights(
                    scenario, 
                    agent_name, 
                    weights
                )
                
                # Calculate loss
                loss = self._calculate_loss(prediction, scenario["ground_truth_decision"])
                total_loss += loss
                
                # Backward pass (calculate gradients)
                grads = self._calculate_gradients(scenario, agent_name, weights)
                for w in gradients:
                    gradients[w] += grads[w]
            
            # Update weights
            for w in weights:
                weights[w] -= learning_rate * (gradients[w] / len(training_scenarios))
            
            if iteration % 10 == 0:
                print(f"Iteration {iteration}: Loss = {total_loss / len(training_scenarios):.4f}")
        
        return weights
    
    def _predict_with_weights(self, scenario, agent_name, weights) -> str:
        """Predict decision using learned weights"""
        # Example for CEO
        if agent_name == "CEO":
            roi_norm = min(1.0, scenario["expected_roi_percent"] / 100.0)
            risk_norm = scenario["risk_level"] / 10.0
            budget_norm = min(1.0, scenario["budget_million_usd"] / 10.0)
            
            score = (
                weights.get("roi_weight", 0.6) * roi_norm +
                weights.get("risk_weight", 0.3) * (1 - risk_norm) +
                weights.get("budget_weight", 0.1) * budget_norm
            )
            
            if score >= 0.75:
                return "APPROVE"
            elif score >= 0.5:
                return "REVISE"
            else:
                return "REJECT"
```

---

## BÖLÜM 6: ROUND-BASED TARTIŞMA ÖRNEĞI

### Scenario:
```json
{
  "name": "Southeast Asia Expansion",
  "budget_million_usd": 5.0,
  "expected_roi_percent": 45.0,
  "risk_level": 6,
  "team_readiness": 7
}
```

### Execution Flow:

```
ROUND 1: Initial Analysis
─────────────────────────

CEO Message:
├─ Stance: SUPPORT
├─ Confidence: 0.78
└─ Reasoning: "High ROI (45%) offsets moderate risk. Growth potential strong."

CFO Message:
├─ Stance: NEUTRAL
├─ Confidence: 0.65
└─ Reasoning: "ROI promising BUT risk_level=6 concerning. Need risk mitigation."

HR Message:
├─ Stance: SUPPORT
├─ Confidence: 0.82
└─ Reasoning: "Team readiness=7 is adequate. Hiring load manageable."

Scores: [0.78, 0.65, 0.82] → Average: 0.75 → Decision: APPROVE


ROUND 2: Cross-Analysis with Learned Weights
──────────────────────────────────────────────

CEO Adjusts (considering CFO's risk warning):
├─ Previous CFO confidence: 0.65 (lower than CEO)
├─ CEO's learned pattern: "When CFO worried, reduce my confidence by 8%"
├─ New Confidence: 0.78 - 0.08 = 0.70
├─ Stance: SUPPORT (unchanged)
└─ Reasoning: "CFO flagged risk mitigation. We can address this with planning."

CFO Adjusts (considering CEO & HR support):
├─ Both CEO and HR confident
├─ CFO learned: "Majority support → risk might be acceptable"
├─ New Confidence: 0.65 + 0.05 = 0.70
├─ Stance: NEUTRAL → SUPPORT (upgraded!)
└─ Reasoning: "Team consensus and ready team reduce execution risk."

HR Maintains (both align with support):
├─ Confidence: 0.82 (unchanged)
├─ Stance: SUPPORT
└─ Reasoning: "No new concerns. Team ready."

Scores: [0.70, 0.70, 0.82] → Average: 0.74 → Decision: REVISE (?)


ROUND 3: Consensus Building
────────────────────────────

Orchestrator Aggregates with Learned Weights:
├─ CEO weight (learned): 0.35 (was 0.33)
├─ CFO weight (learned): 0.35 (was 0.33)
├─ HR weight (learned): 0.30 (was 0.34)

Weighted Score: 0.70*0.35 + 0.70*0.35 + 0.82*0.30 = 0.246 + 0.245 + 0.246 = 0.737

Final Decision: REVISE with Confidence: 0.74
├─ Rationale: "Consensus reached. Risk is manageable with proper planning."
├─ Debate Trace:
│  ├─ Round 1: CEO aggressive (0.78), CFO cautious (0.65)
│  ├─ Round 2: Agents converged after cross-analysis
│  └─ Round 3: Learned weights applied → stable decision
└─ Recommendations:
   ├─ Develop detailed risk mitigation plan
   ├─ Allocate 10% contingency budget
   └─ Schedule quarterly reviews
```

---

## BÖLÜM 7: METRICS & MONITORING

### 7.1 Agent Performance Metrics

```python
class AgentPerformanceMonitor:
    """Track agent accuracy over time"""
    
    def calculate_metrics(self, predictions, ground_truth):
        return {
            "accuracy": accuracy_score(predictions, ground_truth),
            "precision": precision_score(predictions, ground_truth, average='weighted'),
            "recall": recall_score(predictions, ground_truth, average='weighted'),
            "f1": f1_score(predictions, ground_truth, average='weighted'),
            "confidence_calibration": self._calibration_error(predictions, ground_truth),
            "auc_roc": roc_auc_score(predictions, ground_truth)
        }
```

### 7.2 Debate Quality Metrics

```python
{
    "convergence_rounds": 2,  # How many rounds until consensus?
    "disagreement_score": 0.08,  # Std of agent scores
    "debate_trace_length": 6,  # Number of messages
    "final_decision_confidence": 0.74,  # How confident was final decision?
    "decision_stability": 0.92  # Did decision stay same across rounds?
}
```

---

## BÖLÜM 8: IMPLEMENTATION ROADMAP

```
Week 1-2: Synthetic Data Generation
├─ Build SyntheticScenarioGenerator
├─ Generate 1000 training scenarios
└─ Create ground_truth labels

Week 3-4: Agent Calibration
├─ Build AgentCalibrator
├─ Train agent weights on synthetic data
└─ Validate on test set

Week 5-6: Multi-Round Debate
├─ Build DebateOrchestrator
├─ Implement cross-agent analysis
└─ Add learned weight aggregation

Week 7-8: Feedback Loop
├─ Real scenario execution
├─ Performance tracking
└─ Continuous weight updates

Week 9-10: Monitoring & Dashboards
├─ Streamlit dashboard
├─ Agent performance metrics
└─ Debate quality analytics
```

---

## ✅ BAŞLANGIC KONTROL LİSTESİ

- [ ] Synthetic data generator tasarla
- [ ] Database schema: agent_decisions table
- [ ] Agent calibrator implementation
- [ ] Multi-round debate orchestrator
- [ ] Performance tracking system
- [ ] Integration tests
- [ ] Streamlit dashboard mockup
