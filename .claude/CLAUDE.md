# 🤖 Multiagent Business Decision System
## Project Documentation for Claude Code

---

## 📌 Project Overview

**Mission:** Build a multi-agent collaborative decision system that learns from real business data and outcome-based reinforcement learning.

**Status:** Phase 1 (Data Collection) — Ready to start
**Last Updated:** 2026-04-30
**Team:** Solo researcher

---

## 🏗️ Current Architecture

### Clean Architecture Pattern
```
app/
├── domain/
│   ├── agents/           # CEO, CFO, HR agents
│   ├── learning/         # AgentCalibrator, DebateOrchestrator, SyntheticDataGen
│   ├── services/         # Classifier, Aggregator
│   ├── repositories.py   # Data access interface
│   └── models.py         # Domain models
├── infrastructure/
│   ├── database/         # SQLAlchemy, Alembic migrations
│   ├── llm.py           # Claude API integration
│   ├── repositories/     # SQL implementations
│   └── config.py        # Configuration
├── application/
│   ├── use_cases/       # Business logic
│   └── exceptions.py    # Custom exceptions
├── presentation/
│   ├── api/v1/routes/   # FastAPI endpoints
│   └── schemas/         # Pydantic models
└── main.py             # App entry point
```

### Key Components

**1. Multi-Agent System**
- **CEO Agent:** Growth-focused (ROI weight 60%)
- **CFO Agent:** Risk-averse (Risk weight 35%)
- **HR Agent:** Team-welfare focused (Burnout weight 55%)

Each agent:
- Analyzes business scenarios independently
- Provides confidence score
- Participates in multi-round debate
- Learns from outcomes

**2. Debate Orchestrator**
- Round 1: Independent analysis (no prior messages)
- Round 2+: Cross-analysis with feedback
- Consensus: Weighted aggregation
- Quality metrics: convergence, engagement, stability

**3. Agent Calibrator (Phase 2)**
- Loss: Decision + Confidence + L2 regularization
- Optimizer: SGD with numerical gradients
- Early stopping: 10-epoch patience
- Metrics: accuracy, precision, recall, F1

**4. Outcome-Based Loss (Phase 3) — PLANNED**
- ROI prediction accuracy (50% weight)
- Market success (25% weight)
- Team burnout (15% weight)
- Overconfidence penalty (10% weight)

---

## 📊 3-Phase Implementation Plan

### PHASE 1: Data Collection (Weeks 1-2)
**Goal:** Gather 100-150 real business scenarios

**Data Sources:**
- HBS cases: 20-30 scenarios (4 hours)
- SEC filings: 50+ scenarios (6 hours)
- Kaggle datasets: 10-15 scenarios (2 hours)
- McKinsey cases: 10-15 scenarios (3 hours)
- Internal data: 5-20 scenarios (if available, 2 hours)

**Deliverables:**
- `data/real_datasets/` folder with 5 JSON files
- `reports/phase1_data_summary.json` (metadata)
- Quality score ≥ 0.7 for 95% of scenarios

**Success Criteria:**
- ✅ 100+ scenarios collected
- ✅ 90%+ pass validation
- ✅ All required fields present
- ✅ Data anonymized & ready

---

### PHASE 2: Agent Training (Weeks 3-4)
**Goal:** Train agents achieving >70% accuracy on real data

**Current Implementation Status:** ✅ READY

Files:
- `app/domain/learning/agent_calibrator.py` — Calibration engine
- `app/scripts/real_data_training.py` — Training pipeline
- `app/domain/learning/debate_orchestrator.py` — Debate manager

**Process:**
1. Load 100+ real scenarios from Phase 1
2. Split: 70% train, 30% test (stratified)
3. Train each agent independently
4. Measure debate quality
5. Save trained weights

**Deliverables:**
- `ceo_real_weights.json`, `cfo_real_weights.json`, `hr_real_weights.json`
- `reports/phase2_training_results.json`
- Accuracy metrics per agent
- Debate quality metrics

**Success Criteria:**
- ✅ CEO accuracy ≥ 70%
- ✅ CFO accuracy ≥ 70%
- ✅ HR accuracy ≥ 70%
- ✅ Debate convergence < 0.05 std
- ✅ Cross-agent engagement > 60%

