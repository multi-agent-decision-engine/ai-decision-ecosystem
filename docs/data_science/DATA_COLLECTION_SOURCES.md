# 📊 REAL DATA COLLECTION SOURCES
## PhD-Level Datasets for Agent Training

---

## 🎯 INTERNETTEN BULABİLECEĞİN PUBLIC DATASETS

### **1. HARVARD BUSINESS SCHOOL (HBS) CASE STUDIES** ⭐

```
Link: https://www.hbsp.harvard.edu/collections/cases
Free: Some cases open access (filters needed)
Paid: $10-30 per case (university usually has access)

What's there:
├─ Real business decisions
├─ Background + context
├─ Decision made + rationale
├─ Outcomes described
└─ 100+ cases (strategic decisions, M&A, investments)

Examples:
├─ "Kodak's Digital Moment" - Product strategy
├─ "Uber's Expansion Strategy" - Market entry
├─ "Netflix Strategy" - Business model
└─ "Amazon Go" - Technology investment

How to extract:
1. Read case study PDF
2. Identify decision context (budget, risk, ROI)
3. Note the decision made
4. Look for outcome section (what happened)
5. Extract as structured data

Target: 20-30 cases
```

### **2. KAGGLE DATASETS** 

```
Link: https://www.kaggle.com/datasets
Search: "business decision", "project management", "ROI"

Relevant Datasets:
├─ Project Management Datasets
│  └─ https://www.kaggle.com/search?q=project+management
├─ Investment/Business Datasets
│  └─ https://www.kaggle.com/search?q=investment+decisions
├─ Risk Analysis Datasets
│  └─ https://www.kaggle.com/search?q=risk+assessment
└─ Corporate Finance Datasets
   └─ https://www.kaggle.com/search?q=corporate+finance

Quality: Variable (read reviews first)
Target: 10-20 usable datasets
```

### **3. SEC FILINGS (US Companies)**

```
Link: https://www.sec.gov/edgar/
Free: Public access, no login needed

What's there:
├─ 10-K forms (annual reports)
├─ 10-Q forms (quarterly reports)
├─ S-1 (IPO filings)
├─ 8-K (material events)
└─ Proxy statements (board decisions)

Business Decisions Documented:
├─ Major acquisitions/investments
├─ Strategic pivots
├─ Risk assessments
├─ Board approvals
└─ Financial impacts

Companies to search:
├─ Tech: Apple, Google, Microsoft, Amazon
├─ Finance: JPMorgan, Goldman Sachs
├─ Retail: Walmart, Target
└─ Healthcare: UnitedHealth, CVS

How to extract:
1. Search company (EDGAR database)
2. Find 10-K/10-Q
3. Look for "Risk Factors" section
4. Find "Management's Discussion & Analysis"
5. Extract strategic decisions + outcomes

Target: 15-25 companies, multiple filings = 50-75 decisions
```

### **4. MCKINSEY CASE STUDIES & ARTICLES**

```
Link: https://www.mckinsey.com/insights
Free: Many articles open access

Types:
├─ "What we're thinking about"
├─ Business problem cases
├─ Decision frameworks
├─ Post-implementation reviews
└─ Quarterly Business Reviews (QBRs)

Useful Articles:
├─ "Strategy" section
├─ "Corporate Finance"
├─ "Operations"
└─ "Risk & Resilience"

Target: 10-15 case studies
```

### **5. BECKER FRIEDMAN INSTITUTE (Academic)**

```
Link: https://bfi.uchicago.edu/
Free: Academic papers with real data

Focus:
├─ Business economics
├─ Decision making
├─ Organizations
└─ Strategy

Target: 5-10 papers with datasets
```

### **6. EUROPEAN BANK FOR RECONSTRUCTION (EBRD)**

```
Link: https://www.ebrd.com/research
Free: Business climate surveys, investment data

Contains:
├─ Project evaluations
├─ Risk assessments
├─ ROI tracking
└─ Multi-year outcomes

Target: 5-10 investment projects
```

