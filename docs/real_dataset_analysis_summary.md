# Real Dataset Analysis Summary

Bu rapor, `scripts/evaluate_real_dataset.py` tarafından otomatik olarak üretilen veri bilimi değerlendirme özetidir.

## Genel Veri Seti İstatistikleri
- **Toplam Senaryo Sayısı:** 200
- **Senaryo Tipi Dağılımı:** Project Management (200 kayıt)

## Veri Dağılım Metrikleri (Ortalamalar)
- **Ortalama Beklenen ROI (%):** %28.77
- **Ortalama Risk Seviyesi (1-5):** 3.62
- **Ortalama Takım Hazır Bulunuşluğu (1-5):** 3.58

## Karar Dağılım Grafiği Özeti
- **APPROVE (Onaylanan Proje Sayısı):** 98
- **REJECT (Reddedilen Proje Sayısı):** 102

## Veri Kalitesi Raporu
- Kaynak veri setinde bütçe bilgisi bulunmadığı için 200 kayıtta `budget_million_usd` alanı `None` olarak işaretlenmiş, veri bütünlüğü şemaya uydurulmuştur. Sistem kararlılığı %100'dır.
