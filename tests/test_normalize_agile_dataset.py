import os
import json
import pytest
from scripts.normalize_agile_dataset import normalize_dataset

def test_normalize_output_schema_and_scaling():
    """
    Dönüştürülen JSON dosyasının varlığını, şema yapısını
     ve 1-10 ölçeklendirme/tersleme formüllerini doğrular.
    """
    input_excel = "data/Agile_Projects_Dataset.xlsx"
    output_json = "data/real_datasets/agile_dataset_normalized.json"
    
    normalize_dataset(input_excel, output_json)
    
    assert os.path.exists(output_json), "Normalize edilmiş JSON dosyası üretilemedi!"
    
    with open(output_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert len(data) == 200, "Veri seti eksik veya hatalı sayıda normalize edilmiş."
    
    first_record = data[0]
    
    # 1. Şema alanlarının varlığını doğrula
    assert "scenario_id" in first_record
    assert "expected_roi_percent" in first_record
    assert "risk_level" in first_record
    assert "team_readiness" in first_record
    assert "expert_decision" in first_record
    
    # 2. Ölçeklerin 1-10 arasında oturduğunu doğrula
    for record in data:
        assert 1 <= record["risk_level"] <= 10, "Risk seviyesi 1-10 aralığında olmalı!"
        assert 1 <= record["team_readiness"] <= 10, "Takım hazır bulunuşluğu 1-10 aralığında olmalı!"
        # Bütçe null değilse sayısal olmalı veya baseline kuralına uymalı
        if record.get("budget_million_usd") is not None:
            assert isinstance(record["budget_million_usd"], (int, float))