---

## 🏢 ŞIRKET VERİSİ (If Accessible)

### **Option A: Your Own Company**

```
Request from:
├─ CTO / VP Engineering
├─ CFO / Finance Director
├─ Chief Strategy Officer
└─ PMO (Project Management Office)

What to ask:
├─ "Historical project decisions (2020-2024)"
├─ "Budget estimate vs actual"
├─ "ROI expected vs achieved"
├─ "Risk assessments made"
├─ "Team readiness evaluations"
├─ "Final outcomes (success/failure)"

Privacy:
├─ Full anonymization
├─ NDA signature
├─ No client names
└─ No sensitive details

Expected: 50-100 projects
Timeline: 1-3 weeks negotiation
```

### **Option B: Partner Company**

```
Approach:
├─ Local startup/corporation
├─ Propose: "Data for PhD research"
├─ Offer: "Better decision framework as ROI"
└─ Mutual benefit

Template Email:
"Hi [Company],

I'm developing an AI decision support system.
I'd like access to your historical project data
(anonymized) to validate the algorithm.

In return, you get:
├─ Better decision frameworks
├─ Risk assessment tools
└─ ROI optimization models

Would you be interested?"

Expected: 30-50 projects
Timeline: 2-4 weeks
```

---

## 📥 HOW TO COLLECT (Step-by-Step)

### **Step 1: Source Identification (Week 1)**

```bash
# Create collection plan
📄 Create: data_sources.csv

Format:
source,url,format,difficulty,target_cases,notes
"Harvard Business School",https://hbsp.harvard.edu,PDF,medium,20,"Need university access or paid"
"SEC EDGAR",https://sec.gov/edgar,HTML/XML,easy,50,"Free public data"
"Kaggle",https://kaggle.com,CSV/JSON,easy,15,"Variable quality"
"McKinsey",https://mckinsey.com,articles,medium,10,"Free articles"
"Company X",internal,Excel,easy,50,"Contact CTO"
```
```

### **Step 2: Data Collection (Week 1-2)**

```python
# app/scripts/collect_public_datasets.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

class DataCollector:
    """Collect datasets from internet sources"""
    
    def collect_sec_filings(self, company_ticker, num_years=3):
        """
        Collect S&P 500 company data from SEC EDGAR
        
        Example: collect_sec_filings("AAPL", 3)
        Returns: Strategic decisions + financials
        """
        # Query SEC EDGAR API
        # Parse 10-K/10-Q
        # Extract:
        #   - Risk factors
        #   - Strategic initiatives
        #   - Capital expenditures
        #   - Business segments
        #   - Acquisitions
        pass
    
    def collect_kaggle_datasets(self, search_query):
        """Download datasets from Kaggle"""
        pass
    
    def collect_hbs_cases(self, category):
        """
        Collect HBS cases (manual process, mostly)
        
        1. Visit https://hbsp.harvard.edu
        2. Search: "Strategic decision", "Investment", etc.
        3. Download PDFs
        4. Extract structured data
        """
        pass
```

### **Step 3: Data Extraction (Week 2-3)**

```python
# app/scripts/extract_decision_data.py

class DecisionExtractor:
    """Extract decision from unstructured data"""
    
    def extract_from_hbs_case(self, pdf_text):
        """
        Example flow:
        1. Read case study PDF
        2. Identify:
           - Company profile
           - Decision context (budget, timing, market)
           - Key stakeholders (CEO, CFO, HR views)
           - Decision made (APPROVE/REJECT/REVISE)
           - Rationale
        3. Identify outcomes:
           - What happened
           - Success/failure
           - Financial impact
        4. Structure as JSON
        """
        
        decision = {
            "source": "HBS Case Study",
            "company": "...",
            "case_title": "...",
            
            "decision_context": {
                "budget_million": 50.0,
                "expected_roi": 35.0,
                "risk_level": 7,
                "team_readiness": 6,
                "market_timing": "urgent"
            },
            
            "decision": {
                "choice": "APPROVE",
                "stakeholder_views": {
                    "ceo": "support",
                    "cfo": "neutral",
                    "coo": "support"
                },
                "rationale": "..."
            },
            
            "outcomes": {
                "actual_roi": 32.0,
                "success": True,
                "timeline_months": 18,
                "challenges": ["..."],
                "lessons": ["..."]
            }
        }
        
        return decision
    
    def extract_from_sec_filing(self, xml_data):
        """Extract from 10-K"""
        pass
    
    def extract_from_article(self, article_text):
        """Extract from McKinsey/article"""
        pass
