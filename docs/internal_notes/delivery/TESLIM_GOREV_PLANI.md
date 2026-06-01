# Teslim Gorev Plani

Bu dokuman, projeyi teslime uygun hale getirmek icin ekip icindeki gorevleri sirali ve sorumlu kisi bazli olarak tanimlar.

Proje: Multi-Agent Decision Engine / AI Decision Ecosystem  
Amaç: Gercek veriyle desteklenen, backend-frontend baglantisi calisan, ajan tartismasi gosterilebilen ve veri bilimi katkisi raporlanabilir bir karar destek sistemi teslim etmek.

## Ekip Sorumluluklari

| Kisi | Ana Sorumluluk | Odak |
|---|---|---|
| Melike | Agent mimarisi ve backend baglanti sozlesmesi | Backend API, agent debate response, Docker/API stabilitesi |
| Helin | Veri bilimi ve veri analizi | Dataset normalization, validation, mapping, evaluation raporu |
| Afgra | Frontend | Gercek API entegrasyonu, debate console, final report UI |

## Melike Gorev Durumu

Durum: KAPANDI (zorunlu kabul kriterleri + nice-to-have maddeleri dahil tamamlandi)

Tamamlanan backend gorevleri:

1. Detailed simulation response schema'lari eklendi.
   - `AgentMessageResponse`
   - `RoundResponse`
   - `SimulationResponse`
2. `/api/v1/scenarios/{id}/simulate` endpoint'i artik round-based detayli response donuyor.
3. Response'a su alanlar eklendi:
   - `rounds`
   - `total_rounds`
   - `consensus_reached`
   - `stability_reached`
   - `scenario_type`
   - `scenario_type_confidence`
   - `agent_weights`
4. Agent mesajlari frontend debate console icin API response'una tasindi.
5. Backend API testleri detailed response sozlesmesine gore guncellendi.
6. `pytest tests/test_api_scenario_get_endpoints.py tests/test_round_based_discussion.py` calistirildi.
7. Backend simulation contract dokumani eklendi:
   - `docs/backend_simulation_contract.md`
8. Docker image yeniden build edildi ve canli endpoint ile dogrulandi.
9. HR round 2 cross-analysis eksigi giderildi.
   - HR artik ikinci turda CEO/CFO goruslerine acik referans veriyor.
   - Canli Docker response'ta HR reasoning icinde `Cross-analysis` dogrulandi.
10. Simulation response schema sertlestirildi.
   - `rounds` bos liste olamaz.
   - `rounds[].messages` bos liste olamaz.
   - `agent_outputs` bos liste olamaz.
   - `agent_weights` sabit `CEO`, `CFO`, `HR` modeliyle doner.
   - `scenario_type` bilinen scenario type degerleriyle sinirlandi.
11. README'ye kisa detailed response snippet'i eklendi.
12. Nice-to-have sertlestirmeler tamamlandi:
    - `AgentMessageResponse.confidence` alani `[0.0, 1.0]` araligina kisitlandi.
    - `SimulationResponse.scenario_type_confidence` alani `[0.0, 1.0]` araligina kisitlandi.
    - OpenAPI schema snapshot testi eklendi (`tests/test_simulation_schema_snapshot.py`):
      - `SimulationResponse`, `RoundResponse`, `AgentMessageResponse`,
        `AgentOutputResponse`, `AgentWeightsResponse` icin `required` ve
        `properties` setleri kilitlendi.
      - `stance`, `final_decision`, `scenario_type` enum degerleri kilitlendi.
      - `rounds`, `agent_outputs`, `messages` icin `minItems: 1` kilitlendi.
      - Frontend sozlesmesi sessizce degisirse CI kirmizi doner.

Test sonucu:

```text
Targeted backend tests: 41 passed
Full test suite: 104 passed
```

Melike icin kalan/dogrulanacak gorevler:

| Oncelik | Gorev | Durum | Not |
|---|---|---|---|
| 1 | Docker image rebuild | Tamamlandi | Kod degisiklikleri container icine alindi |
| 2 | Docker uzerinden live `/simulate` kontrolu | Tamamlandi | Response'ta `rounds`, `scenario_type`, `agent_weights` goruldu |
| 3 | Afgra'ya API contract devri | Hazir | `docs/backend_simulation_contract.md` referans verilecek |
| 4 | README backend endpoint bolumu | Tamamlandi | Contract linki ve response snippet'i eklendi |
| 5 | Agent reasoning kalitesi kontrolu | Tamamlandi | HR dahil round 2 cross-analysis dogrulandi |
| 6 | Nice-to-have: confidence range + OpenAPI snapshot | Tamamlandi | 4 yeni test eklendi, full suite 104 passed |

Melike'nin siradaki uygulama adimlari:

1. Response ornegi Afgra ile paylasilir.
2. Frontend Debate Console `rounds` alanina baglanirken `docs/backend_simulation_contract.md` referans alinir.

## Genel Teslim Hedefi

Teslim tarihinde sistem su sekilde calismali:

1. Docker ile backend ve database sorunsuz calismali.
2. Frontend gercek backend endpointlerine baglanmali.
3. Scenario listesi backend'den gelmeli.
4. Start Simulation butonu gercek ajan simülasyonunu baslatmali.
5. CEO, CFO ve HR ajanlarinin ciktisi UI'da gorunmeli.
6. Ajanlarin round-based tartisma mesajlari backend response'undan alinmali.
7. Final decision, final score ve agent contribution verileri UI'da gosterilmeli.
8. Dataset normalize edilmis ve validation'dan gecmis olmali.
9. Veri mapping ve analiz raporu teslim dokumanlarinda bulunmali.
10. README veya teslim dokumaninda kurulum ve demo akisi acik olmali.

## Oncelik Sirasi

### 1. Backend ve Docker Stabilizasyonu

Sorumlu: Melike

Amac: Backend ve database'in demo sirasinda tek komutla calismasini saglamak.

Yapilacaklar:

1. `docker-compose.yml` ile `ai_decision_app` ve `ai_decision_db` container'larinin birlikte kalktigini kontrol et.
2. `localhost:8000/health` endpoint'inin `200` dondugunu dogrula.
3. `GET /api/v1/scenarios` endpoint'inin database baglantisi ile calistigini dogrula.
4. Local Python backend ile Docker backend'in port cakismasi yaratmadigindan emin ol.
5. Demo icin hangi backend'in kullanilacagini netlestir: Docker backend onerilir.

Kabul kriteri:

```text
GET http://localhost:8000/health -> 200
GET http://localhost:8000/api/v1/scenarios -> 200
```

### 2. Detailed Simulation Response

Sorumlu: Melike

Amac: Frontend'in agent debate console ve karar raporunu gercek backend response'u ile doldurabilmesi.

Yapilacaklar:

1. `app/presentation/schemas/scenario.py` dosyasina detayli response modellerini ekle:
   - `AgentMessageResponse`
   - `RoundResponse`
   - `SimulationDetailResponse`
2. `POST /api/v1/scenarios/{id}/simulate` endpoint'ini detayli response donecek hale getir.
3. Response icine su alanlari ekle:

```text
scenario_id
rounds
total_rounds
consensus_reached
stability_reached
agent_outputs
final_score
final_decision
scenario_type
scenario_type_confidence
agent_weights
```

4. `ScenarioSimulationService.run_simulation()` sonucundaki round bilgilerini route response'una bagla.
5. API testleri ekle veya guncelle.

Kabul kriteri:

```text
POST /api/v1/scenarios/{id}/simulate
```

su bilgileri donmeli:

```json
{
  "scenario_id": 5,
  "rounds": [],
  "total_rounds": 2,
  "consensus_reached": false,
  "stability_reached": true,
  "agent_outputs": [],
  "final_score": 46.0,
  "final_decision": "REJECT",
  "scenario_type": "team_expansion",
  "scenario_type_confidence": 0.61,
  "agent_weights": {
    "CEO": 0.25,
    "CFO": 0.25,
    "HR": 0.5
  }
}
```

### 3. Dataset Schema ve Mapping Temizligi

Sorumlu: Helin

Amac: Real dataset'in proje domain modeliyle uyumlu ve savunulabilir hale getirilmesi.

Yapilacaklar:

1. `data/Agile_Projects_Dataset.xlsx` kolonlarini incele.
2. Kolon mapping kararlarini netlestir:

