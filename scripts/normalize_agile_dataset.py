import pandas as pd
import json
import os

def normalize_dataset(file_path, output_path):
    # Bilgisayarındaki Agile Excel dosyasını okuyoruz
    df = pd.read_excel(file_path)
    normalized_data = []

    for index, row in df.iterrows():
        # Takım arkadaşının istediği gibi: 1 ise APPROVE, 0 ise REJECT yapıyoruz
        decision = "APPROVE" if row['Project Success'] == 1 else "REJECT"
        
        # Arkadaşının istediği yeni şemayı (canonical schema) buraya kurduk
        scenario = {
            "scenario_id": f"agile_{index + 1:03d}",
            "source": "Agile",
            "source_file": "Agile_Projects_Dataset.xlsx",
            "name": f"Agile Project Scenario {index + 1:03d}",
            "description": f"Scenario generated based on agile effectiveness score of {row['Agile Effectiveness']}.",
            "budget_million_usd": None,  # Bütçe verisi olmadığı için null bırakıyoruz
            "expected_roi_percent": float(row['Cost Savings (%)']), # Doğru esleme (ROI)
            "risk_level": int(row['Risk Mitigation']),
            "team_readiness": int(row['Agile Effectiveness']),
            "expert_decision": decision,
            "expert_confidence": 0.8,
            "actual_outcomes": {
                "success": bool(row['Project Success'])
            },
            "industry": "Technology",
            "scenario_type": "project_management"
        }
        normalized_data.append(scenario)

    # Çıktı klasörünü oluşturup yeni JSON dosyasını kaydediyoruz
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_data, f, indent=2, ensure_ascii=False)
    print(f"Başarılı: {output_path} dosyası oluşturuldu!")

if __name__ == "__main__":
    # Excel dosyasının yerini ve yeni çıkacak temiz JSON dosyasının yerini belirttik
    normalize_dataset("data/Agile_Projects_Dataset.xlsx", "data/real_datasets/agile_dataset_normalized.json")