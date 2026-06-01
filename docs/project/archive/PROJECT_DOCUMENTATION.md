# 🤖 Multi-Agent Business Decision System
## PhD-Level Research Project

---

## 📚 Project Documentation

This project implements a multi-agent debate system for collaborative business decision-making with reinforcement learning.

### Key Documents

1. **[TRAINING_STRATEGY.md](TRAINING_STRATEGY.md)** — Why we follow: Data Collection → Training → Outcome-Based RL
   - Phase 1: Collect 100+ real scenarios (Weeks 1-2)
   - Phase 2: Train agents on real data >70% accuracy (Weeks 3-4)
   - Phase 3: Add outcome-based punishment via RL (Weeks 5-6)
   - Phase 4: Publication-ready validation (Weeks 7-8)

2. **[OUTCOME_BASED_RL.md](OUTCOME_BASED_RL.md)** — Detailed RL mechanism (Phase 3)
   - OutcomeBasedLoss implementation
   - Multi-dimensional penalty: ROI error, market success, team burnout, overconfidence
   - Agent-specific optimization (CEO growth, CFO risk, HR welfare)

3. **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)** — Week-by-week implementation plan
   - Hourly task breakdown
   - Data sources (HBS, SEC, Kaggle, McKinsey)
   - Success criteria for each phase
   - File structure & timeline

---

## 🏗️ Architecture

### Current State ✅
```
✅ AgentCalibrator (Phase 2 ready)
   - CrossEntropyLoss (decision accuracy)
   - ConfidenceCalibrationLoss (confidence matching)
   - L2 regularization
   - Gradient descent optimization

✅ DebateOrchestrator (multi-round discussion)
   - Round 1: Independent analysis
   - Round 2+: Cross-analysis with consensus
   - Quality metrics: convergence, engagement, stability

✅ SyntheticDataGenerator (1000+ scenarios)
   - Realistic distributions & correlations
   - Ground truth labels via expert consensus
   - Simulated outcomes (ROI, market success, team burnout)
```

### Phase 1: Data Collection 📊
**Goal:** Gather 100-150 real business scenarios
- HBS cases: 20-30 scenarios (4h)
- SEC filings: 50+ scenarios (6h)
- Kaggle: 10-15 scenarios (2h)
- McKinsey: 10-15 scenarios (3h)
- Validation & cleaning: 10h

**Output:** `data/real_datasets/` with validated scenarios

### Phase 2: Agent Training 🤖
**Goal:** >70% accuracy on real data
- Load real scenarios
- Train CEO, CFO, HR agents
- Measure debate quality
- Save trained weights

**Output:** `ceo_real_weights.json`, `cfo_real_weights.json`, `hr_real_weights.json`

### Phase 3: Outcome-Based RL ⚡
**Goal:** Add punishment mechanism, improve 1-2%
- Implement OutcomeBasedLoss
- Update AgentCalibrator
- Fine-tune with outcome loss
- Measure outcome prediction accuracy

**Output:** Improved agents + Phase 3 report

### Phase 4: Publication 📰
**Goal:** PhD-ready results
- Cross-validation
- Statistical significance
- Research paper
- Publication submission

---

## 📊 Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| **1** | Real scenarios | 100+ |
| **1** | Data quality score | ≥0.7 |
| **2** | Agent accuracy | ≥70% |
| **2** | Debate convergence | <0.05 std |
| **3** | Accuracy improvement | +1-2% |
| **3** | Outcome prediction | <10% MAE |
| **4** | Cross-validation | ≥70% |
| **4** | Statistical significance | p<0.05 |

---

## 🚀 Quick Start

### Next Steps (Phase 1)

1. **Read the strategy** → [TRAINING_STRATEGY.md](TRAINING_STRATEGY.md)
2. **Check the roadmap** → [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)
3. **Start data collection:**
   - HBS cases: https://www.hbs.edu/faculty/Pages/item.aspx?num=52676
   - SEC Edgar: https://www.sec.gov/edgar
   - Kaggle: https://www.kaggle.com/datasets (search "business decisions")
   - McKinsey: https://www.mckinsey.com/insights/featured-insights

4. **Create data folder:**
   ```bash
   mkdir -p data/real_datasets
   ```

---

## 📁 Project Structure

