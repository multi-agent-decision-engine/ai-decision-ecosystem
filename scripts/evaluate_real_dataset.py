import json
import os

def evaluate_dataset(json_path: str, output_report_path: str, summary_md_path: str):
    if not os.path.exists(json_path):
        print(f"Hata: Analiz edilecek dosya bulunamadı: {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    total_records = len(data)
    approve_count = sum(1 for r in data if r["expert_decision"] == "APPROVE")
    reject_count = sum(1 for r in data if r["expert_decision"] == "REJECT")
    revise_count = sum(1 for r in data if r["expert_decision"] == "REVISE")
    
    # Gerçek temizlik kontrolü
    missing_budgets = sum(1 for r in data if r.get("budget_million_usd") is None)
    is_clean = True if missing_budgets == 0 and total_records > 0 else False
    
    analysis_results = {
        "total_records": total_records,
        "distribution": {
            "APPROVE": approve_count,
            "REJECT": reject_count,
            "REVISE": revise_count
        },
        "missing_budget_values": missing_budgets,
        "is_clean": is_clean,
        "metrics_summary": {
            "scenario_type": "project_management",
            "industry": "Technology"
        }
    }
    
    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
    # Madde 13: Veri Bilimi Sınırları ve Sınırlamaları Dokümantasyonu (Önemli!)
    os.makedirs(os.path.dirname(summary_md_path), exist_ok=True)
    with open(summary_md_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Real Dataset Analysis Summary

## Veri İstatistikleri ve Genel Dağılım
* **Toplam Senaryo Sayısı:** {total_records}
* **APPROVE Kararı:** {approve_count}
* **REJECT Kararı:** {reject_count}
* **REVISE Kararı:** {revise_count}
* **Eksik Bütçe Değeri:** {missing_budgets} (Imputation uygulandı, tümü 5.0 yapıldı)

## 🚨 Veri Bilimi Sınırlamaları (Limitations)
1. **REVISE Sınıfı Eksikliği:** Orijinal veri seti iki sınıflıdır (APPROVE, REJECT). Karar mekanizmasının `REVISE` sınıfı için bu veri kaynağı kapsamında doğrudan bir ground-truth etiket bulunmamaktadır. Orta skor bölgesi davranışları bu aşamada veriden öğrenilemez.
2. **Sabit Bütçe Dağılımı:** Tüm kayıtlara 5.0 Milyon USD baseline imputation uygulandığı için CFO/CEO ajanlarının bütçe hassasiyeti (budget sensitivity) öğrenimi bu kaynakla sınırlıdır.
3. **Tek Tip Senaryo:** Veri seti yalnızca `project_management` türündedir; dinamik ajan ağırlıklandırması sonraki aşamalarda ek kaynaklarla kalibre edilmelidir.

> **Doğru Çerçeveleme Notu:** Bu PR, real-data ingestion, normalization, validation, ve calibration-ready loader altyapısını hazırlar. Tam ajan kalibrasyonu ve güvenilir performans ölçümü bir sonraki aşamada ek veri kaynaklarıyla tamamlanacaktır.
""")
    print("Başarılı: Güncel analiz raporları ve sınırlamalar dokümanı üretildi!")

if __name__ == "__main__":
    evaluate_dataset(
        "data/real_datasets/agile_dataset_normalized.json",
        "reports/real_dataset_analysis.json",
        "docs/real_dataset_analysis_summary.md"
    )