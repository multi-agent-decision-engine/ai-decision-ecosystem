# Real Dataset Analysis Summary (v2 - Updated)

Bu rapor, `scripts/evaluate_real_dataset.py` tarafından otomatik olarak üretilen güncel veri bilimi değerlendirme özetidir.

## Genel Veri Seti İstatistikleri
- **Toplam Senaryo Sayısı:** 200
- **Senaryo Tipi Dağılımı:** Project Management (200 kayıt)

## Geliştirilmiş 1-10 Ölçek Dağılım Metrikleri (Ortalamalar)
- **Ortalama Beklenen ROI (%):** %28.77
- **Ortalama Risk Seviyesi (1-10 Ölçeği):** 3.77 / 10
- **Ortalama Takım Hazır Bulunuşluğu (1-10 Ölçeği):** 7.16 / 10

## Karar Dağılımı
- **APPROVE (Onaylanan Proje Sayısı):** 98
- **REJECT (Reddedilen Proje Sayısı):** 102

## Veri Kalitesi ve Güvenlik Raporu
- Boş olan bütçe alanlarına kurumsal baseline imputation (`5.0 Milyon USD`) uygulanarak veri bütünlüğü tam korumaya alınmıştır. Sınır denetimleri başarıyla tamamlanmıştır.
