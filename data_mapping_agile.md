# Agile Dataset Mapping & Normalization Documentation (v2 - Updated)

Bu doküman, `data/Agile_Projects_Dataset.xlsx` kaynak dosyasındaki ham verilerin, yapay zeka ajanlarının ortak karar mekanizmasında (Canonical Domain Schema) kullanılmak üzere hangi mühendislik mantığıyla dönüştürüldüğünü açıklar.

## Kolon Eşleme Tablosu (Mapping Matrix)

| Kaynak Kolon (Excel) | Hedef Alan (JSON/Domain) | Veri Tipi | Dönüşüm Mantığı & Ölçeklendirme Gerekçesi |
| :--- | :--- | :--- | :--- |
| `Project Success` | `expert_decision` / `actual_outcomes.success` | `String` / `Boolean` | `1` değerleri `"APPROVE"` (True), `0` değerleri `"REJECT"` (False) olarak map edilmiştir. |
| `Cost Savings (%)` | `expected_roi_percent` | `Float` | Projenin finansal getiri yüzdesini doğrudan temsil eder. |
| `Risk Mitigation` | `risk_level` | `Integer` | **Kritik Ölçekleme & Tersleme:** Kaynak verideki 1-5 skalası, sistem anayasasına uyum için lineer olarak 1-10 skalasına genişletilmiştir. Ek olarak, kaynak kolon riskin kendisini değil "riski azaltma başarısını" ölçtüğü için, yüksek skorlar düşük riske denk gelmektedir. Sistem bütünlüğü için değer terslenmiştir: $risk\_level = 11 - (ham\_deger \times 2)$. |
| `Agile Effectiveness` | `team_readiness` | `Integer` | **Kritik Ölçekleme:** Takımın çevik metotları uygulama başarısı (1-5 arası), sistemin kullandığı 1-10 ölçeğine lineer olarak dönüştürülmüştür: $team\_readiness = ham\_deger \times 2$. |

## Eksik Veri (Missing Data / Imputation) Stratejisi

- **`budget_million_usd`:** Kaynak Excel dosyasında geçmiş projelere ait ham bütçe miktarı yer almamaktadır. Yapay zeka ajanlarının karar destek algoritmalarında matematiksel olarak sıfıbölme hatası (division by zero) veya null pointer hatası almasını engellemek adına **Sabit Baseline Imputation** stratejisi seçilmiştir. Tüm senaryolara kurumsal projelerin baseline ortalamasını temsil eden **`5.0` (5 Milyon USD)** değeri atanmıştır.

## Şema Bütünlüğü ve Tutarsızlık Çözümü
`app/data_converter.py` içindeki eski deneysel şema tamamen devredışı bırakılmış ve geçersiz sayılmıştır. Sistemde tek ve mutlak anayasa olarak `scripts/normalize_agile_dataset.py` tarafından üretilen **Canonical Scenario Schema** seçilmiştir.