---

### PHASE 3: Outcome-Based RL (Weeks 5-6)
**Goal:** Add outcome-based punishment, improve accuracy 1-2%

**New Files (TO CREATE):**
- `app/domain/learning/outcome_loss.py` — OutcomeBasedLoss class
- `app/scripts/phase3_training.py` — Fine-tuning pipeline
- `tests/test_outcome_loss.py` — Unit tests

**Mechanism:**
- Agents penalized for poor outcomes (not just wrong decisions)
- 4-dimensional loss: ROI error + success + burnout + overconfidence
- Agent-specific weights (CEO growth, CFO risk, HR welfare)

**Deliverables:**
- Updated agent weights (phase3_*_weights.json)
- `reports/phase3_outcome_analysis.json`
- Comparison: Phase 2 vs Phase 3 accuracy
- Outcome prediction MAE < 10%

**Success Criteria:**
- ✅ Decision accuracy +1-2% over Phase 2
- ✅ Outcome prediction MAE < 10%
- ✅ Debate convergence -30% faster
- ✅ Confidence calibration +10%

---

### PHASE 4: Validation & Publication (Weeks 7-8)
**Goal:** PhD-ready results

**Tasks:**
- 5-fold cross-validation
- Statistical significance (t-test, p<0.05)
- Research paper (4-5 pages)
- GitHub repo documentation

**Deliverables:**
- Cross-validation scores & statistics
- Research paper (Markdown or LaTeX)
- Final metrics report
- Publication-ready artifacts

---

## 📁 Key Files Reference

### Learning System
```
app/domain/learning/
├── synthetic_data_gen.py          ✅ Generates 1000+ scenarios
├── agent_calibrator.py            ✅ Phase 2 ready
├── debate_orchestrator.py         ✅ Multi-round discussion
└── outcome_loss.py               ⏳ Phase 3 (NEW)
```

### Agents
```
app/domain/agents/
├── base.py                        # Agent interface
├── ceo_agent.py                   # Growth-focused
├── cfo_agent.py                   # Risk-averse
└── hr_agent.py                    # Team-focused
```

### Data & Pipeline
```
app/scripts/
├── seed_data_generator.py         ✅ Synthetic data
├── real_data_training.py          ✅ Phase 2 pipeline
└── phase3_training.py            ⏳ Phase 3 (NEW)

data/
├── real_datasets/                 ← Phase 1 deliverable
│   ├── hbs_cases_extracted.json
│   ├── sec_filings_extracted.json
│   ├── kaggle_cleaned.csv
│   ├── mckinsey_cases_extracted.json
│   └── company_internal_anonymized.json
└── synthetic/
    └── training_scenarios.json     ✅ Exists (1000 scenarios)
```

### Reporting
```
reports/
├── phase1_data_summary.json       ← Phase 1 output
├── phase2_training_results.json   ← Phase 2 output
└── phase3_outcome_analysis.json   ← Phase 3 output
```

---

## 🎯 Working Guidelines

### When Starting Work

1. **Check current phase:**
   - Am I in Phase 1, 2, 3, or 4?
   - What's the success criteria?

2. **Read relevant docs:**
   - `PROJECT_DOCUMENTATION.md` — Overview
   - `TRAINING_STRATEGY.md` — Why this order?
   - `IMPLEMENTATION_ROADMAP.md` — Weekly tasks

3. **Use synthetic data first:**
   - Test logic on `data/synthetic/training_scenarios.json` (1000 scenarios)
   - Verify accuracy targets
   - Only then move to real data

4. **Phase gate:** Don't jump phases
   - Phase 1 must finish before Phase 2
   - Phase 2 baseline before Phase 3 RL
   - Phase 3 before publication

### Code Standards

- **Architecture:** Clean Architecture (domain → infrastructure → presentation)
- **Testing:** Unit tests required for new features
- **Agents:** Agent-specific weights (CEO/CFO/HR different priorities)
- **Loss:** Phase 2 decision+confidence, Phase 3 +outcome
- **Metrics:** Always measure accuracy, convergence, engagement

### Important Constraints

