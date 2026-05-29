import json
import os
import random

class DatasetLoader:
    def __init__(self, file_path="data/real_datasets/agile_dataset_normalized.json"):
        # Verinin okunacağı varsayılan dosya yolunu içeriye tanımlıyoruz
        self.file_path = file_path
        self.raw_data = []
        
    def load_calibration_data(self):
        """
        Normalize edilmiş JSON verisini okur ve AgentCalibrator'ın
        beklediği eğitim formatına (ground_truth_decision içeren yapıya) dönüştürür.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Eğitim veri seti bulunamadı: {self.file_path}")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

        calibration_ready_list = []
        for record in self.raw_data:
            # Ajan kalibrasyonunun (AgentCalibrator) tam olarak beklediği sözlük yapısı
            calibration_item = {
                "budget_million_usd": record.get("budget_million_usd") or 5.0, # Excel'de bütçe yoksa baseline 5.0 ata
                "expected_roi_percent": float(record.get("expected_roi_percent", 0.0)),
                "risk_level": int(record.get("risk_level", 3)),
                "team_readiness": int(record.get("team_readiness", 3)),
                "ground_truth_decision": record.get("expert_decision", "REJECT"), # Karar alanını kalibrasyon şemasına eşliyoruz
                "expert_confidence": float(record.get("expert_confidence", 0.8))
            }
            calibration_ready_list.append(calibration_item)
        
        return calibration_ready_list
    def train_validation_split(self, data, train_ratio=0.8, seed=42):
        """
        Eğitim verisini belirtilen oranda %80 Train ve %20 Validation (Doğrulama) 
        kümesi olarak ikiye rasgele böler.
        """
        # Her çalıştığında aynı şekilde bölünmesi için sabitleyici (seed) koyuyoruz
        random.seed(seed)
        shuffled_data = data.copy()
        random.shuffle(shuffled_data)

        split_index = int(len(shuffled_data) * train_ratio)
        train_set = shuffled_data[:split_index]
        val_set = shuffled_data[split_index:]

        return train_set, val_set# Kodun yerelde kendi kendini test edebilmesi için minik bir tetikleyici ekleyelim
if __name__ == "__main__":
    loader = DatasetLoader()
    try:
        calib_data = loader.load_calibration_data()
        train, val = loader.train_validation_split(calib_data)
        print(f"Başarılı: Loader tıkır tıkır çalışıyor!")
        print(f"-> Toplam Kalibrasyon Verisi: {len(calib_data)}")
        print(f"-> Eğitim Seti (%80): {len(train)} kayıt")
        print(f"-> Doğrulama Seti (%20): {len(val)} kayıt")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")    