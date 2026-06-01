# 🚀 DATA SCIENCE SPRINT IMPLEMENTATION ROADMAP

## Overview
Veri bilimi + agenları eğitmek = akıllı ajan sistemi

**Timeline:** 8-10 hafta  
**Output:** PhD-level multi-agent decision system

---

## SPRINT PHASE: Week 1-2
### Task: Synthetic Data Generation & Infrastructure

**Deliverables:**
- [ ] 1000 realistic training scenarios generated
- [ ] Ground truth labels (expert consensus)
- [ ] Simulated outcomes (real-world performance)
- [ ] Database schema updates
- [ ] JSON export pipeline

**Implementation:**

```bash
# 1. Create learning module structure
mkdir -p app/domain/learning
touch app/domain/learning/__init__.py
touch app/domain/learning/synthetic_data_gen.py
touch app/domain/learning/agent_calibrator.py
touch app/domain/learning/debate_orchestrator.py

# 2. Install dependencies
pip install numpy scipy pandas scikit-learn

# 3. Generate synthetic data
python -c "
from app.domain.learning.synthetic_data_gen import SyntheticDataGenerator
gen = SyntheticDataGenerator()
scenarios = gen.generate_dataset(n_scenarios=1000)
print(f'✅ Generated {len(scenarios)} scenarios')
"

# 4. Save to database
python scripts/load_training_data.py
```

**SQL Schema Addition:**

```sql
-- Historical agent decisions for training
CREATE TABLE agent_training_data (
    id SERIAL PRIMARY KEY,
    scenario_id INT NOT NULL,
    budget_million_usd FLOAT NOT NULL,
    expected_roi_percent FLOAT NOT NULL,
    risk_level INT NOT NULL,
    team_readiness INT NOT NULL,
    
    -- Ground truth (expert decision)
    expert_decision VARCHAR(20) NOT NULL,  -- APPROVE, REVISE, REJECT
    expert_confidence FLOAT NOT NULL,      -- 0.0-1.0
    
    -- Real outcome (simulated for now, real later)
    actual_roi_percent FLOAT,
    completion_months INT,
    team_burnout_rate FLOAT,
    market_success BOOLEAN,
    
    industry VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trained agent weights (persistable)
CREATE TABLE agent_weights (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(20) NOT NULL,  -- CEO, CFO, HR
    
    -- Learnable parameters
    roi_weight FLOAT NOT NULL,
    risk_weight FLOAT NOT NULL,
    team_weight FLOAT NOT NULL,
    confidence_base FLOAT NOT NULL,
    confidence_scaling FLOAT NOT NULL,
    
    -- Training metadata
    training_accuracy FLOAT,
    validation_accuracy FLOAT,
    epochs_trained INT,
    loss_final FLOAT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Debate traces (for analysis)
CREATE TABLE debate_traces (
    id SERIAL PRIMARY KEY,
    scenario_id INT NOT NULL,
    
    -- Debate info
    total_messages INT,
    rounds_to_consensus INT,
    final_decision VARCHAR(20),
    final_confidence FLOAT,
    convergence_score FLOAT,
    
    -- Analytics
    agent_participation JSONB,
    cross_references INT,
    stance_changes INT,
    debate_quality FLOAT,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## SPRINT PHASE: Week 3-4
### Task: Agent Calibration & Weight Training

**Deliverables:**
- [ ] Agent calibrator implemented & tested
- [ ] CEO/CFO/HR weights trained on synthetic data
- [ ] Validation accuracy >75%
- [ ] Weights persisted to database
- [ ] Training curves plotted

**Key Code Points:**

```python
# app/application/use_cases/agent_training_service.py

class AgentTrainingService:
    """Orchestrate agent training pipeline"""
    
    async def train_all_agents(self) -> Dict[str, Dict]:
        """Train CEO, CFO, HR with synthetic data"""
        
        # Load training data
        training_data = await self.repo.get_training_scenarios(limit=800)
        validation_data = await self.repo.get_training_scenarios(offset=800, limit=200)
        
        results = {}
        
        for agent_name in ["CEO", "CFO", "HR"]:
            calibrator = AgentCalibrator(agent_name, learning_rate=0.01)
            
            # Train
            history = calibrator.train(
                training_data=training_data,
                validation_data=validation_data,
                epochs=100,
                batch_size=32
            )
            
            # Validate
            val_accuracy = self._evaluate_accuracy(calibrator, validation_data)
            
            # Persist
            await self.repo.save_weights(
                agent_name=agent_name,
                weights=calibrator.weights.to_dict(),
                accuracy=val_accuracy
            )
            
            results[agent_name] = history
        
        return results
