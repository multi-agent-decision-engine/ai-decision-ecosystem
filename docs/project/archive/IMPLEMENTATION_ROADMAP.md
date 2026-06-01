# 🚀 Agent Training Pipeline Roadmap
## From Data Collection to PhD-Ready Research (8-Week Plan)

**Key Decision:** Postpone outcome-based punishment (Phase 3) until after real data training (Phase 2) completes.

**Success Definition:** Agents trained on 100+ real business scenarios achieving >70% accuracy on unseen test data.

---

## PHASE 1: DATA COLLECTION (Weeks 1-2)

### Goal: Gather 100-150 real business scenarios

#### Week 1: Data Source Gathering

**Task 1.1: Harvard Business School Cases** (4 hours)
- Download 20-30 recent business cases (2020-2024)
- Extract decision scenarios & business metrics
- Store in: `real_datasets/hbs_cases_extracted.json`

**Task 1.2: SEC Filings Analysis** (6 hours)
- Download 50+ 10-K and 8-K filings (2022-2024)
- Extract strategic decisions (M&A, product launches, cost cuts)
- Store in: `real_datasets/sec_filings_extracted.json`

**Task 1.3: Kaggle Datasets** (2 hours)
- Filter for decision + outcome columns
- Standardize to our schema
- Store in: `real_datasets/kaggle_datasets_cleaned.csv`

**Task 1.4: McKinsey Case Collection** (3 hours)
- Review 30+ recent McKinsey cases
- Extract decision + outcome for documented results
- Store in: `real_datasets/mckinsey_cases_extracted.json`

#### Week 2: Data Validation & Cleaning

**Task 2.1: Data Standardization** (3 hours)
- Convert all sources to unified JSON schema
- Ensure consistent field names & types

**Task 2.2: Expert Validation** (4 hours)
- Review each scenario with domain expertise
- Mark: VALID, QUESTIONABLE, INVALID
- Target: 90%+ VALID rate

**Task 2.3: Quality Scoring** (2 hours)
- Score by: completeness, confidence justification, outcomes, recency
- Keep scenarios with Quality Score ≥ 0.7

**Task 2.4: Final Report** (1 hour)
- Create `reports/phase1_data_summary.json`
- Document: total scenarios, by source, quality metrics

**Phase 1 Success Criteria:**
- [ ] 100+ scenarios collected
- [ ] 90%+ validation rate
- [ ] All required fields present
- [ ] Data anonymized

---

## PHASE 2: AGENT TRAINING ON REAL DATA (Weeks 3-4)

### Goal: Train agents achieving >70% accuracy

**Task 3.1: Data Preparation** (1 hour)
```python
# Load all validated scenarios
# Split 70% train, 30% test
# Stratify by decision type
```

**Task 3.2: Train CEO Agent** (2 hours)
```python
ceo_calibrator = AgentCalibrator(agent_name="CEO", learning_rate=0.01)
history = ceo_calibrator.train(training_data, validation_data, epochs=100)
ceo_calibrator.save_weights("ceo_real_weights.json")
```

**Task 3.3: Train CFO & HR Agents** (2 hours)
- Repeat for CFO and HR
- Save: `cfo_real_weights.json`, `hr_real_weights.json`

**Task 3.4: Measure Debate Quality** (2 hours)
- Run debates on test set
- Calculate: convergence score, engagement, stability
- Target: Convergence < 0.05 std

**Task 3.5: Generate Phase 2 Report** (1 hour)
- Document accuracy by agent
- Save debate quality metrics
- Create `reports/phase2_training_results.json`

**Phase 2 Success Criteria:**
- [ ] All agents train without errors
- [ ] CEO/CFO/HR accuracy ≥ 70%
- [ ] Debate convergence < 0.05 std
- [ ] Weights saved for Phase 3

---

## PHASE 3: OUTCOME-BASED PUNISHMENT (Weeks 5-6)

### Goal: Add outcome-based loss, improve by 1-2%

