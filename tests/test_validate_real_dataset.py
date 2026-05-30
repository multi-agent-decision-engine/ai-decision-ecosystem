import json
import pytest
from scripts.validate_real_dataset import validate_dataset

def test_validate_dataset_with_invalid_data(tmp_path):
    """
    Hatalı veri şemaları girildiğinde kalite kapısının 
    False döndürerek geçişi engellediğini doğrular.
    """
    # Geçici bir klasörde test amaçlı hatalı bir JSON dosyası simüle ediyoruz
    test_file = tmp_path / "invalid_test_dataset.json"
    
    # Senaryo: risk_level alanı 10'dan büyük (Ölçek Hatası - Madde 4)
    invalid_data = [{
        "scenario_id": "agile_999",
        "budget_million_usd": 5.0,
        "expected_roi_percent": 12.5,
        "risk_level": 99,  # Hatalı değer!
        "team_readiness": 8,
        "expert_decision": "APPROVE"
    }]
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(invalid_data, f)
        
    # Kalite kapısı bu veriyi reddetmeli (False dönmeli)
    result = validate_dataset(str(test_file))
    assert result is False, "Kalite kapısı hatalı risk_level değerini sızdırdı!"

def test_validate_dataset_with_invalid_enum(tmp_path):
    """
    expert_decision alanına APPROVE/REJECT/REVISE dışında
    geçersiz bir metin girildiğinde kalite kapısının bunu yakaladığını test eder.
    """
    test_file = tmp_path / "invalid_enum_dataset.json"
    
    invalid_data = [{
        "scenario_id": "agile_998",
        "budget_million_usd": 5.0,
        "expected_roi_percent": 10.0,
        "risk_level": 5,
        "team_readiness": 5,
        "expert_decision": "INVALID_DECISION_TEXT"  # Hatalı enum!
    }]
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(invalid_data, f)
        
    result = validate_dataset(str(test_file))
    assert result is False, "Kalite kapısı geçersiz expert_decision enum değerini onayladı!"