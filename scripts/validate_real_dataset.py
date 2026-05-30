import json
import os

def validate_dataset(file_path):
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı! Önce normalize scriptini çalıştırın.")
        return False

    # 1. JSON Parse Edilebiliyor mu? Kontrolü
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Kritik Hata: JSON dosyası parse edilemedi! Detay: {e}")
        return False

    # 2. Dataset Boş mu? Kontrolü
    if not data or len(data) == 0:
        print("Hata: Veri seti boş!")
        return False

    errors = []
    seen_ids = set()
    required_fields = [
        "scenario_id", "budget_million_usd", "expected_roi_percent", 
        "risk_level", "team_readiness", "expert_decision"
    ]
    valid_decisions = {"APPROVE", "REVISE", "REJECT"}

    # 3. Her bir kaydı tek tek kurumsal kurallara göre denetliyoruz
    for index, record in enumerate(data):
        s_id = record.get("scenario_id", f"UNKNOWN_INDEX_{index}")
        
        # Required Fields (Zorunlu Alanlar Var mı?) Kontrolü
        for field in required_fields:
            if field not in record:
                errors.append(f"[{s_id}] Eksik Alan: '{field}' alanı bulunamadı.")

        # Duplicate ID (Mükerrer scenario_id) Kontrolü
        if s_id in seen_ids:
            errors.append(f"[{s_id}] Duplicate Hata: Bu scenario_id veri setinde birden fazla var!")
        seen_ids.add(s_id)

        # Risk Seviyesi Ölçek Kontrolü (Artık 1-10 Arası Olmalı)
        risk = record.get("risk_level")
        if isinstance(risk, int):
            if not (1 <= risk <= 10):
                errors.append(f"[{s_id}] Ölçek Hatası: risk_level ({risk}) 1-10 aralığının dışında!")
        elif risk is not None:
            errors.append(f"[{s_id}] Tip Hatası: risk_level bir tam sayı (integer) olmalı.")

        # Takım Hazır Bulunuşluğu Ölçek Kontrolü (Artık 1-10 Arası Olmalı)
        readiness = record.get("team_readiness")
        if isinstance(readiness, int):
            if not (1 <= readiness <= 10):
                errors.append(f"[{s_id}] Ölçek Hatası: team_readiness ({readiness}) 1-10 aralığının dışında!")
        elif readiness is not None:
            errors.append(f"[{s_id}] Tip Hatası: team_readiness bir tam sayı (integer) olmalı.")

        # ROI Sayısal mı? Kontrolü
        roi = record.get("expected_roi_percent")
        if not isinstance(roi, (int, float)):
            errors.append(f"[{s_id}] Tip Hatası: expected_roi_percent sayısal (numeric) olmalı.")

        # Expert Decision Geçerli bir Enum mı? Kontrolü
        decision = record.get("expert_decision")
        if decision not in valid_decisions:
            errors.append(f"[{s_id}] Değer Hatası: expert_decision '{decision}' olamaz. Sadece APPROVE, REVISE, REJECT geçerlidir.")

    # 4. Sonuçların Raporlanması (Missing/Null alan raporu dahil)
    if errors:
        print(f"⚠️ Doğrulama Başarısız! Toplam {len(errors)} adet kalite hatası bulundu:")
        for err in errors[:10]:  # Terminali boğmamak için ilk 10 hatayı gösterelim
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... ve {len(errors) - 10} adet daha hata var.")
        return False
    else:
        print(f"Başarılı: Veri kalitesi doğrulandı. {len(data)} kaydın tamamı 1-10 Canonical Şemasına %100 uygundur.")
        return True

if __name__ == "__main__":
    validate_dataset("data/real_datasets/agile_dataset_normalized.json")