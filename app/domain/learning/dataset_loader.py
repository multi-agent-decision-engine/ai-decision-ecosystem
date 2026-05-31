import json
import os
import random

class DatasetLoader:
    def __init__(self, file_path="data/real_datasets/agile_dataset_normalized.json"):
        # Varsayılan dosya yolunun mevcut doğru adresi göstermesini sağladık (Madde 9)
        self.file_path = file_path
        self.raw_data = []

    def load_calibration_data(self):
        """
        Normalize edilmiş JSON verisini okur ve AgentCalibrator'ın
        beklediği eğitim formatına dönüştürür.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Eğitim veri seti bulunamadı: {self.file_path}")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

        calibration_ready_list = []
        for record in self.raw_data:
            calibration_item = {
                "budget_million_usd": record.get("budget_million_usd") or 5.0,
                "expected_roi_percent": float(record.get("expected_roi_percent", 0.0)),
                "risk_level": int(record.get("risk_level", 3)),
                "team_readiness": int(record.get("team_readiness", 3)),
                "ground_truth_decision": record.get("expert_decision", "REJECT"),
                "expert_confidence": float(record.get("expert_confidence", 0.85))
            }
            calibration_ready_list.append(calibration_item)
        
        return calibration_ready_list

    def train_validation_split(self, data, train_ratio=0.8, seed=42):
        """
        Eğitim verisini belirtilen oranda Train ve Validation kümesi olarak ikiye böler.
        """
        random.seed(seed)
        shuffled_data = data.copy()
        random.shuffle(shuffled_data)

        split_index = int(len(shuffled_data) * train_ratio)
        train_set = shuffled_data[:split_index]
        val_set = shuffled_data[split_index:]

        return train_set, val_set

# Adım 8'deki test dosyasının (test_dataset_loader.py) bağımlılığını doğrudan karşılamak için
# Sınıf dışından çağrılabilen global bir fonksiyon köprüsü ekliyoruz (Mühendisin tam istediği standart)
def load_calibration_data(file_path, split_ratio=0.8):
    loader = DatasetLoader(file_path=file_path)
    calib_data = loader.load_calibration_data()
    return loader.train_validation_split(calib_data, train_ratio=split_ratio)

if __name__ == "__main__":
    loader = DatasetLoader()
    try:
        calib_data = loader.load_calibration_data()
        train, val = loader.train_validation_split(calib_data)
        print("Başarılı: Loader tıkır tıkır çalışıyor!")
        print(f"-> Toplam Kalibrasyon Verisi: {len(calib_data)}")
        print(f"-> Eğitim Seti (%80): {len(train)} kayıt")
        print(f"-> Doğrulama Seti (%20): {len(val)} kayıt")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")