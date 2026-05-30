import os
import json
import pandas as pd

def normalize_dataset(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Kaynak Excel dosyası bulunamadı: {input_path}")
        
    df = pd.read_excel(input_path)
    normalized_records = []
    
    for index, row in df.iterrows():
        # Madde 5: Budget Imputation (Normalize aşamasında 5.0 baseline atanıyor)
        budget = 5.0
        
        # Madde 3: Cost Savings (%) -> expected_roi_percent
        roi = float(row['Cost Savings (%)'])
        
        # Madde 4 & 5: Risk Mitigation (1-5) -> Önce gerçek riske tersle, sonra 1-10 skalasına genişlet
        # Formül: 1->5, 2->4, 3->3, 4->2, 5->1 (Tersleme) -> Sonra x2 ile 1-10 aralığı
        raw_risk_mitigation = int(row['Risk Mitigation'])
        inverted_risk = 6 - raw_risk_mitigation  # 1 ise 5, 5 ise 1 olur
        risk_level = int(inverted_risk * 2)      # 1-5 skalasını 2-10 aralığına taşır
        
        # Madde 4: Agile Effectiveness (1-5) -> x2 ile 1-10 aralığına genişlet
        raw_readiness = int(row['Agile Effectiveness'])
        team_readiness = int(raw_readiness * 2)
        
        # Madde 3: Project Success -> expert_decision mapping
        success_val = row['Project Success']
        expert_decision = "APPROVE" if success_val in [1, True, "Success"] else "REJECT"
        
        scenario_id = f"agile_{index + 1:03d}"
        
        record = {
            "scenario_id": scenario_id,
            "source": "Kaggle Agile Dataset",
            "source_file": "Agile_Projects_Dataset.xlsx",
            "name": f"Agile Project Scenario {index + 1}",
            "description": f"Automated normalization of agile enterprise project tracking data for record {index + 1}.",
            "budget_million_usd": budget,
            "expected_roi_percent": roi,
            "risk_level": risk_level,
            "team_readiness": team_readiness,
            "expert_decision": expert_decision,
            "expert_confidence": 0.85,
            "actual_outcomes": {
                "success": True if expert_decision == "APPROVE" else False,
                "notes": "Historical dataset baseline result."
            },
            "industry": "Technology",
            "scenario_type": "project_management"
        }
        normalized_records.append(record)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_records, f, ensure_ascii=False, indent=2)
    print(f"Başarılı: 200 kayıt Canonical Schema'ya (1-10) göre normalize edildi.")

if __name__ == "__main__":
    normalize_dataset("data/Agile_Projects_Dataset.xlsx", "data/real_datasets/agile_dataset_normalized.json")