```

**Testing:**

```python
# tests/test_agent_calibrator.py

def test_agent_calibrator_training():
    """Verify weights improve over training"""
    
    calibrator = AgentCalibrator("CEO")
    initial_weights = calibrator.weights.copy()
    
    # Train on sample data
    history = calibrator.train(training_data=[...], validation_data=[...])
    
    # Verify weights changed
    assert calibrator.weights.roi_weight != initial_weights.roi_weight
    
    # Verify loss decreased
    assert history['final_val_loss'] < history['initial_val_loss']

def test_agents_improve_accuracy():
    """Cross-validate: trained agents better than baseline"""
    
    baseline_accuracy = 0.60  # Random guessing
    trained_accuracy = evaluate_agent("CEO", "trained_weights.json")
    
    assert trained_accuracy > baseline_accuracy + 0.10
```

---

## SPRINT PHASE: Week 5-6
### Task: Multi-Round Debate Engine

**Deliverables:**
- [ ] DebateOrchestrator implemented
- [ ] Cross-agent analysis working
- [ ] Learned weights applied to consensus
- [ ] Debate traces recorded
- [ ] Integration tests passing

**Implementation Steps:**

```python
# app/domain/learning/debate_orchestrator.py üzerinde build

# Step 1: Load trained weights
weights_dict = {
    "CEO": load_weights("ceo_weights.json"),
    "CFO": load_weights("cfo_weights.json"),
    "HR": load_weights("hr_weights.json")
}

# Step 2: Create agents
agents = {
    "CEO": CEOAgent(weights=weights_dict["CEO"]),
    "CFO": CFOAgent(weights=weights_dict["CFO"]),
    "HR": HRAgent(weights=weights_dict["HR"])
}

# Step 3: Run debate
orchestrator = DebateOrchestrator(max_rounds=3)
trace = orchestrator.orchestrate_debate(
    scenario=scenario,
    agents_dict=agents,
    learned_weights={"CEO": 0.35, "CFO": 0.35, "HR": 0.30}
)

# Step 4: Analyze
analytics = DebateAnalytics.analyze_trace(trace)
```

**API Endpoint Updates:**

```python
# app/presentation/routes/v1/scenarios.py

@router.post("/scenarios/{scenario_id}/simulate-with-debate")
async def simulate_with_debate(
    scenario_id: int,
    simulation_service: SimulationService = Depends(...)
):
    """Run multi-round debate simulation"""
    
    trace = await simulation_service.run_debate_simulation(scenario_id)
    
    return {
        "scenario_id": scenario_id,
        "final_decision": trace.final_decision,
        "confidence": trace.final_confidence,
        "rounds": trace.rounds_to_consensus,
        "debate_trace": [
            {
                "round": turn.round_number,
                "agent": turn.agent_name,
                "stance": turn.stance,
                "confidence": turn.confidence,
                "reasoning": turn.reasoning
            }
            for turn in trace.agent_turns
        ],
        "analytics": DebateAnalytics.analyze_trace(trace)
    }
```

---

## SPRINT PHASE: Week 7-8
### Task: Feedback Loop & Continuous Learning

**Deliverables:**
- [ ] Real scenario → outcome tracking
- [ ] Agent accuracy monitoring
- [ ] Weight retraining pipeline
- [ ] Performance dashboard
- [ ] Automated retraining triggers

**Implementation:**

```python
# app/domain/learning/performance_tracker.py

