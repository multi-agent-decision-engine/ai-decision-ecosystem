import pytest
import os
from app.domain.learning.dataset_loader import DatasetLoader

def test_dataset_loader_happy_path():
    """
    Mevcut normalize edilmiş gerçek veri setiyle loader'ın 
    doğru çalışıp çalışmadığını test eder (Mutlu Yol).
    """
    loader = DatasetLoader()
    
    # 1. Veri başarıyla yüklendi mi?
    data = loader.load_calibration_data()
    assert isinstance(data, list)
    assert len(data) > 0

    # 2. Şema dönüşümleri doğru yapılmış mı?
    first_item = data[0]
    assert "ground_truth_decision" in first_item
    assert "budget_million_usd" in first_item
    assert isinstance(first_item["risk_level"], int)

    # 3. Veri bölme (split) mekanizması doğru çalışıyor mu?
    train, val = loader.train_validation_split(data, train_ratio=0.8)
    assert len(train) + len(val) == len(data)

def test_dataset_loader_invalid_path():
    """
    Sisteme var olmayan hatalı bir dosya yolu verildiğinde 
    FileNotFoundError hatası fırlatıp fırlatmadığını test eder (Edge Case).
    """
    invalid_loader = DatasetLoader(file_path="data/real_datasets/non_existent_file.json")
    
    with pytest.raises(FileNotFoundError):
        invalid_loader.load_calibration_data()