❌ **DON'T:**
- Start Phase 3 before Phase 2 finishes
- Train on synthetic data thinking it's real
- Mix synthetic and real data without explicit split
- Ignore agent-specific optimization (CEO ≠ HR)
- Skip debate orchestration (agents must debate)

✅ **DO:**
- Validate data quality (score ≥ 0.7)
- Test on hold-out test set (30%)
- Measure debate convergence
- Track accuracy over epochs
- Save checkpoints at each phase

---

## 🔗 Related Documentation

### In Project Root
1. **[PROJECT_DOCUMENTATION.md](../PROJECT_DOCUMENTATION.md)** — Start here (overview)
2. **[TRAINING_STRATEGY.md](../TRAINING_STRATEGY.md)** — Why Phase 1→2→3→4?
3. **[OUTCOME_BASED_RL.md](../OUTCOME_BASED_RL.md)** — Phase 3 details
4. **[IMPLEMENTATION_ROADMAP.md](../IMPLEMENTATION_ROADMAP.md)** — Week-by-week tasks

### In This Folder (.claude)
- `settings.local.json` — Project permissions & config
- `CLAUDE.md` — This file (project context)

---

## 📊 Success Metrics by Phase

| Phase | Metric | Target | Status |
|-------|--------|--------|--------|
| **1** | Real scenarios | 100+ | ⏳ Pending |
| **1** | Data quality | ≥0.7 | ⏳ Pending |
| **2** | CEO accuracy | ≥70% | ⏳ Pending |
| **2** | CFO accuracy | ≥70% | ⏳ Pending |
| **2** | HR accuracy | ≥70% | ⏳ Pending |
| **2** | Convergence | <0.05 std | ⏳ Pending |
| **3** | Accuracy gain | +1-2% | ⏳ Pending |
| **3** | Outcome MAE | <10% | ⏳ Pending |
| **4** | CV score | ≥70% | ⏳ Pending |
| **4** | p-value | <0.05 | ⏳ Pending |

---

## 🚀 Quick Start Commands

### Setup
```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Create data directories
mkdir -p data/real_datasets
mkdir -p reports
```

### Phase 1: Generate Synthetic Data (for testing)
```python
from app.domain.learning.synthetic_data_gen import SyntheticDataGenerator

gen = SyntheticDataGenerator(random_seed=42)
scenarios = gen.generate_dataset(n_scenarios=1000, distribution="realistic")
```

### Phase 2: Train on Real Data
```python
from app.scripts.real_data_training import RealDataPipeline

pipeline = RealDataPipeline(data_directory="data/real_datasets/")
results = pipeline.run_full_pipeline()
```

### Phase 3: Add Outcome Loss (FUTURE)
```python
# Will be implemented in Phase 3
from app.domain.learning.outcome_loss import OutcomeBasedLoss
```

---

## ⚠️ Important Notes

1. **Data Privacy:** All company data must be anonymized
2. **Baseline:** Synthetic data gives ~75-80% accuracy (use as reference)
3. **Real data:** Target >70% accuracy (real data is messier)
4. **Outcome loss:** Only valid when outcomes are known (Phase 3)
5. **Publication:** Results need 5-fold CV + statistical test (p<0.05)

---

## 🔄 Current Status

**Overall Progress:** 25% (Phase 1 ready to start)

- ✅ Architecture designed & implemented
- ✅ Agents created (CEO/CFO/HR)
- ✅ Debate system working
- ✅ Agent calibrator ready
- ✅ Synthetic data generator ready
- ⏳ Phase 1: Data collection (START HERE)
- ⏳ Phase 2: Agent training
- ⏳ Phase 3: Outcome-based RL
- ⏳ Phase 4: Publication

**Next Step:** Start Phase 1 data collection (HBS, SEC, Kaggle, McKinsey)

---

## 📞 Questions?

Refer to:
- **"What do I do?"** → `IMPLEMENTATION_ROADMAP.md`
- **"Why this order?"** → `TRAINING_STRATEGY.md`
- **"How does Phase 3 work?"** → `OUTCOME_BASED_RL.md`
- **"Quick overview?"** → `PROJECT_DOCUMENTATION.md`

---

**Document Version:** 1.0
**Last Updated:** 2026-04-30
**Owner:** AI Research Team
**Status:** ACTIVE
