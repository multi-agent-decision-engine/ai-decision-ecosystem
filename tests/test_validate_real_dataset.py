import json
import pytest
from scripts.validate_real_dataset import validate_dataset

def test_validate_dataset_with_invalid_data(tmp_path):
    """
    Hatalı veri şemaları girildiğinde kalite kapısının
    doğru şekilde reaksiyon verdiğini doğrular.
    """
    test_file = tmp_path / "invalid_test_dataset.json"
    
    # "source" alanı eklendi, böylece alan kontrolünü geçip risk ölçek kontrolüne odaklanacak
    invalid_data = [{
        "scenario_id": "agile_999",
        "source": "Kaggle Agile Dataset",
        "budget_million_usd": 5.0,
        "expected_roi_percent": 12.5,
        "risk_level": 99,  # Ölçek dışı hatalı değer!
        "team_readiness": 8,
        "expert_decision": "APPROVE"
    }]
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(invalid_data, f)
        
    result = validate_dataset(str(test_file))
    # Kalite kapımız hatalı risk_level'ı yakalayıp False dönmeli
    assert result is False, "Kalite kapısı hatalı risk_level değerini sızdırdı!"

def test_validate_dataset_with_invalid_enum(tmp_path):
    """
    expert_decision alanına geçersiz bir metin girildiğinde yakalandığını test eder.
    """
    test_file = tmp_path / "invalid_enum_dataset.json"
    
    invalid_data = [{
        "scenario_id": "agile_998",
        "source": "Kaggle Agile Dataset",
        "budget_million_usd": 5.0,
        "expected_roi_percent": 10.0,
        "risk_level": 5,
        "team_readiness": 5,
        "expert_decision": "INVALID_DECISION_TEXT"  # Hatalı enum!
    }]
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(invalid_data, f)
        
    result = validate_dataset(str(test_file))
    assert result is False, "Kalite kapısı geçersiz expert_decision değerini onayladı!"