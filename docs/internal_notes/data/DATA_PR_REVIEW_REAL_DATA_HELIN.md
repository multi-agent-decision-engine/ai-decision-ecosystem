# Real Data Branch Review - feature/real-data-helin

Bu dokuman `feature/real-data-helin` branch'inde yapilan data calismasini degerlendirmek, eksikleri netlestirmek ve bundan sonra hangi amacla ilerlenmesi gerektigini anlatmak icin hazirlandi.

## Genel Degerlendirme

Bu branch dogru bir ihtiyaca dokunuyor: projede ajanlarin sadece sentetik veya manuel senaryolarla degil, gercek veri kaynaklarindan turetilen senaryolarla egitilmesi ve test edilmesi hedefleniyor. Bu, `DATA_COLLECTION_SOURCES.md`, `DATA_SCIENCE_FRAMEWORK.md` ve `DATA_SCIENCE_SUMMARY.md` dosyalarinda anlatilan veri bilimi vizyonuyla uyumlu bir yon.

Ancak mevcut branch henuz bu hedefi tam olarak karsilamiyor. Su anki calisma daha cok "Agile datasetinden ilk veri cikarma denemesi" seviyesinde. Bu haliyle merge edilirse proje icine data dosyalari eklenmis olur, fakat bu data henuz training pipeline'a, API'ye veya dokumanlarda anlatilan real-data validation hedeflerine guvenli sekilde baglanmis olmaz.

Bu nedenle branch merge edilmeden once data semasi, kaynak acikligi, dosya temizligi ve kullanilabilirlik tarafinda duzeltmeler yapilmali.

## Bu Branch'te Yapilanlar

Branch asagidaki dosyalari ekliyor:

- `app/data_converter.py`
- `data/Agile_Projects_Dataset.xlsx`
- `data/project-management-risk-analysis-and-prediction.ipynb`
- `data/real_datasets/COMBINED_DATASET.json`
- `data/real_scenarios.json.pub`

Yapilan isin ozeti:

- Agile project dataset repo icine alinmis.
- `app/data_converter.py` ile Excel/CSV kaynaklarindan JSON formatinda veri uretme denemesi yapilmis.
- `data/real_datasets/COMBINED_DATASET.json` icinde 200 kayitlik bir dataset olusturulmus.
- Kayitlarda `source`, `budget`, `risk`, `readiness`, `decision` alanlari bulunuyor.
- Dataset dengeli sayilabilecek bir karar dagilimina sahip:
  - `APPROVE`: 98 kayit
  - `REJECT`: 102 kayit

Bu kisim projenin "gercek veriye gecis" hedefi icin iyi bir baslangic olabilir.

## Mevcut Eksikler ve Problemler

### 1. Dataset proje semasiyla uyumlu degil

Mevcut `COMBINED_DATASET.json` kayitlari su formatta:

```json
{
  "source": "Agile",
  "budget": 26.0,
  "risk": 4,
  "readiness": 4,
  "decision": "APPROVE"
}
```

Fakat projenin domain modeli ve data science dokumanlari daha zengin bir sema bekliyor:

```json
{
  "scenario_id": 1,
  "source": "Agile",
  "name": "...",
  "description": "...",
  "budget_million_usd": 5.0,
  "expected_roi_percent": 35.0,
  "risk_level": 6,
  "team_readiness": 7,
  "expert_decision": "APPROVE",
  "expert_confidence": 0.8,
  "actual_outcomes": {
    "success": true,
    "actual_roi_percent": 30.0
  },
  "industry": "Technology",
  "scenario_type": "project_management"
}
```

Mevcut veri bu semanin yalnizca kucuk bir bolumunu karsiliyor. Ozellikle su alanlar eksik:

- `expected_roi_percent`
- `expert_confidence`
- `actual_outcomes`
- `industry`
- `scenario_type`
- `name`
- `description`
- `budget_million_usd`
- `risk_level`
- `team_readiness`
- `expert_decision`

Bu alanlar olmadigi icin veri su an ajan egitimi icin dogrudan kullanilabilir durumda degil.

### 2. Alan isimleri ve anlamlari net degil

`app/data_converter.py` icinde su mapping yapiliyor:

- `Cost Savings (%)` -> `budget`
- `Risk Mitigation` -> `risk`
- `Agile Effectiveness` -> `readiness`
- `Project Success` -> `decision`

Burada en kritik sorun `Cost Savings (%)` alaninin `budget` olarak kaydedilmesi. Cost saving bir yuzde/fayda metriği olabilir, ama "budget" yani proje butcesi anlamina gelmez. Bu, ileride modeli yanlis egitebilir.

Benzer sekilde `Risk Mitigation` dogrudan `risk` olarak kullanilmis. Risk mitigation degeri yuksekse bu "risk yuksek" mi demek, yoksa "risk iyi azaltildi" mi demek? Bu ayrim netlestirilmeden `risk_level` olarak kullanmak hatali olabilir.