```

### **Step 4: Data Validation (Week 3)**

```
Checklist:
├─ [ ] Budget >= $1M (material decision)
├─ [ ] Decision clearly documented
├─ [ ] Outcomes known (12+ months later)
├─ [ ] Confidence high (not speculation)
├─ [ ] Multiple sources agree (if possible)
└─ [ ] No sensitive data included

Quality scores:
├─ High confidence: 8-10
├─ Medium confidence: 6-7
├─ Low confidence: 4-5
├─ Exclude: <4

Target: 70-100 HIGH confidence scenarios
```

---

## 📋 TARGET DATASET SPECIFICATION

```
Final Dataset (Collected + Curated):

├─ Number of scenarios: 100+
├─ Time span: 2015-2024 (diverse market conditions)
├─ Industries: 5+ (Tech, Finance, Retail, Healthcare, Mfg)
├─ Budget range: $1M - $500M
├─ Decision types:
│  ├─ Strategic investments
│  ├─ Market expansions
│  ├─ Product launches
│  ├─ M&A deals
│  ├─ Technology adoptions
│  └─ Cost reduction initiatives
│
├─ Quality:
│  ├─ 80%+ HIGH confidence
│  ├─ Full outcomes known
│  ├─ Experts validated
│  └─ Anonymized (if needed)
│
└─ Format: JSON/CSV with schema
```

---

## ✅ COLLECTION CHECKLIST

Week 1:
- [ ] HBS cases research (identify 20-30)
- [ ] SEC EDGAR search (identify 50-75 companies/decisions)
- [ ] Kaggle search (identify 10-15 datasets)
- [ ] McKinsey articles (identify 10-15 cases)
- [ ] Company contact (request data)

Week 2:
- [ ] Download all sources
- [ ] Manual extraction (HBS cases, articles)
- [ ] API extraction (SEC, Kaggle)
- [ ] Data structuring

Week 3:
- [ ] Validation + QA
- [ ] Remove low-confidence
- [ ] Expert review
- [ ] Final dataset (100+)

---

## 📊 EXPECTED OUTPUT

```
real_datasets_final/
├─ hbs_cases_extracted.json (20 scenarios)
├─ sec_filings_extracted.json (50+ scenarios)
├─ kaggle_datasets_cleaned.csv (15 scenarios)
├─ mckinsey_cases_extracted.json (10 scenarios)
├─ company_internal_anonymized.json (50 scenarios)
│
└─ COMBINED_DATASET.json (145 scenarios total)
   ├─ 100 training
   ├─ 25 validation
   └─ 20 test

Quality metrics:
├─ Completeness: 95%+
├─ Accuracy: Validated
├─ Confidence: Average 7.8/10
└─ Ready for: Agent training + PhD publication
```

---

## 🔗 QUICK LINKS TO START

**Public Datasets:**
1. https://www.hbsp.harvard.edu/collections/cases
2. https://www.sec.gov/edgar/
3. https://www.kaggle.com/
4. https://www.mckinsey.com/insights
5. https://bfi.uchicago.edu/

**Tools for Data Extraction:**
```bash
# PDF extraction
pip install pdfplumber PyPDF2

# Web scraping
pip install beautifulsoup4 selenium

# XML parsing
pip install xml2json xmltodict

# Data processing
pip install pandas numpy
```

---

**Başlayalım mı? Hangi kaynağın ile başlamak istersin?** 🚀
