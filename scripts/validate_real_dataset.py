import json

def validate_dataset(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert len(data) > 0, "Dataset boş olamaz!"
    
    # Projenin beklediği zorunlu alanlar
    required_fields = ["scenario_id", "source", "expected_roi_percent", "risk_level", "team_readiness", "expert_decision"]
    valid_decisions = ["APPROVE", "REJECT", "REVISE"]

    for record in data:
        # 1. Alan kontrolü
        for field in required_fields:
            assert field in record, f"{record.get('scenario_id')}: {field} alanı eksik!"
        
        # 2. Değer aralığı kontrolü (Excel'deki veriler 1-5 arası)
        assert 1 <= record["risk_level"] <= 5, f"Risk seviyesi 1-5 arasında olmalı: {record['risk_level']}"
        assert record["expert_decision"] in valid_decisions, f"Geçersiz karar: {record['expert_decision']}"

    print(f"Mükemmel! {len(data)} adet kayıt doğrulama testinden başarıyla geçti.")

if __name__ == "__main__":
    validate_dataset("data/real_datasets/agile_dataset_normalized.json")