Bu nedenle data mapping tekrar dusunulmeli ve her kolonun neyi temsil ettigi dokumante edilmeli.

### 3. `COMBINED_DATASET.json` ismi su an yaniltici

Dosya adi `COMBINED_DATASET.json`, fakat icindeki tum kayitlar sadece `Agile` kaynagindan geliyor. Finance dosyalari converter icinde bekleniyor ama branch'te yok.

Bu nedenle iki secenek var:

- Gercekten birden fazla kaynak eklenecekse Finance/HBS/SEC/Kaggle gibi kaynaklar da normalize edilip combine edilmeli.
- Sadece Agile verisi kalacaksa dosya adi `agile_dataset_normalized.json` gibi daha durust bir isim olmali.

### 4. `data/real_scenarios.json.pub` dosyasi kaldirilmali

Bu dosya JSON degil. Binary Office/Publisher formatinda gorunuyor. Data klasorunde `.json.pub` gibi bir adla durmasi kafa karistirici ve riskli.

Merge oncesi kaldirilmasi onerilir.

### 5. Notebook cok buyuk ve temizlenmemis

`data/project-management-risk-analysis-and-prediction.ipynb` yaklasik 18 MB boyutunda ve output iceriyor.

Notebook projede kalacaksa:

- Output'lari temizlenmeli.
- Neden gerekli oldugu dokumante edilmeli.
- Mumkunse `notebooks/` gibi ayri bir klasore alinmali.

Eger sadece kaynak/reference olarak kullanildiysa repo icine koymak yerine link veya kaynak bilgisi yeterli olabilir.

### 6. Converter dependency'leri eksik

`app/data_converter.py` `pandas` kullaniyor. Excel okumak icin genelde `openpyxl` da gerekir.

Fakat `requirements.txt` icinde bu dependency'ler yok. Temiz bir ortamda converter calismayabilir.

Eklenmesi gerekenler:

```text
pandas
openpyxl
```

Ya da converter uygulamanin runtime parcasi olmayacaksa `app/` altindan cikarilip `scripts/` altina alinmali ve dependency notu dokumana yazilmali.

### 7. Data validation yok

Olusturulan JSON icin otomatik kontrol yok.

Merge oncesi en azindan su kontrolleri yapan bir script veya test olmali:

- Tum kayitlarda required fields var mi?
- `risk_level` 1-10 araliginda mi?
- `team_readiness` 1-10 araliginda mi?
- `expert_decision` sadece `APPROVE`, `REVISE`, `REJECT` degerlerinden biri mi?
- `source` bos degil mi?
- Kayit sayisi beklenen minimum degeri karsiliyor mu?

### 8. Veri henuz projeye entegre edilmemis

Su an dataset repo icinde var, fakat API, training script veya application service tarafinda kullanildigi gorunmuyor.

Bu nedenle branch'in etkisi su an daha cok "dosya ekleme" seviyesinde. Eger amac real data ile ajanlari egitmekse bir loader/training entegrasyonu gerekir.

## Proje Dokumanlarina Gore Beklenen Hedef

`DATA_COLLECTION_SOURCES.md` su hedefi tarif ediyor:

- Birden fazla real-world kaynak kullanmak:
  - HBS case studies
  - SEC filings
  - Kaggle datasets
  - McKinsey articles
  - Sirket ici anonim veriler
- 100+ kaliteli senaryo cikarmak
- Outcome bilgisi olan veriler toplamak
- Quality score / confidence bilgisi eklemek
- Son dataset'i agent training ve validation icin kullanmak

`DATA_SCIENCE_FRAMEWORK.md` ve `DATA_SCIENCE_SUMMARY.md` ise su egitim formatini bekliyor:

- Scenario input:
  - budget
  - expected ROI
  - risk
  - team readiness
- Ground truth:
  - expert decision
  - expert confidence
  - reasoning
- Outcome:
  - actual ROI
  - completion time
  - success/failure
  - team burnout veya execution sonucu
- Model hedefi:
  - agent accuracy olcmek
  - learned weights uretmek
  - debate kalitesini olcmek
  - real outcome'lardan feedback loop kurmak

Mevcut branch bu hedefin yalnizca baslangic veri toplama kismina dokunuyor. Nihai amac icin sema ve pipeline uyumu gerekiyor.

## Yapilmasi Gerekenler

### A. Dosya temizligi

- `data/real_scenarios.json.pub` kaldirilmali.
- Notebook gerekli degilse kaldirilmali.
- Notebook gerekli ise output'lari temizlenmeli ve `notebooks/` klasorune alinmali.

### B. Canonical dataset semasi belirlenmeli

Tek bir standart JSON semasi belirlenmeli. Onerilen minimum sema:

```json
{
  "scenario_id": "agile_001",
  "source": "Agile",
  "source_file": "Agile_Projects_Dataset.xlsx",
  "name": "Agile project scenario 001",
  "description": "Scenario generated from Agile project metrics.",
  "budget_million_usd": null,
  "expected_roi_percent": 26.0,
  "risk_level": 4,
  "team_readiness": 4,
  "expert_decision": "APPROVE",
  "expert_confidence": 0.7,
  "actual_outcomes": {
    "project_success": true
  },
  "industry": "Project Management",
  "scenario_type": "agile_project"
}
```

Eger bazi alanlar kaynak dataset'te yoksa `null` veya turetilmis deger kullanilabilir, fakat bu durum `mapping_notes` veya dokumanla aciklanmali.

### C. Mapping dokumante edilmeli

Her kaynak kolonun projedeki hangi alana donustugu acikca yazilmali:

```text
Agile_Projects_Dataset.xlsx

Project Success       -> expert_decision / actual_outcomes.project_success
Cost Savings (%)      -> expected_roi_percent veya benefit_percent
Risk Mitigation       -> risk_level icin terslenmis veya normalize edilmis deger
Agile Effectiveness   -> team_readiness
```

Ozellikle `Risk Mitigation` icin karar verilmeli:

- Eger yuksek deger daha iyi mitigation demekse risk dusuk olmalidir.
- Eger yuksek deger risk seviyesi demekse dogrudan kullanilabilir.

Bu netlestirilmeden model egitimi yapilmamali.

### D. Converter yeniden duzenlenmeli

`app/data_converter.py` yerine daha acik bir script onerilir:

```text
app/scripts/normalize_agile_dataset.py
```

Bu script:

- Excel dosyasini okur.
- Canonical semaya cevirir.
- Output olarak `data/real_datasets/agile_dataset_normalized.json` yazar.
- Gerekirse daha sonra `data/real_datasets/COMBINED_DATASET.json` icine merge edilir.

### E. Validation eklenmeli

Onerilen dosya:

```text
app/scripts/validate_real_dataset.py
```

Minimum kontroller:

- JSON parse ediliyor mu?
- Kayit sayisi beklenen aralikta mi?
- Required fields eksiksiz mi?
- Range kontrolleri gecerli mi?
- Karar label'lari gecerli mi?

Test olarak da eklenebilir:

```text
tests/test_real_dataset_schema.py
```

### F. Training entegrasyonu netlestirilmeli

Bu dataset sadece dokumantasyon icin mi, yoksa ajan egitimi icin mi kullanilacak?

Eger ajan egitimi icinse:

- `AgentCalibrator` bekledigi alanlarla uyumlu veri almali.
- `ground_truth_decision` alanina `expert_decision` map edilmeli.
- Train/test split uretilmeli.
- Sonuc raporu kaydedilmeli.

Eger sadece kaynak veri olarak duracaksa:

- Bu durum README veya data dokumaninda acikca yazilmali.
- "Training-ready dataset degildir" notu eklenmeli.

## Onerilen Ilerleme Sirasi

1. `data/real_scenarios.json.pub` dosyasini kaldir.
2. Notebook'u temizle, tasima veya kaldirma karari ver.
3. Agile kolon mapping'ini netlestir.
4. Canonical dataset semasini uygula.
5. Converter'i `normalize_agile_dataset.py` olarak yeniden yaz.
6. `COMBINED_DATASET.json` adini ancak gercekten combine edildiyse kullan.
7. Dataset validation script'i veya testi ekle.
8. `requirements.txt` icine gerekli dependency'leri ekle.
9. Dataset'i training pipeline'a bagla veya "source-only" olarak dokumante et.
10. PR aciklamasini gercek duruma gore guncelle.

## PR Merge Kriterleri

Bu branch su kosullar saglanmadan merge edilmemeli:

- Data klasorunde yanlis/binary/ilgisiz dosya kalmamali.
- Dataset semasi proje modelleriyle uyumlu olmali.
- Converter temiz ortamda calisabilmeli.
- Dataset validation gecmeli.
- `git diff --check` temiz olmali.
- PR aciklamasi "ne eklendi, nasil test edilir, data hangi amacla kullanilir" sorularini cevaplamali.

## Nihai Amac

Bu calismanin nihai amaci sadece repo icine veri dosyasi eklemek degil.

Asil amac:

- Gercek kaynaklardan toplanmis is/proje kararlarini standart bir senaryo formatina donusturmek.
- Bu senaryolari CEO, CFO ve HR ajanlarinin karar kalitesini olcmek icin kullanmak.
- Ajan agirliklarini gercek veya gercege yakin outcome verileriyle kalibre etmek.
- Multi-agent debate mekanizmasinin daha dogru, daha aciklanabilir ve daha olculebilir kararlar uretmesini saglamak.

Bu yuzden data calismasi su soruya cevap vermeli:

> "Bu dataset ajanlarin daha iyi karar vermesini nasil sagliyor ve bunu nasil olcuyoruz?"

Branch bundan sonraki adimda bu soruya teknik olarak cevap verecek hale getirilmeli.