```text
Project Success      -> expert_decision / actual_outcomes.success
Cost Savings (%)     -> expected_roi_percent
Risk Mitigation      -> risk_level
Agile Effectiveness  -> team_readiness
```

3. `Risk Mitigation` alaninin dogrudan risk mi yoksa risk azaltma skoru mu oldugunu belirle.
4. Gerekirse risk degerini tersle veya 1-10 araligina normalize et.
5. Mapping kararlarini `docs/data_mapping_agile.md` dosyasina yaz.

Kabul kriteri:

```text
docs/data_mapping_agile.md
```

dosyasinda her kaynak kolonun sistemde hangi alana donustugu aciklanmis olmali.

### 4. Dataset Normalization

Sorumlu: Helin

Amac: Agile dataset'i canonical scenario schema'ya tam uyumlu JSON formatina cevirmek.

Yapilacaklar:

1. `scripts/normalize_agile_dataset.py` dosyasini guncelle.
2. Output dosyasini su sekilde uret:

```text
data/real_datasets/agile_dataset_normalized.json
```

3. Her kayitta su alanlar bulunmali:

```text
scenario_id
source
source_file
name
description
budget_million_usd
expected_roi_percent
risk_level
team_readiness
expert_decision
expert_confidence
actual_outcomes
industry
scenario_type
```

4. `COMBINED_DATASET.json` dosyasinin gercekten combined olup olmadigini kontrol et.
5. Sadece Agile verisi varsa teslimde `agile_dataset_normalized.json` ana dataset olarak kullanilsin.

Kabul kriteri:

Normalize script calismali ve canonical schema'ya uygun JSON uretmeli.

```bash
python scripts/normalize_agile_dataset.py
```

### 5. Dataset Validation

Sorumlu: Helin

Amac: Dataset'in otomatik kalite kontrollerinden gecmesini saglamak.

Yapilacaklar:

1. `scripts/validate_real_dataset.py` kapsamni genislet.
2. Su kontrolleri ekle:
   - JSON parse ediliyor mu?
   - Dataset bos degil mi?
   - Required fields var mi?
   - `scenario_id` duplicate degil mi?
   - `risk_level` gecerli aralikta mi?
   - `team_readiness` gecerli aralikta mi?
   - `expected_roi_percent` numeric mi?
   - `expert_decision` sadece `APPROVE`, `REVISE`, `REJECT` degerlerinden biri mi?
   - Missing/null alanlar raporlanabiliyor mu?

Kabul kriteri:

```bash
python scripts/validate_real_dataset.py
```

basariyla calismali ve kac kaydin dogrulandigini yazmali.

### 6. Dataset Analiz Raporu

Sorumlu: Helin

Amac: Veri bilimi katkisini olculebilir ve anlatilabilir hale getirmek.

Yapilacaklar:

1. `scripts/evaluate_real_dataset.py` dosyasini ekle.
2. Su metrikleri hesapla:
   - toplam kayit sayisi
   - karar dagilimi
   - ortalama ROI
   - ortalama risk
   - ortalama team readiness
   - missing value sayisi
   - scenario type dagilimi
3. Ciktiyi su dosyaya kaydet:

```text
reports/real_dataset_analysis.json
```

4. Kisa yorum raporu ekle:

```text
docs/real_dataset_analysis_summary.md
```

Kabul kriteri:

Teslim dokumaninda dataset'in kac kayittan olustugu, karar dagilimi ve veri kalitesi acikca gorunmeli.

### 7. Agent Calibration Hazirligi

Sorumlu: Helin

Amac: Real dataset'i ileride `AgentCalibrator` ile kullanilabilir hale getirmek.

Yapilacaklar:

1. `app/domain/learning/dataset_loader.py` dosyasini ekle.
2. Bu loader su donusumu yapmali:

```text
expert_decision -> ground_truth_decision
```

3. Loader, `AgentCalibrator` icin su formatta veri dondurmeli:

```json
{
  "budget_million_usd": 5.0,
  "expected_roi_percent": 45.0,
  "risk_level": 6,
  "team_readiness": 7,
  "ground_truth_decision": "APPROVE",
  "expert_confidence": 0.8
}
```

4. Train/validation split fonksiyonu ekle.

