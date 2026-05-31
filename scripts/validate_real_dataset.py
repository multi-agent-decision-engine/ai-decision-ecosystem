import sys
import json
import os

def validate_dataset(json_path: str) -> bool:
    if not os.path.exists(json_path):
        print(f"Hata: Dosya bulunmadi -> {json_path}")
        return False
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Hata: JSON parse hatasi -> {e}")
        return False
        
    if not isinstance(data, list) or len(data) == 0:
        print("Hata: Dataset bos veya liste yapisinda degil!")
        return False
        
    required_fields = ["scenario_id", "source", "expected_roi_percent", "risk_level", "team_readiness", "expert_decision", "budget_million_usd"]
    valid_decisions = ["APPROVE", "REJECT", "REVISE"]
    seen_ids = set()
    errors = []
    
    for record in data:
        scen_id = record.get("scenario_id", "UNKNOWN_ID")
        
        # 1. Duplicate ID Kontrolü
        if scen_id in seen_ids:
            errors.append(f"Duplicate scenario_id tespit edildi: {scen_id}")
        seen_ids.add(scen_id)
        
        # 2. Zorunlu Alan Kontrolleri (Field Var mı ve Null değil mi?)
        for field in required_fields:
            if field not in record or record[field] is None:
                errors.append(f"{scen_id}: Zorunlu alan eksik veya NULL -> {field}")
                
        # 3. Risk Level Null Sızıntısı ve Aralık Kontrolü (Bulgu 1 Düzeltmesi)
        risk = record.get("risk_level")
        if risk is None:
            errors.append(f"{scen_id}: risk_level degeri NULL olamaz!")
        elif not isinstance(risk, int):
            errors.append(f"{scen_id}: risk_level degeri tamsayi (int) olmali!")
        elif not (1 <= risk <= 10):
            errors.append(f"{scen_id}: risk_level 1-10 araliginin disinda -> {risk}")
            
        # 4. Team Readiness Null Sızıntısı ve Aralık Kontrolü (Bulgu 1 Düzeltmesi)
        readiness = record.get("team_readiness")
        if readiness is None:
            errors.append(f"{scen_id}: team_readiness degeri NULL olamaz!")
        elif not isinstance(readiness, int):
            errors.append(f"{scen_id}: team_readiness degeri tamsayi (int) olmali!")
        elif not (1 <= readiness <= 10):
            errors.append(f"{scen_id}: team_readiness 1-10 araliginin disinda -> {readiness}")
            
        # 5. Budget Tip ve Numeric Kontrolü (Bulgu 1 Düzeltmesi)
        budget = record.get("budget_million_usd")
        if budget is None:
            errors.append(f"{scen_id}: budget_million_usd degeri NULL olamaz!")
        elif not isinstance(budget, (int, float)):
            errors.append(f"{scen_id}: budget_million_usd degeri sayisal (numeric) olmali!")
            
        # 6. ROI Numeric Kontrolü
        roi = record.get("expected_roi_percent")
        if roi is not None and not isinstance(roi, (int, float)):
            errors.append(f"{scen_id}: expected_roi_percent sayisal degil!")
            
        # 7. Enum Kontrolü
        if record.get("expert_decision") not in valid_decisions:
            errors.append(f"{scen_id}: Gecersiz expert_decision degeri -> {record.get('expert_decision')}")

    if errors:
        print(f"Kalite Kapisi Basarisiz! Toplam {len(errors)} hata bulundu:")
        for err in errors[:5]:  # Ilk 5 hatayi göster
            print(f"  - {err}")
        return False
        
    print(f"Basarili: Veri kalitesi doğrulandi. {len(data)} kaydin tamami 1-10 Canonical Semasina %100 uygundur.")
    return True

if __name__ == "__main__":
    success = validate_dataset("data/real_datasets/agile_dataset_normalized.json")
    if not success:
        sys.exit(1)