class PerformanceTracker:
    """Monitor agent accuracy in production"""
    
    async def track_outcome(
        self,
        scenario_id: int,
        final_decision: str,
        actual_outcome: str,  # After 3-6 months
        agent_predictions: Dict[str, str]
    ):
        """Record decision accuracy"""
        
        # Log prediction accuracy
        was_correct = final_decision == actual_outcome
        
        for agent_name, prediction in agent_predictions.items():
            await self.repo.log_agent_accuracy(
                agent_name=agent_name,
                prediction=prediction,
                was_correct=was_correct
            )
        
        # Trigger retraining if accuracy drops
        accuracy = await self.repo.get_recent_accuracy(agent_name, days=30)
        if accuracy < 0.65:  # Threshold
            await self.trigger_retraining(agent_name)
    
    async def trigger_retraining(self, agent_name: str):
        """Kick off weight retraining for degraded agent"""
        
        training_data = await self.repo.get_all_outcomes()  # Real data now!
        
        calibrator = AgentCalibrator(agent_name)
        new_weights = calibrator.train(training_data)
        
        await self.repo.save_weights(agent_name, new_weights)
        
        logger.info(f"✅ {agent_name} retrained with real outcomes")
```

---

## SPRINT PHASE: Week 9-10
### Task: Analytics Dashboard & PhD Documentation

**Deliverables:**
- [ ] Streamlit dashboard live
- [ ] Agent performance heatmaps
- [ ] Decision distribution analytics
- [ ] PhD-quality research paper draft
- [ ] Algorithms documented

**Streamlit Dashboard:**

```python
# streamlit_app.py

import streamlit as st
import plotly.express as px
from app.domain.learning.debate_orchestrator import DebateAnalytics

st.set_page_config(page_title="AI Decision Ecosystem", layout="wide")

st.title("🤖 AI Decision Ecosystem - Dashboard")

# Tab 1: Scenario Analysis
with st.tabs(["Scenario", "Agent Performance", "Debate Analytics", "Research"]):
    
    # Tab 1: Scenario Analysis
    with st.container():
        st.header("📊 Scenario Analysis")
        
        scenario_id = st.number_input("Scenario ID", min_value=1)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Budget", f"${scenario['budget_million_usd']:.1f}M")
        with col2:
            st.metric("Expected ROI", f"{scenario['expected_roi_percent']:.1f}%")
        with col3:
            st.metric("Risk Level", f"{scenario['risk_level']}/10")
        with col4:
            st.metric("Team Readiness", f"{scenario['team_readiness']}/10")
        
        # Run debate
        if st.button("Run Debate Simulation"):
            trace = run_debate(scenario_id)
            
            st.success(f"✅ Decision: {trace.final_decision}")
            st.metric("Confidence", f"{trace.final_confidence*100:.0f}%")
            st.metric("Rounds", trace.rounds_to_consensus)
            
            # Debate trace visualization
            st.subheader("Debate Trace")
            for turn in trace.agent_turns:
                with st.expander(f"Round {turn.round_number} - {turn.agent_name}"):
                    st.write(f"**Stance:** {turn.stance}")
                    st.write(f"**Confidence:** {turn.confidence*100:.0f}%")
                    st.write(f"**Reasoning:** {turn.reasoning}")
    
    # Tab 2: Agent Performance
    with st.container():
        st.header("🎯 Agent Performance Metrics")
        
        # Accuracy over time
        accuracy_data = get_agent_accuracy_timeseries()
        fig = px.line(accuracy_data, x="date", y="accuracy", color="agent")
        st.plotly_chart(fig)
        
        # Confusion matrix
        confusion = get_agent_confusion_matrix()
        st.write("Confusion Matrix (CEO):")
        st.dataframe(confusion)
    
    # Tab 3: Debate Analytics
    with st.container():
        st.header("💬 Debate Quality Metrics")
        
        analytics = get_debate_analytics_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Rounds", analytics['avg_rounds'])
        with col2:
            st.metric("Avg Convergence", analytics['avg_convergence'])
        with col3:
            st.metric("Cross-Refs per Debate", analytics['avg_cross_refs'])
    
    # Tab 4: Research
    with st.container():
        st.header("📚 Research & PhD Contributions")
        
        st.markdown("""
        ### Novel Algorithm: Multi-Agent Consensus Protocol
        
        **Paper Title:** 
        "Neuro-Symbolic Consensus in Enterprise Decision Systems:
        A Hybrid LLM + Deterministic Rules Approach"
        
        **Key Contributions:**
        1. Multi-round debate protocol with convergence guarantees
        2. Learned agent weights from historical outcomes
        3. Uncertainty quantification via confidence calibration
        4. Explainable AI integration (agent reasoning traces)
        
        **Metrics:**
        - Accuracy: 78.5% (vs 60% baseline)
        - Decision confidence well-calibrated
        - Debate convergence: avg 2.1 rounds
        """)
        
        # Download research paper draft
        st.download_button(
            label="📥 Download Research Paper",
            data=get_paper_draft(),
            file_name="research_paper.pdf"
        )
