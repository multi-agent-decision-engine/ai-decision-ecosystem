# 🎯 Outcome-Based Punishment System
## Reinforcement Learning through Real-World Outcomes

---

## Overview

**What:** Agents get penalized when their decisions lead to poor business outcomes, not just when predictions are wrong.

**Why:** Separates "lucky guesses" from "good reasoning"
- Agent says APPROVE, actually correct decision ✅ BUT ROI = -5% instead of predicted 45% ❌
- Current: Only decision loss (0.0) | New: Adds outcome loss (penalty)

**When:** Phase 3 (after agents trained on real data with baseline accuracy)

---

## The Problem Current Loss Misses

### Example Scenario
```
Agent Decision: "APPROVE" (Ground truth: "APPROVE" ✓)
Agent Confidence: 95%

Synthetic Outcome:
  Predicted ROI: +45%
  Actual ROI: -5%
  Market Success: False

Current Loss:
  ✓ Decision correct → 0.0 loss
  ✓ High confidence on correct decision → 0.0 loss
  = Total: 0.0 (Agent thinks it's perfect)

New Outcome Loss:
  ✗ Actual outcome = disaster
  = Penalty agent for bad reasoning (even though decision label was "correct")
```

**Impact:** Without outcome loss, agents learn to mimic decision patterns, not understand business logic.

---

## Implementation Architecture

### New Loss Function: OutcomeLoss

```python
class OutcomeBasedLoss(LossFunction):
    """
    Penalizes agent when actual outcome diverges from expected outcome
    """
    
    def compute(
        self, 
        predicted_roi: float,          # What agent expected
        actual_roi: float,              # What actually happened
        market_success: bool,           # Did it work?
        team_burnout: float,           # Team health (0-1)
        prediction_confidence: float   # How sure was agent?
    ) -> float:
        """
        Multi-dimensional outcome loss
        
        Returns: loss 0.0-1.0
        """
        
        # Dimension 1: ROI accuracy
        roi_error = abs(predicted_roi - actual_roi)
        roi_loss = np.tanh(roi_error / 100)  # Saturates at ±100%
        
        # Dimension 2: Market success
        success_loss = 0.0 if market_success else 0.5
        
        # Dimension 3: Team health (burnout should stay low)
        burnout_loss = team_burnout  # Higher burnout = higher loss
        
        # Confidence penalty: overconfident predictions on bad outcomes
        if not market_success and prediction_confidence > 0.7:
            confidence_penalty = 0.2
        else:
            confidence_penalty = 0.0
        
        # Weighted combination
        total_loss = (
            roi_loss * 0.50 +           # ROI accuracy critical
            success_loss * 0.25 +       # Market acceptance
            burnout_loss * 0.15 +       # Team welfare
            confidence_penalty * 0.10   # Overconfidence penalty
        )
        
        return total_loss
```

### Updated AgentCalibrator Loss

```python
def _calculate_loss(
    self,
    scenario: Dict,
    prediction: str,
    confidence: float
) -> float:
    """
    PHASE 2 (current):
    total_loss = decision_loss + confidence_loss + regularization
    
    PHASE 3 (new):
    total_loss = decision_loss + outcome_loss + confidence_loss + regularization
    """
    
    # Existing losses (Phase 2)
    clf_loss = CrossEntropyLoss().compute(prediction, scenario["ground_truth_decision"])
    conf_loss = ConfidenceCalibrationLoss().compute(confidence, prediction == scenario["ground_truth_decision"])
    
    # NEW: Outcome loss (Phase 3 only)
    outcome_loss = 0.0
    if "actual_roi_percent" in scenario:  # Real/synthetic data with outcomes
        outcome_loss = OutcomeBasedLoss().compute(
            predicted_roi=scenario["expected_roi_percent"],
            actual_roi=scenario["actual_roi_percent"],
            market_success=scenario.get("market_success", False),
            team_burnout=scenario.get("team_burnout_rate", 0.0),
            prediction_confidence=confidence
        )
    
    # L2 regularization
    weight_magnitude = sum([w**2 for w in self.weights.values()])
    reg_loss = self.l2_reg * weight_magnitude
    
    # Combine (Phase 3 weights outcome heavily since we have data)
    total_loss = (
        clf_loss * 0.40 +
        outcome_loss * 0.40 +        # NEW: Equal weight to outcome
        conf_loss * 0.15 +
        reg_loss * 0.05
    )
    
    return total_loss
```

---

## Agent-Specific Outcome Optimization

### CEO Agent: Growth Outcomes
```
Outcome metrics CEO cares about:
  ✓ ROI > predicted (bonus)
  ✓ Market success (binary, important)
  ✓ Team burnout < 0.3 (acceptable)
  
Loss weights:
  - ROI_weight: 0.60 (growth-focused)
  - Success_weight: 0.25
  - Burnout_weight: 0.15
```

### CFO Agent: Risk Management
```
Outcome metrics CFO cares about:
  ✓ ROI stable (low variance preferred)
  ✓ Team burnout < 0.2 (stricter)
  ✓ Market success (secondary)
  
Loss weights:
  - ROI_accuracy_weight: 0.50 (not raw ROI, but prediction accuracy)
  - Success_weight: 0.20
  - Burnout_weight: 0.30 (risk averse)
```

### HR Agent: Team Welfare
```
Outcome metrics HR cares about:
  ✓ Team burnout < 0.25 (primary concern)
  ✓ Completion in reasonable time
  ✓ Market success (team morale indicator)
  
Loss weights:
  - ROI_weight: 0.20 (less important)
  - Success_weight: 0.25
  - Burnout_weight: 0.55 (team welfare paramount)
```

---

## Expected Outcomes (Phase 3)

### Success Criteria

| Metric | Phase 2 Target | Phase 3 Target | Reason |
|--------|---|---|---|
| Decision Accuracy | 70% | 72% | Outcome loss refines weight balance |
| Outcome Prediction Error | N/A | <10% MAE | New focus of training |
| Debate Convergence | <0.05 std | <0.03 std | Agents more aligned on outcomes |
| Confidence Calibration | 65% | 75% | Outcome feedback improves confidence |

### Publication Narrative

```
"Phase 2: Agents achieve 70% accuracy learning decision patterns
 Phase 3: By incorporating outcome-based loss, agents improve to:
   - 72% decision accuracy (better weight balance)
   - 75% outcome prediction accuracy (new capability)
   - Faster debate convergence (agents aligned on outcomes)
   
Conclusion: Outcome-based RL improves both decision quality and 
business impact prediction, enabling agents to optimize for 
real-world success, not just decision labels."
```

---

## Code Locations

- **OutcomeLoss class:** `app/domain/learning/outcome_loss.py` (new)
- **Updated AgentCalibrator:** `app/domain/learning/agent_calibrator.py` (Phase 3 branch)
- **Debate weight adjustment:** `app/domain/learning/debate_orchestrator.py` (phase3_weights method)
- **Tests:** `tests/test_outcome_loss.py` (new)
- **Pipeline:** `app/scripts/phase3_training.py` (new)
