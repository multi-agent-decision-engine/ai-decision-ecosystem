import os
import json
import pytest
from scripts.normalize_agile_dataset import normalize_dataset

def test_normalize_output_schema_and_scaling():
    input_excel = "data/Agile_Projects_Dataset.xlsx"
    output_json = "data/real_datasets/agile_dataset_normalized.json"
    
    # Normalize motorunu tetikle
    normalize_dataset(input_excel, output_json)
    
    # Dosya oluştu mu?
    assert os.path.exists(output_json), "JSON ciktisi uretilemedi!"
    
    with open(output_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert len(data) == 200, "Veri sayisi hatali!"
    first_record = data[0]
    
    # Şema alan kontrolü
    assert "scenario_id" in first_record
    assert "source" in first_record
    assert "risk_level" in first_record
    assert "team_readiness" in first_record
    
    # 1-10 ölçek doğrulaması
    for record in data:
        assert 1 <= record["risk_level"] <= 10, "Risk level 1-10 arasinda olmali!"
        assert 1 <= record["team_readiness"] <= 10, "Team readiness 1-10 arasinda olmali!"
        assert record["budget_million_usd"] == 5.0, "Budget imputation hatali!"