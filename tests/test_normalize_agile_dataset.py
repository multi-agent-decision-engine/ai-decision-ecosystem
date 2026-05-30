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
    
    # Gerçek veri seti üzerinden fonksiyonu tetikliyoruz
    normalize_dataset(input_excel, output_json)
    
    # 1. Çıktı dosyası gerçekten üretildi mi?
    assert os.path.exists(output_json), "Normalize edilmiş JSON dosyası üretilemedi!"
    
    with open(output_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert len(data) == 200, "Veri seti eksik veya hatalı sayıda normalize edilmiş."
    
    first_record = data[0]
    
    # 2. Canonical Schema Alan Kontrolleri (Madde 6)
    assert "scenario_id" in first_record
    assert "budget_million_usd" in first_record
    assert "expected_roi_percent" in first_record
    assert "risk_level" in first_record
    assert "team_readiness" in first_record
    assert "expert_decision" in first_record
    
    # 3. Imputation Doğrulaması (Madde 5)
    assert first_record["budget_million_usd"] == 5.0, "Bütçe baseline imputation değeri 5.0 olmalı!"
    
    # 4. 1-10 Ölçek Sınır Doğrulaması (Madde 4)
    for record in data:
        assert 1 <= record["risk_level"] <= 10, "Risk seviyesi 1-10 aralığında olmalı!"
        assert 1 <= record["team_readiness"] <= 10, "Takım hazır bulunuşluğu 1-10 aralığında olmalı!"