**Task 5.1: Implement OutcomeLoss** (3 hours)
- Create `app/domain/learning/outcome_loss.py`
- Implement OutcomeBasedLoss class
- Multi-dimensional: ROI error + market success + team burnout + overconfidence

**Task 5.2: Update AgentCalibrator** (2 hours)
- Modify `_calculate_loss()` to include outcome_loss
- Phase 3 weighting: decision=0.40, outcome=0.40, confidence=0.15, reg=0.05

**Task 5.3: Phase 3 Training** (2 hours)
```python
# Load Phase 2 weights as starting point
# Train with outcome loss
# Fine-tune: 50 epochs
# Compare accuracy vs Phase 2
```

**Task 5.4: Outcome Prediction Metrics** (2 hours)
- Measure: ROI prediction error MAE
- Target: < 10% error

**Task 5.5: Phase 3 Report** (1 hour)
- Compare Phase 2 vs Phase 3
- Document improvements
- Save `reports/phase3_outcome_analysis.json`

**Phase 3 Success Criteria:**
- [ ] OutcomeLoss implemented & tested
- [ ] Decision accuracy improves 1-2% over Phase 2
- [ ] Outcome prediction MAE < 10%
- [ ] Debate convergence faster than Phase 2

---

## PHASE 4: VALIDATION & PUBLICATION (Weeks 7-8)

### Goal: Publish PhD-ready results

**Task 6.1: Cross-Validation** (2 hours)
- 5-fold cross-validation on test set
- Report mean accuracy ± std

**Task 6.2: Statistical Analysis** (1 hour)
- T-test: Phase 2 vs Phase 3 accuracy
- Verify statistical significance (p < 0.05)

**Task 6.3: Write Research Paper** (4 hours)
- Sections: Abstract, Introduction, Method, Results, Discussion, Conclusion
- Include tables: accuracy comparison, debate quality metrics
- Include figures: convergence over rounds, cross-fold performance

**Task 6.4: Final Report** (1 hour)
- Document: data collected, agents trained, accuracy achieved
- Status: PUBLICATION READY

---

## Project File Structure

```
multiagent/
├── data/
│   ├── real_datasets/
│   │   ├── hbs_cases_extracted.json
│   │   ├── sec_filings_extracted.json
│   │   ├── kaggle_cleaned.csv
│   │   ├── mckinsey_cases_extracted.json
│   │   └── company_internal_anonymized.json
│   └── synthetic/
│       └── training_scenarios.json
│
├── app/domain/learning/
│   ├── synthetic_data_gen.py ✅ Done
│   ├── agent_calibrator.py ✅ Phase 2 ready
│   ├── debate_orchestrator.py ✅ Done
│   └── outcome_loss.py ⏳ Phase 3 (NEW)
│
├── app/scripts/
│   ├── real_data_training.py ✅ Phase 2 main
│   └── phase3_training.py ⏳ Phase 3 (NEW)
│
├── reports/
│   ├── phase1_data_summary.json
│   ├── phase2_training_results.json
│   └── phase3_outcome_analysis.json
│
└── TRAINING_STRATEGY.md ✅
   OUTCOME_BASED_RL.md ✅
   IMPLEMENTATION_ROADMAP.md ✅
```

---

## Timeline Summary

| Week | Phase | Task | Deliverable |
|------|-------|------|-------------|
| 1-2 | **Phase 1** | Data collection & validation | 100+ scenarios |
| 3-4 | **Phase 2** | Agent training on real data | >70% accuracy |
| 5-6 | **Phase 3** | Outcome-based RL refinement | 1-2% improvement |
| 7-8 | **Phase 4** | Validation & publication | Research paper |

---

## Success Metrics

**Phase 1:** 100+ scenarios, 90%+ valid
**Phase 2:** CEO/CFO/HR >70% accuracy, convergence <0.05 std
**Phase 3:** +1-2% accuracy improvement, outcome MAE <10%
**Phase 4:** Publication-ready research, 5-fold CV, p<0.05 significance

---

**Total Effort:** ~130 hours over 8 weeks (16-17 hours/week)
**Publication Venue:** JMLR, NeurIPS, or domain conference
**Status:** READY TO START
