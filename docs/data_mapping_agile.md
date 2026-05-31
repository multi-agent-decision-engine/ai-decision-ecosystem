# Data Mapping & Normalization Specification (Agile Dataset)

## 1. Kolon ve Alan Eşlemeleri
Aşağıdaki tabloda Kaggle Agile veri seti kolonlarının sistemimizin Canonical Şeması ile olan resmi eşlemeleri yer almaktadır:

| Orijinal Veri Kolonu | Canonical Şema Alanı | Açıklama |
| :--- | :--- | :--- |
| `Project Success` | `expert_decision` / `actual_outcomes.success` | 1/Success ise APPROVE, aksi halde REJECT. |
| `Cost Savings (%)` | `expected_roi_percent` | Doğrudan numeric ROI yüzdesi olarak eşlenmiştir. |
| `Risk Mitigation` | `risk_level` | Ters çevrilerek gerçek risk seviyesine (1-10) dönüştürülmüştür. |
| `Agile Effectiveness` | `team_readiness` | 1-5 skalasından 2-10 skalasına genişletilmiştir. |

## 2. Dönüşüm ve Skala Formülleri
* **Risk Seviyesi (1-10):** Orijinal veri setindeki `Risk Mitigation` bir risk azaltma başarı puanıdır (yüksek olması riskin azaldığını gösterir). Gerçek risk seviyesini bulmak için önce veri terslenmiştir: $\text{inverted\_risk} = 6 - \text{raw\_value}$. Ardından, sistemin kullandığı 1-10 canonical formatına oturtulması amacıyla 2 ile çarpılarak genişletilmiştir: $\text{risk\_level} = \text{inverted\_risk} \times 2$.
* **Takım Hazır Bulunuşluğu (1-10):** Orijinal `Agile Effectiveness` (1-5) verisi sistem şemasına uyum için doğrudan 2 ile çarpılarak 2-10 ölçeğine taşınmıştır.

## 3. Eksik Veri Stratejisi (Imputation)
Orijinal veri setindeki 200 kaydın tamamında `budget_million_usd` alanı boş (None) durumdadır. Sistem mimarisinin çalışması amacıyla tüm senaryolara **Sabit Baseline Imputation (5.0 Milyon USD)** atanmıştır. Bu değer, kurumsal çevik projelerin baseline finansal bütçe medyanı baz alınarak sektörel standartlara göre belirlenmiştir.