```
multiagent/
├── TRAINING_STRATEGY.md              ← START HERE: Why this order?
├── OUTCOME_BASED_RL.md               ← Phase 3 detailed mechanism
├── IMPLEMENTATION_ROADMAP.md         ← Week-by-week plan
├── README.md                         ← You are here
│
├── data/
│   ├── real_datasets/                ← Phase 1 deliverable (Phase 1)
│   │   ├── hbs_cases_extracted.json
│   │   ├── sec_filings_extracted.json
│   │   ├── kaggle_cleaned.csv
│   │   ├── mckinsey_cases_extracted.json
│   │   └── company_internal_anonymized.json
│   └── synthetic/
│       └── training_scenarios.json    ← Already exists (1000 scenarios)
│
├── app/
│   ├── domain/learning/
│   │   ├── synthetic_data_gen.py      ✅ Done
│   │   ├── agent_calibrator.py        ✅ Phase 2 ready
│   │   ├── debate_orchestrator.py     ✅ Done
│   │   └── outcome_loss.py            ⏳ Phase 3 (NEW)
│   │
│   ├── domain/agents/
│   │   ├── ceo_agent.py
│   │   ├── cfo_agent.py
│   │   └── hr_agent.py
│   │
│   └── scripts/
│       ├── real_data_training.py      ✅ Phase 2 ready
│       └── phase3_training.py         ⏳ Phase 3 (NEW)
│
└── reports/
    ├── phase1_data_summary.json       ← Phase 1 output
    ├── phase2_training_results.json   ← Phase 2 output
    └── phase3_outcome_analysis.json   ← Phase 3 output
```

---

## 🎯 Core Concept

### The Problem We're Solving

**Multi-agent debate for business decisions with outcome-aware learning**

Traditional approach: Agents make independent decisions
❌ Not collaborative
❌ Single points of failure
❌ No cross-validation

Multi-agent debate approach:
✅ CEO focuses on growth
✅ CFO focuses on risk management
✅ HR focuses on team welfare
✅ They debate and reach consensus

**With Outcome-Based RL:**
✅ Agents aren't just "right" or "wrong"
✅ They learn if their reasoning led to good business outcomes
✅ Separates "lucky guesses" from "smart reasoning"
✅ PhD-level contribution

---

## 📖 Phase Progression

### PHASE 1: Data Collection (Weeks 1-2)
```
Problem: We need real business examples to train on
Solution: Collect 100+ scenarios from HBS, SEC, Kaggle, McKinsey
Why: Synthetic data is good, but real data proves it works
```

### PHASE 2: Agent Training (Weeks 3-4)
```
Problem: Agents need to learn decision patterns from examples
Solution: Train CEO/CFO/HR on real data
Why: Real data validation shows agents understand business logic
Target: >70% accuracy
```

### PHASE 3: Outcome-Based RL (Weeks 5-6)
```
Problem: Agents can predict decisions, but do they drive good outcomes?
Solution: Add outcome_loss (ROI accuracy, market success, team health)
Why: Separates "lucky" decisions from "smart" reasoning
Target: +1-2% accuracy improvement
```

### PHASE 4: Publication (Weeks 7-8)
```
Problem: Results need academic rigor
Solution: Cross-validation, statistical testing, research paper
Why: PhD-quality validation
Output: Publication-ready manuscript
```

---

## 💡 Key Innovation

**Outcome-based reinforcement learning for business agents**

Traditional ML: Optimize for decision label accuracy (0/1)
**Our approach:** Optimize for business outcomes (ROI, success, team wellness)

Example:
```
Agent predicts: APPROVE ✅ (correct decision label)
Actual outcome: ROI = -5% ❌ (bad business result)

Old loss: 0.0 (decision was correct)
New loss: HIGH (outcome was bad)

Agent learns: "Being right isn't enough. I need to predict outcomes correctly too."
```

---

## 🔗 Related Files

- Agents: `app/domain/agents/`
- Data pipeline: `app/scripts/real_data_training.py`
- Debate system: `app/domain/learning/debate_orchestrator.py`
- Tests: `tests/`

---

## 📝 Notes

- **Total effort:** ~130 hours over 8 weeks
- **Publication venues:** JMLR, NeurIPS, ACM Transactions
- **Status:** Ready to start Phase 1
- **Last updated:** 2026-04-30

---

**Questions?** Refer to the three documentation files above. Each answers a specific question:
- *"Why this order?"* → TRAINING_STRATEGY.md
- *"How does outcome-based RL work?"* → OUTCOME_BASED_RL.md
- *"What do I do this week?"* → IMPLEMENTATION_ROADMAP.md