Kabul kriteri:

`dataset_loader.py` normalize dataset'i okuyup training-ready liste dondurmeli.

### 8. Frontend Gercek API Akisi

Sorumlu: Afra

Amac: UI'nin mock data yerine backend response'u ile calismasi.

Yapilacaklar:

1. Frontend'in `GET /api/v1/scenarios` ile scenario listesini cektigini kontrol et.
2. Scenario dropdown veya liste seciminin dogru calistigini kontrol et.
3. `Start Simulation` butonunun `POST /api/v1/scenarios/{id}/simulate` cagirdigini kontrol et.
4. `agent_outputs`, `final_score`, `final_decision` alanlarini UI'a bagla.
5. Backend kapaliyken error state goster.
6. Scenario yoksa empty state goster.
7. Simulation calisirken loading state goster.

Kabul kriteri:

Frontend acildiginda scenario listesi backend'den gelmeli ve simulation butonu gercek sonucu UI'a basmali.

### 9. Frontend Debate Console

Sorumlu: Afra

Bagimlilik: Melike'nin detailed simulation response gorevi tamamlanmali.

Amac: Ajanlarin kendi aralarinda yaptigi round-based tartismayi UI'da gostermek.

Yapilacaklar:

1. Backend response'undaki `rounds` alanini oku.
2. Her round icin agent mesajlarini listele.
3. Her mesajda su alanlari goster:
   - agent
   - stance
   - confidence
   - reasoning
   - round_number
4. `consensus_reached` ve `stability_reached` bilgisini UI'da goster.
5. Round yoksa anlamli empty state goster.

Kabul kriteri:

Simulation sonrasi UI'da CEO, CFO ve HR ajanlarinin round mesajlari gorunmeli.

### 10. Frontend Final Report

Sorumlu: Afra

Amac: Executive Decision Report panelinin gercek simulation verisinden uretilmesi.

Yapilacaklar:

1. Final report icine secili scenario bilgilerini koy.
2. Agent finding alanlarini `agent_outputs` veya `rounds` verisinden uret.
3. Final score ve final decision alanlarini backend'den al.
4. Copy report ve download report butonlarini dogrula.
5. UI'da hardcoded ornek karar metinleri kalmamasini sagla.

Kabul kriteri:

Report, secili scenario ve gercek simulation sonucu ile uyumlu olmali.

### 11. Entegrasyon Testi

Sorumlu: Melike + Afra

Amac: Backend ve frontend'in birlikte sorunsuz calistigini dogrulamak.

Yapilacaklar:

1. Docker backend ve DB'yi baslat.
2. Frontend'i calistir.
3. Browser'da scenario listesini kontrol et.
4. Bir scenario sec.
5. Simulation baslat.
6. Agent outputs, debate console ve final report alanlarini kontrol et.

Kabul kriteri:

Demo akisi kesintisiz calismali.

### 12. Teslim Dokumantasyonu

Sorumlu: Tum ekip

Amac: Projenin ne yaptigini, nasil calistigini ve ekip katkilarini net anlatmak.

Yapilacaklar:

1. README'ye kurulum adimlarini ekle.
2. Docker ile calistirma adimlarini ekle.
3. Frontend calistirma adimlarini ekle.
4. Veri bilimi katkisini dokumante et.
5. Agent mimarisi ve debate flow'u anlat.
6. Ekip katkilarini kisi bazli yaz.

Kabul kriteri:

Teslim dokumaninda su uc baslik net gorunmeli:

```text
Melike: Agent mimarisi ve backend integration
Helin: Real dataset, validation ve data analysis
Afgra: Frontend cockpit ve backend integration UI
```

## Kisi Bazli Ozet Gorevler

### Melike

1. Docker backend + DB stabilizasyonu
2. `/simulate` detailed response schema
3. Agent rounds response entegrasyonu
4. Scenario classification ve agent weights response'u
5. Backend API testleri
6. Backend endpoint dokumantasyonu

### Helin

1. Agile dataset kolon analizi
2. Data mapping dokumani
3. Normalize dataset uretimi
4. Dataset validation script guncellemesi
5. Dataset analiz/evaluation raporu
6. Agent calibration icin dataset loader hazirligi

### Afgra

