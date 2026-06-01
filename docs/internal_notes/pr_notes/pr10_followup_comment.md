# Takip — PR #10 Güncel Durum Analizi (2026-05-30)

PR #10 güncellendi (9 → 14 dosya, +6621 / -0). Normalize JSON çıktısı, analiz JSON'u, 2 yeni test ve dependency güncellemeleri eklendi. Ancak hem **CI kırık** hem de bu issue'daki **12 maddenin yarısı hâlâ açık**. Aşağıda madde madde gerçek durum ve eklenmesi gereken yeni başlıklar.

---

## 🚨 CI Durumu

Şu an PR #10 testleri yeşil değil.

```
FAILED tests/test_normalize_agile_dataset.py::test_normalize_output_schema_and_scaling
FAILED tests/test_validate_real_dataset.py::test_validate_dataset_with_invalid_data
FAILED tests/test_validate_real_dataset.py::test_validate_dataset_with_invalid_enum
3 failed, 104 passed
```

Kök sebepler:

1. **Normalize testi `assert None == 5.0`** — `scripts/normalize_agile_dataset.py` hâlâ `budget_million_usd: None` üretiyor; budget imputation **normalize aşamasında uygulanmamış**, yalnızca loader'da fallback olarak duruyor.
2. **Validate fixture'larında `source` alanı eksik** — yeni testlerin fixture'ları validate'in zorunlu kıldığı `source` alanını taşımıyor.
3. **`validate_dataset()` `True/False` döndürmüyor** — fonksiyon `assert` ile exception fırlatıyor; test ise `result is False` bekliyor. Test ile production fonksiyonu arasında **sözleşme uyumsuzluğu** var.

---

## Issue Maddelerinin Güncel Skoru