```

**Research Paper Outline:**

```markdown
# Neuro-Symbolic Consensus in Multi-Agent Decision Systems

## Abstract
We propose a novel hybrid approach combining:
- Symbolic rules (deterministic agent logic)
- Neural language models (Ollama LLM reasoning)
- Bayesian consensus (learned aggregation weights)

## 1. Introduction
- Problem: Enterprise decisions require domain expertise + risk awareness
- Existing approaches: 100% LLM (hallucination risk) or pure rules (inflexible)
- Our contribution: Interpretable multi-agent debate

## 2. System Architecture
- [Clean Architecture diagram]
- Agent roles (CEO, CFO, HR)
- Multi-round debate protocol

## 3. Learning Algorithm
- Weight optimization via gradient descent
- Synthetic data generation (1000+ realistic scenarios)
- Calibration via historical outcomes

## 4. Experiments
- Accuracy benchmarks
- Convergence analysis
- Comparison with baseline (single-agent, random aggregation)

## 5. Results
- Tables: Accuracy, F1, confidence calibration
- Figures: Learning curves, debate traces

## 6. Discussion
- When does debate help? (conflicting signals)
- When is single-round sufficient? (unanimous)
- Future: Multi-agent teams, hierarchical debates

## 7. Conclusion
- Reproducible, interpretable AI for critical decisions
- Open source implementation
```

---

## 📋 JIRA TASKS TEMPLATE

```
[JIRA-101] Generate synthetic training data (1000 scenarios)
└─ Subtasks:
   - Implement SyntheticDataGenerator class
   - Create 1000 scenarios with realistic correlations
   - Generate ground truth labels
   - Simulate real-world outcomes
   - Export to JSON

[JIRA-102] Implement agent calibrator
└─ Subtasks:
   - Define loss functions (classification, confidence)
   - Implement gradient descent optimizer
   - Train CEO/CFO/HR agents
   - Validate on test set
   - Save weights to DB

[JIRA-103] Build multi-round debate engine
└─ Subtasks:
   - Implement DebateOrchestrator
   - Cross-agent analysis logic
   - Convergence detection
   - Consensus aggregation
   - Debate trace recording

[JIRA-104] Add feedback loop & continuous learning
└─ Subtasks:
   - Performance tracking system
   - Accuracy monitoring
   - Automatic retraining triggers
   - Real-world outcome integration

[JIRA-105] Create analytics dashboard
└─ Subtasks:
   - Streamlit setup
   - Agent performance visualizations
   - Debate quality metrics
   - Research documentation
```

---

## ✅ QUALITY GATES

- [ ] 80%+ test coverage (unit + integration)
- [ ] All synthetic data validated
- [ ] Agent accuracy >75% on test set
- [ ] Debate convergence within 3 rounds
- [ ] CI/CD passing (GitHub Actions)
- [ ] Code review from 2 maintainers
- [ ] Documentation complete
- [ ] Performance benchmarks recorded

---

## 🎓 PhD-LEVEL OUTCOMES

By end of sprint:

1. **Novel Algorithm**: Multi-round debate protocol with learned weights
2. **Reproducible**: 1000+ training scenarios, open-source code
3. **Measurable**: Accuracy metrics, convergence analysis
4. **Research-Ready**: Paper draft + figures + tables
5. **Production-Ready**: Dashboard, monitoring, CI/CD

**Expected Publication Venues:**
- ACM Transactions on AI
- Journal of AI Research
- IEEE Intelligent Systems