1. Scenario list frontend entegrasyonu
2. Start Simulation API entegrasyonu
3. Agent outputs UI
4. Debate Console UI
5. Final Decision ve Executive Report UI
6. Loading, error ve empty state kontrolleri

## Kritik Bagimliliklar

1. Afgra'nin Debate Console'u tamamlamasi icin Melike'nin detailed simulation response'u bitmeli.
2. Learned/calibrated weights entegrasyonu icin Helin'in dataset loader hazirligi bitmeli.
3. Demo icin Melike'nin Docker/API stabilizasyonu once tamamlanmali.
4. Teslim raporu icin Helin'in dataset analysis output'u hazir olmali.

## Teslim Oncesi Kontrol Listesi

- [ ] Docker backend calisiyor. (Canli Docker smoke tekrar kosulacak)
- [ ] Docker database healthy. (Canli Docker smoke tekrar kosulacak)
- [ ] `GET /health` 200 donuyor. (Canli endpoint smoke tekrar kosulacak)
- [ ] `GET /api/v1/scenarios` 200 donuyor. (Canli endpoint smoke tekrar kosulacak)
- [x] `POST /api/v1/scenarios/{id}/simulate` response contract testleri geciyor.
- [x] Simulation response agent output iceriyor.
- [x] Simulation response round/debate bilgisi iceriyor.
- [x] Frontend scenario listesini backend'den cekmek icin `/api/v1/scenarios` kullaniyor.
- [x] Frontend simulation sonucunu gercek `/simulate` API'dan okumaya bagli.
- [x] Debate Console gercek `rounds` verisini okuyacak sekilde kodlandi.
- [x] Dataset normalize edildi.
- [x] Dataset validation script basariyla calisiyor.
- [x] Dataset analiz raporu olustu.
- [x] README kurulum ve demo akisini anlatiyor.
- [x] Ekip katkilari kisi bazli dokumante edildi.

Son dogrulama notu (2026-06-01):

- PR #14 GitHub'da merge edildi ve local `main` `origin/main` ile guncellendi.
- LLM kapali normal backend/test akisi dogrulandi:
  `pytest tests/test_api_scenario_get_endpoints.py tests/test_round_based_discussion.py tests/test_llm_agent_factory.py`
  sonucu `33 passed`.
- LLM acik demo akisi stub client ile dogrulandi:
  `python scripts/demo_llm_reasoning.py`
  base reasoning ile LLM-enriched reasoning farkini gosterdi.
- `MADE_USE_LLM=1` env path'i dogrulandi:
  `AgentFactory` uc ajani `LLMAgent` olarak wrap etti; LLM yaniti gelmediginde sistem base reasoning'e fallback etti.
- Dataset kalite smoke testleri dogrulandi:
  `pytest tests/test_validate_real_dataset.py tests/test_normalize_agile_dataset.py tests/test_dataset_loader.py`
  sonucu `5 passed`.

Canli demo icin kalan manuel kontroller:

1. `docker compose up --build` ile backend + database'i baslat.
2. `GET http://localhost:8000/health` kontrol et.
3. `GET http://localhost:8000/api/v1/scenarios?limit=5&offset=0` kontrol et.
4. `POST http://localhost:8000/api/v1/scenarios/{id}/simulate` kontrol et.
5. Frontend'i browser'da acip scenario listesi, simulation sonucu, debate console ve final report panellerini canli backend ile kontrol et.

## Minimum Teslim Kriterleri

Teslim icin minimum kabul edilebilir seviye:

1. Backend + DB Docker ile calismali.
2. Frontend backend'e baglanmali.
3. En az bir scenario uzerinde simulation calismali.
4. CEO, CFO ve HR ciktisi gorunmeli.
5. Final decision ve final score gorunmeli.
6. Dataset normalize ve validate edilmis olmali.
7. Veri mapping dokumani bulunmali.
8. Demo adimlari README'de yazmali.

## Nice-to-Have Gorevler

Zaman kalirsa:

1. Agent calibrated weights'i simulation servisinde kullanmak.
2. Confusion matrix ve agent accuracy raporu uretmek.
3. Debate quality score hesaplamak.
4. Frontend'de dataset summary paneli eklemek.
5. Export edilebilir detayli simulation report eklemek.