| # | Madde | Durum | Not |
|---|---|---|---|
| 1 | `requirements.txt` | ⚠️ Yarım | `pandas` + `openpyxl` eklendi ✅ ama `fastapi` ve `httpx` **duplicate** olarak (zaten pin'liydi) bir kez daha eklenmiş. Temizlenmeli. |
| 2 | Normalize çıktısı PR'a | ✅ | `agile_dataset_normalized.json` (3802 satır) PR'da. |
| 3 | `docs/data_mapping_agile.md` | ❌ | Hâlâ yaratılmamış. |
| 4 | 1-10 ölçek dönüşümü | ❌ | Commit mesajı *"verified 1-10 scale"* diyor ama normalize hâlâ `int(row['Risk Mitigation'])` (ham 1-5), validate hâlâ `assert 1 <= risk_level <= 5`. **Kodda hiçbir scale dönüşümü yok**. |
| 5 | Budget imputation stratejisi | ⚠️ Yarım | Loader'da `or 5.0` fallback var; normalize çıktısı hâlâ `None`. Doküman yok. |
| 6 | Şema tutarsızlığı | ❌ | `app/data_converter.py` ve `COMBINED_DATASET.json` dokunulmamış; iki ayrı şema hâlâ yan yana. |
| 7 | Validation genişletme | ❌ | Yeni kontrol yok (duplicate id, team_readiness range, ROI numeric, missing raporu). `assert` hâlâ kullanılıyor. Fonksiyon `True/False` döndürmüyor. |
| 8 | `is_clean` mantığı | ❌ | Analiz JSON `is_clean: true, missing_budget_values: 0` diyor; normalize çıktısı hâlâ `None` üretiyorken bu tutarsız. |
| 9 | `DatasetLoader` doğrulama | ⚠️ Yarım | Default path artık çalışır dosyaya işaret ediyor ✅. Ama satır sonu hatası HÂLÂ aynı: `return train_set, val_set# Kodun yerelde...` |
| 10 | Mimari konum | ❌ | `app/data_converter.py` hâlâ `app/` köküne. |
| 11 | Test kapsamı | ⚠️ Yarım | 2 yeni test eklendi (her ikisi de FAILING). `tests/test_dataset_loader.py` YOK. |
| 12 | Kozmetik | ❌ | Trailing whitespace, emoji print'leri ve commit mesajı doğruluğu hâlâ açık. |

---

## Açık Blocker Maddeleri (Detay)

### 1. CI testleri yeşile dönmeli
- `pytest -q` hatasız çalışmalı.
- Yeni testler **gerçekten** geçmeli (`104 passed` yetmez, yeni 2-3 testin de yeşil olması zorunlu).
- Commit mesajlarında *"passing unit tests"* iddiası yalnızca CI çıktısıyla doğrulandıktan sonra yazılmalı.

### 2. `requirements.txt` temizliği
- `fastapi` ve `httpx` zaten pin'li satırlarda var — yeniden eklenmiş versiyonlar kaldırılmalı.
- Aynı paket **hem pin'li hem unpinned** olarak yazılmamalı.
- Yalnızca `pandas` ve `openpyxl` net olarak eklenmiş kalmalı.

### 3. Normalize script ↔ commitlenen JSON tutarlılığı
Şu an `agile_dataset_normalized.json` PR'da ama `scripts/normalize_agile_dataset.py` yeniden çalıştırıldığında **aynı çıktıyı üretmiyor** (çünkü kod hâlâ None ve 1-5 üretiyor).

Gereken:
- Script imputation'ı kendisi yapmalı (`budget_million_usd = 5.0`).
- 1-10 ölçek dönüşümü script'in içinde olmalı.
- Script tekrar çalıştırıldığında:
  ```bash
  python scripts/normalize_agile_dataset.py
  git diff -- data/real_datasets/agile_dataset_normalized.json
  ```
  beklenmeyen fark üretmemeli.

### 4. Veri mapping dokümanı
`docs/data_mapping_agile.md` hâlâ eksik. İçeriği:

```
Project Success      -> expert_decision / actual_outcomes.success
Cost Savings (%)     -> expected_roi_percent
Risk Mitigation      -> risk_level
Agile Effectiveness  -> team_readiness
```

Ek olarak şunlar açıklanmalı:
- `Risk Mitigation` doğrudan risk mi yoksa risk azaltma metriği mi (gerekirse ters çevirme formülü).
- 1-5 → 1-10 dönüşüm formülü.
- `budget_million_usd = 5.0` baseline kararının gerekçesi.

### 5. 1-10 ölçek dönüşümü gerçekten uygulanmalı
- `normalize_agile_dataset.py` içinde dönüşüm açıkça yapılmalı.
- `validate_real_dataset.py` 1-10 aralığı kontrol etmeli.
- Testler 1-10 ölçekle uyumlu olmalı.
- Tüm kayıtlar için: `1 <= risk_level <= 10` ve `1 <= team_readiness <= 10`.

### 6. Budget imputation normalize aşamasında yapılmalı
- Imputation **normalize çıktısında** uygulanmalı, sadece loader fallback'i olmamalı.
- Canonical dataset'te `budget_million_usd` `None` olmamalı.
- Loader fallback'i güvenlik ağı olarak kalabilir.
- Mapping dokümanında karar gerekçelendirilmeli.

### 7. Şema tutarsızlığı (Merge Blocker)

İki ayrı şema yan yana:

| Pipeline | Şema |
|---|---|
| `normalize_agile_dataset.py` (canonical) | `scenario_id`, `budget_million_usd`, `expected_roi_percent`, `risk_level`, `team_readiness`, `expert_decision`, `expert_confidence` |
| `data_converter.py` → `COMBINED_DATASET.json` | `budget`, `risk`, `readiness`, `decision` |

Gereken:
- Tek canonical schema seçilmeli.
- `COMBINED_DATASET.json` ya canonical'a dönüştürülmeli ya PR'dan çıkarılmalı.
- `data_converter.py` ya kaldırılmalı ya **legacy/exploration** olarak işaretlenmeli.
- `Cost Savings (%)` semantik olarak budget değil — bu eşleme yanıltıcı, düzeltilmeli.

### 8. Validation fonksiyonu yeniden tasarlanmalı

`validate_real_dataset.py` hâlâ `assert` tabanlı. Sorunlar:
- `python -O` ile `assert`'ler devre dışı kalır → production'da güvensiz.
- Fonksiyon `True/False` döndürmüyor, testler bunu bekliyor → sözleşme ihlali.
- Hata raporu üretmiyor.

Gereken:
- `validate_dataset(path) -> bool` imzası: başarı `True`, başarısızlık `False`.
- Hata listesi (`errors: list[str]`) döndürülmeli veya log'lanmalı.
- `assert` yerine `if ... return False` veya custom `ValidationError`.
- Eklenmesi gereken kontroller:
  - JSON parse hatası
  - Dataset boşluğu
  - Required fields tamlığı
  - `scenario_id` duplicate
  - `risk_level` 1-10
  - `team_readiness` 1-10
  - `expected_roi_percent` numeric
  - `expert_decision` ∈ {APPROVE, REVISE, REJECT}
  - `budget_million_usd` null değil ve numeric
  - Missing/null alan raporu

### 9. Evaluate çıktısı normalize ile tutarlı olmalı
Şu an `reports/real_dataset_analysis.json`:
```json
{ "missing_budget_values": 0, "is_clean": true }
```

Ama normalize hâlâ `None` üretiyorsa bu sonuç **tekrarlanabilir değil**. Evaluate normalize output ile aynı kaynaktan çalışmalı; `is_clean` ancak gerçekten temizse `true` olmalı.

### 10. `DatasetLoader` düzeltmeleri
- Satır sonu hatası giderilmeli:
  ```python
  return train_set, val_set# Kodun yerelde...   # ← newline eksik, kod yapışmış
  ```
- `tests/test_dataset_loader.py` eklenmeli:
  - Mutlu yol
  - Hatalı path / FileNotFoundError
  - Train/validation split determinizmi (`seed=42` → aynı output)
  - 1-10 ölçekli canonical dataset ile uyum

### 11. Mimari konum düzeltmesi (Merge Blocker)
`app/data_converter.py` Clean Architecture'a aykırı yerde. Şu konumlardan birine taşınmalı:
- `scripts/data_converter.py` (script ise)
- `app/infrastructure/data/data_converter.py` (modül ise)
- Kullanılmıyorsa kaldırılmalı.

Veri pipeline'ında hangi dosyanın **otorite** olduğu şu an belirsiz.

### 12. Test kapsamı tamamlanmalı
- `test_normalize_agile_dataset.py` geçmeli (şu an FAIL).
- `test_validate_real_dataset.py` geçmeli (şu an FAIL).
- `test_dataset_loader.py` eklenmeli.
- Fixture'lar validation schema'sıyla uyumlu olmalı (`source` dahil).
- Hatalı veri testleri exception yerine `False`/error report davranışını doğrulamalı.

---

## 🆕 13. Veri Bilimi Sınırları Dokümante Edilmeli

Mevcut dataset için tespitler:

```
Toplam kayıt:     200
APPROVE:          98
REJECT:           102
REVISE:           0     ← yok
Scenario type:    yalnız project_management
Budget:           tüm kayıtlarda 5.0 (imputation sonrası)
ROI range:        ~10-48
Risk range:       1-7
Team readiness:   4-10
```

`docs/real_dataset_analysis_summary.md` içinde şunlar açıkça yazılmalı:

- Dataset 2 sınıflı (`APPROVE`, `REJECT`); 3 sınıflı karar mekanizmasının (`APPROVE` / `REVISE` / `REJECT`) `REVISE` sınıfı için **bu PR kapsamında doğrudan ground-truth label yoktur**.
- Bu nedenle bu PR **"ajanlar gerçek veriyle tam kalibre edildi"** gibi iddialar kurmamalı. Doğru çerçeveleme:

> Bu PR, real-data ingestion, normalization, validation, analysis ve calibration-ready loader altyapısını hazırlar. Tam ajan kalibrasyonu ve güvenilir performans ölçümü sonraki PR'da, daha çeşitli veri kaynakları ve metriklerle tamamlanacaktır.

- Sınırlamalar dokümante edilmeli:
  - REVISE eksikliği → orta-skor bölgesi davranışı veriden öğrenilemez.
  - Budget sabit (tek değer) → CFO/CEO budget sensitivity öğrenimi sınırlı.
  - Tek scenario_type → dynamic agent weighting öğrenimi sınırlı.

### Bu PR'da REVISE üretilmeli mi?

**Hayır.** Mevcut PR zaten kırık; REVISE eklemek kapsamı büyütür ve yeni tartışma açar. REVISE örnekleri sonraki PR'da şu seçeneklerden biriyle ele alınmalı:

- Ek veri kaynağı (HBS, McKinsey, SEC vs.) ile gerçek REVISE örneklerini getirmek.
- **Kurallı ve dokümante** bir pseudo-label stratejisi (ör. orta-ROI + orta-risk + orta-readiness → REVISE), bu durumda kayıtlar açıkça `derived_label: true` ile işaretlenmeli ve dokümana not düşülmeli:

  > REVISE sınıfı kaynak dataset içinde doğrudan bulunmadığı için rule-based pseudo-label olarak türetilmiştir. Bu etiket gerçek expert label değildir.

- [ ] `docs/real_dataset_analysis_summary.md` içine `REVISE` eksikliği ve diğer sınırlamalar maddesi eklensin.
- [ ] Bu PR kapsamında real dataset 2 sınıflı (`APPROVE`, `REJECT`) olarak ele alınsın; REVISE bu PR'da üretilmesin.
- [ ] 3 sınıflı ajan kalibrasyonu sonraki PR'a bırakılsın (ya yeni kaynak ya açıkça etiketlenmiş pseudo-label).

---

## 🆕 14. Kozmetik ve Süreç Kalitesi
- `git diff --check` temiz olmalı.
- Trailing whitespace temizlenmeli.
- Emoji'li `print` log'ları (`✅❌⚠️🚀`) sadeleştirilmeli (opsiyonel: `logging` modülü).
- **Commit mesajları gerçek durumu yansıtmalı.** Testler geçmiyorken *"passing unit tests"* veya *"All reviewer blockers resolved"* yazılmamalı — bu güveni zedeler ve review'da yanlış sinyal verir.

---

## Kabul Kriterleri

Aşağıdaki komutlar **hatasız** çalışmalı:

```bash
python scripts/normalize_agile_dataset.py
python scripts/validate_real_dataset.py
python scripts/evaluate_real_dataset.py
python app/domain/learning/dataset_loader.py
pytest -q
git diff --check
```

Beklenen dosyalar repoda bulunmalı:

```
data/real_datasets/agile_dataset_normalized.json   (canonical, 1-10 ölçek, budget imputed)
reports/real_dataset_analysis.json                  (script ile yeniden üretilebilir)
docs/real_dataset_analysis_summary.md               (sınırlamalar dahil)
docs/data_mapping_agile.md                          (yeni)
tests/test_dataset_loader.py                        (yeni)
```

---

## Merge Kuralı

> **Bu yorumdaki açık blocker'lar kapanmadan PR #10 merge edilmemeli.**

En kritik bloker'lar:

```
- CI / pytest kırıkları (3 failing test)
- Normalize script ile commit'lenen JSON'un birbirini üretmemesi
- 1-10 ölçek dönüşümünün kodda uygulanmamış olması
- Validation fonksiyonunun assert tabanlı kalması + True/False sözleşmesi ihlali
- Şema tutarsızlığı: data_converter.py vs canonical dataset
- Mapping dokümanının eksikliği
- DatasetLoader testinin eksikliği
- Mimari konum: app/data_converter.py
```

REVISE eksikliği bir **veri bilimi sınırlamasıdır**; bu PR'ı bloke etmez ama açıkça dokümante edilmesi zorunludur ve "tam kalibre edildi" tarzı iddiaları engellemelidir.
