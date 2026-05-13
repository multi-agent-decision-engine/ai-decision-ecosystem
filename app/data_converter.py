import pandas as pd
import json
import os

def csv_to_json():
    combined_data = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(current_dir) if "app" in current_dir else current_dir

    # DOSYA LİSTESİ (İsimleri senin klasörüne göre esnek tuttum)
    files = [
        {"name": "Agile_Projects_Dataset.xlsx", "type": "excel", "source": "Agile"},
        {"name": "Corporate_Financial_Risk_Assessment_Data.csv", "type": "csv", "source": "Finance"},
        {"name": "Corporate_Financial_Risk_Assessment_Data.xlsx", "type": "excel", "source": "Finance"}
    ]

    for f_info in files:
        f_path = os.path.join(base_path, "data", f_info["name"])
        
        if os.path.exists(f_path):
            try:
                if f_info["type"] == "excel":
                    df = pd.read_excel(f_path)
                else:
                    df = pd.read_csv(f_path)
                
                print(f"✅ {f_info['source']} dosyası okundu: {f_info['name']}")
                
                for _, row in df.iterrows():
                    if f_info["source"] == "Agile":
                        combined_data.append({
                            "source": "Agile",
                            "budget": float(row.get('Cost Savings (%)', 0)),
                            "risk": int(row.get('Risk Mitigation', 5)),
                            "readiness": int(row.get('Agile Effectiveness', 7)),
                            "decision": "APPROVE" if str(row.get('Project Success')) == '1' else "REJECT"
                        })
                    else: # Finance Verisi
                        combined_data.append({
                            "source": "Finance",
                            "budget": float(row.get('Total_Assets', 0) / 1000000),
                            "risk": int(row.get('Financial_Risk_Label', 5)),
                            "readiness": 7,
                            "decision": "REJECT" if row.get('Financial_Risk_Label') == 1 else "APPROVE"
                        })
            except Exception as e:
                print(f"❌ {f_info['name']} işlenirken hata: {e}")
        else:
            print(f"⚠️ UYARI: {f_info['name']} klasörde bulunamadı.")

    # KAYDETME
    if combined_data:
        output_path = os.path.join(base_path, "data", "real_datasets", "COMBINED_DATASET.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=4, ensure_ascii=False)
        print(f"\n🚀 BAŞARILI! Toplam {len(combined_data)} veri birleştirildi.")