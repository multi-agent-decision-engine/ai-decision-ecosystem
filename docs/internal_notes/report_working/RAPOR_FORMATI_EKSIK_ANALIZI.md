# Rapor Formati Eksik Analizi

Kaynak format dosyasi: `Yazilim_Muhendisligi_Donem_Projesi_Rapor_Formati.docx.pdf`  
Metin ciktisi: `rapor_formati_extracted.txt`  
Proje: Multi-Agent Decision Engine / AI Decision Ecosystem

Bu dokuman, BMU326 donem projesi rapor formatindaki zorunlu bolumleri mevcut proje icerigiyle eslestirir. Amac, `TESLIM_GOREV_PLANI.md` disinda kalan rapor/kanit eksiklerini netlestirmek ve kimin hangi bolumu tamamlayacagini gostermektir.

## Genel Durum

Proje teknik olarak rapor formatinin buyuk kismini destekliyor:

- Backend: FastAPI, Pydantic, SQLAlchemy Async, PostgreSQL, Alembic
- Frontend: React, Vite, TypeScript, Tailwind
- Mimari: Clean Architecture + Repository Pattern + Dependency Injection + Factory/Strategy benzeri agent yapisi
- Test: pytest, API ve domain testleri, schema snapshot testleri
- Veri: Agile dataset, normalize/validate scriptleri, real-data PR analizi
- Surec: GitHub PR akisi ve Jira/Kanban dokumantasyon taslagi

Ancak resmi rapor teslimi icin teknik kod kadar kanit dokumani da gerekiyor. En kritik eksikler:

1. Jira ekran goruntuleri ve Epic/Story/Task tablosu
2. GitHub repo, branch, commit history, PR review ekran goruntuleri
3. E-R diyagrami ve iliskisel sema tablosu
4. User story / acceptance criteria / functional requirement tablolarinin proje ozelinde yazilmasi
5. Unit test senaryolarinin rapor tablosuna donusturulmesi
6. Veri bilimi katkilarinin rapor formatinin ilgili bolumlerine dagitilmasi
7. Frontend ekran goruntuleri ve demo akisi

## Oncelik Matrisi

| Oncelik | Eksik | Neden Kritik | Sorumlu |
|---|---|---|---|
| P0 | Jira + GitHub ekran goruntuleri | Format acikca ekran goruntusu istiyor | Tum ekip |
| P0 | User story ve gereksinim tablolari | Bolum 2'nin ana teslimi | Melike + Afgra + Helin |
| P0 | E-R diyagrami ve DB semasi | Bolum 6 zorunlu | Melike |
| P0 | Frontend-backend demo ekranlari | Uygulama gelistirme ve ekler icin kanit | Afgra |
| P1 | Test senaryosu tablosu | Bolum 8 zorunlu | Melike |
| P1 | Veri mapping ve dataset analiz ozeti | Veri bilimi katkisini savunur | Helin |
| P1 | Mimari diyagramin rapor gorseline donusturulmesi | Bolum 5.1.1 gorsel istiyor | Melike |
| P2 | Bonus bolumu | Ek puan/profesyonellik | Tum ekip |

## 1. Giris ve Proje Tanimi

### 1.1 Projenin Amaci ve Kapsami

Mevcut kaynak:

- `README.md`
- `docs/PROJECT_TRACKING.md`
- `PROJECT_DOCUMENTATION.md`

Rapora yazilacak proje ozeti:

Multi-Agent Decision Engine, is senaryolarini CEO, CFO ve HR perspektiflerinden degerlendiren bir karar destek sistemidir. Sistem bir senaryonun butce, beklenen ROI, risk ve takim hazirligi bilgilerini alir; ajanlar tur bazli tartisma yapar; final skor ve karar uretir.

Eksik:

- Kapsam disi maddeler net yazilmali.
- Ornek kapsam disi:
  - Gercek sirket finans sistemlerine baglanti yok.
  - Canli kullanici/rol bazli auth bu teslimin ana kapsami degil.
  - LLM/AI ciktisi karar destek amaclidir; nihai karar insan kullaniciya aittir.

Sorumlu: Melike

### 1.2 Hedef Kullanicilar

Eksik tablo yazilmali.

Onerilen kullanici profilleri:

| Kullanici | Rol | Ihtiyac | Beklenti |
|---|---|---|---|
| Yonetici / CEO | Stratejik karar verici | Yatirim kararinin genel etkisini gormek | Final decision, stratejik risk/ROI yorumu |
| Finans sorumlusu / CFO | Butce ve finans kontrolu | ROI, maliyet, risk dengesini izlemek | Finansal skor ve CFO gerekcesi |
| HR / Operasyon yoneticisi | Takim kapasitesi ve uygulanabilirlik | Ekip hazirligi ve kaynak ihtiyacini gormek | HR agent analizi |
| Proje takimi / Analist | Karar surecini analiz eden ekip | Ajan tartismasini ve veri etkisini izlemek | Debate console, rapor ve metrikler |

Sorumlu: Melike + Afgra

### 1.3 Kullanilan Teknolojiler ve Araclar

Mevcut kaynak:

- `README.md`
- `frontend/package.json`
- `requirements.txt`
- `.github/workflows/ci.yml`

Raporda tabloya konacaklar:

| Kategori | Teknoloji / Arac | Aciklama |
|---|---|---|
| Programlama dili | Python, TypeScript | Backend ve frontend gelistirme |
| Backend catisi | FastAPI | REST API ve servis katmani |
| Frontend catisi | React + Vite | Cockpit UI |
| Stil | Tailwind CSS | Frontend tasarim sistemi |
| ORM | SQLAlchemy Async | Repository implementasyonlari |
| Veritabani | PostgreSQL | Kalici senaryo/simulasyon kaydi |
| Migration | Alembic | Sema degisim yonetimi |
| Test | pytest | Unit/integration/schema testleri |
| DevOps | Docker Compose | App + DB container ortami |
| CI/CD | GitHub Actions | PR uzerinde test calistirma |
| Proje yonetimi | Jira Kanban | Gorev takibi |
| AI/Data | Ollama/LangChain, dataset scriptleri | Agent reasoning ve veri hazirligi |

Eksik:

- Rapor icin frontend ekran goruntusu ve paket bilgisi eklenmeli.

Sorumlu: Tum ekip

## 2. Proje Gereksinimleri

### 2.1 User Stories ve Kabul Kriterleri

Eksik: Format proje ozelinde User Story tablosu istiyor. Bu tablo henuz resmi rapor formatina cevrilmemis.

Onerilen user story seti:

| ID | Hikaye Basligi | Kullanici Hikayesi | Kabul Kriterleri |
|---|---|---|---|
| US-01 | Senaryo Listeleme | Bir karar analisti olarak kayitli senaryolari listelemek isterim, boylece analiz edilecek senaryoyu secebilirim. | `GET /api/v1/scenarios` 200 doner; bos liste durumunda UI empty state gosterir; limit/offset desteklenir. |
| US-02 | Senaryo Simulasyonu | Bir yonetici olarak secili senaryoyu simule etmek isterim, boylece CEO/CFO/HR yorumlarini ve final karari gorebilirim. | `POST /simulate` final_score ve final_decision doner; agent_outputs bos olamaz; hata durumlari UI'da gosterilir. |
| US-03 | Ajan Tartismasi | Bir analist olarak ajanlarin tur bazli mesajlarini gormek isterim, boylece karar surecinin gerekcesini anlayabilirim. | Response `rounds` icerir; her round en az bir mesaj icerir; HR round 2 diger ajanlara referans verir. |
| US-04 | Karar Raporu | Bir yonetici olarak simulasyon sonucundan executive report almak isterim, boylece karar ciktisini paylasabilirim. | UI final score, decision, agent findings ve scenario bilgisini gosterir. |
| US-05 | Gercek Dataset Hazirligi | Bir veri bilimci olarak Agile datasetini normalize etmek isterim, boylece ajan performansi ve kalibrasyon icin kullanabilirim. | Normalize JSON uretilir; validation script basarili calisir; mapping dokumani vardir. |

Sorumlu:

- Melike: US-02, US-03 backend kabul kriterleri
- Afgra: US-01, US-04 UI kabul kriterleri
- Helin: US-05 veri kabul kriterleri

### 2.2 Fonksiyonel Gereksinimler

Eksik: Rapor tablosu halinde yazilmali.

Onerilen gereksinimler:

| ID | Gereksinim | Aciklama | Ilgili Story |
|---|---|---|---|
| FR-01 | Senaryo olusturma | API yeni karar senaryosu olusturur. | US-01 |
| FR-02 | Senaryo listeleme | API kayitli senaryolari sayfali doner. | US-01 |
| FR-03 | Simulasyon calistirma | Secili senaryo icin CEO, CFO, HR analizi yapilir. | US-02 |
| FR-04 | Round-based debate | Ajanlar birden fazla turda onceki mesajlara gore yanit uretir. | US-03 |
| FR-05 | Final karar hesaplama | Agent skorlarindan final_score ve final_decision uretilir. | US-02 |
| FR-06 | Scenario classification | Senaryo tipi belirlenir ve agent_weights uretilir. | US-02 |
| FR-07 | Frontend cockpit | Scenario listesi, debate console ve executive report UI'da gosterilir. | US-01, US-03, US-04 |
| FR-08 | Dataset normalize/validate | Agile dataset canonical schema'ya donusturulur ve dogrulanir. | US-05 |

### 2.3 Fonksiyonel Olmayan Gereksinimler

Onerilen tablo:

| ID | Gereksinim | Aciklama |
|---|---|---|
| NFR-01 | Surdurulebilirlik | Clean Architecture ile domain, application, infrastructure ve presentation katmanlari ayrilir. |
| NFR-02 | Test edilebilirlik | Domain ve API davranislari pytest ile dogrulanir. |
| NFR-03 | Sozlesme kararliligi | Pydantic schema ve OpenAPI snapshot testleri frontend kontratini korur. |
| NFR-04 | Calistirilabilirlik | Docker Compose ile backend ve PostgreSQL birlikte calisir. |
| NFR-05 | Kullanilabilirlik | Frontend loading, error ve empty state sunar. |
| NFR-06 | Veri kalitesi | Dataset required field, aralik, duplicate ve karar etiketi kontrollerinden gecer. |

Eksik:

- Afgra frontend durumlarini ekran goruntusuyle kanitlamali.
- Helin veri kalite ciktisini rapora eklemeli.

### 2.4 Is Kurallari ve Kisitlamalar

Mevcut kaynak:

- `README.md`
- `app/domain/services/aggregator.py`
- `app/domain/services/classifier.py`
- `app/presentation/schemas/scenario.py`

Rapora yazilacak kurallar:

- `risk_level` 1-10 araliginda olmalidir.
- `team_readiness` 1-10 araliginda olmalidir.
- `budget_million_usd` pozitif olmalidir.
- Final karar esikleri:
  - `final_score >= 75`: APPROVE
  - `50 <= final_score < 75`: REVISE
  - `final_score < 50`: REJECT
- `scenario_type` sadece bilinen enum degerlerinden biri olabilir.
- `agent_weights` sabit CEO/CFO/HR anahtarlarini tasir.
- `rounds`, `messages`, `agent_outputs` bos donmemelidir.

Eksik:

- Bu kurallar rapor metnine tablo olarak eklenmeli.

Sorumlu: Melike

## 3. Cevik Yazilim Gelistirme Sureci

### 3.1 Epic / Story / Task Hiyerarsisi

Mevcut kaynak:

- `TESLIM_GOREV_PLANI.md`
- `docs/workflow.md`
- Jira board ekranlari ekipte olmali.

Eksik:

- Jira'daki gercek issue key'leriyle tablo doldurulmali.
- Format su kolonlari istiyor: Tip, Anahtar, Ust Oge, Baslik, Baslangic, Bitis, Talimat Veren, Gerceklestiren.

Onerilen epic yapisi:

| Epic | Sorumlu | Kapsam |
|---|---|---|
| Agent Architecture & Simulation Contract | Melike | Backend detailed response, agent debate, schema/test |
| Real Dataset & Calibration Prep | Helin | Dataset mapping, normalize, validate, analysis, loader |
| Decision Cockpit Frontend | Afgra | React cockpit, API integration, report UI |
| Documentation & Delivery | Tum ekip | README, rapor, ekran goruntuleri, demo |

### 3.2 Jira Ekran Goruntuleri

Zorunlu kanitlar:

- Kanban board genel gorunumu: To Do / In Progress / Code Review / Done
- 2-3 Jira kart detay ekrani
- Development panelinde branch, commit, PR baglantisi
- Activity/History sekmesinde durum gecisleri

Eksik:

- Bu ekran goruntuleri repo icinde yok. Rapor icin manuel alinmali.

Sorumlu: Tum ekip

## 4. Surum Kontrolu - Git ve GitHub

### 4.1 GitHub Repository Yapisi

Mevcut repo yapisi rapora uygundur:

| Klasor / Dosya | Aciklama |
|---|---|
| `app/` | Backend kaynak kodu |
| `frontend/` | React/Vite frontend |
| `tests/` | pytest testleri |
| `docs/` | Mimari, workflow, contract ve teslim dokumanlari |
| `data/` | Real dataset dosyalari |
| `scripts/` | Dataset, seed ve validation scriptleri |
| `alembic/` | Migration dosyalari |
| `.github/` | CI ve repo yonergeleri |
| `README.md` | Kurulum, API, mimari ve test bilgisi |

Eksik:

- GitHub repo ana sayfa ekran goruntusu alinmali.

### 4.2 README Dosyasi

Mevcut:

- Proje aciklamasi var.
- Kurulum, Docker, API endpointleri, mimari ve test stratejisi var.
- Backend simulation contract linki var.

Eksik:

- Takim uyeleri bolumu eklenmeli.
- Frontend calistirma adimlari net eklenmeli.
- Guncel test sayisi ve frontend build bilgisi yazilmali.
- Uygulama ekran goruntusu eklenmeli.

Sorumlu: Tum ekip

### 4.3 GitHub Tarafi

Zorunlu kanitlar:

- Commit history ekran goruntusu
- Branches sekmesi
- Pull Requests listesi

Eksik:

- Bunlar lokal dosyadan uretilemez; GitHub arayuzunden alinmali.

Sorumlu: Tum ekip

### 4.4 Pull Request ve Code Review Sureci

Mevcut konu:

- PR #5: real-data Helin
- PR #6: ai-decision-cockpit Afgra
- Melike backend detailed simulation contract degisiklikleri

Eksik:

- 3-4 PR review yorumu, approve/request changes ekran goruntusu alinmali.
- PR aciklamalarina test komutlari ve acceptance criteria eklenmeli.

Sorumlu: Tum ekip

## 5. Yazilim Mimarisi ve Tasarimi

### 5.1 Sistem Mimarisi

Mevcut kaynak:

- `README.md`
- `docs/ARCHITECTURE_DEFENSE.md`
- `docs/PROJECT_TRACKING.md`

Rapora yazilacak mimari:

- Clean Architecture / Layered Architecture
- Presentation: FastAPI routes, Pydantic schemas, React frontend
- Application: use case services
- Domain: entities, agent logic, classifier, aggregator, discussion orchestrator
- Infrastructure: SQLAlchemy repositories, database, LLM/logger integrations

Eksik:

- Rapor icin gorsel mimari diyagram PNG olarak hazirlanmali.

Sorumlu: Melike

### 5.1.1 Mimari Diyagram

Mevcut:

- README icinde Mermaid diyagram var.
- `docs/PROJECT_TRACKING.md` icinde ASCII diyagram var.

Eksik:

- Word raporu icin gorsel olarak kullanilabilecek net PNG/SVG diyagram uretilmeli.

Oneri:

- Mermaid diyagrami GitHub veya Mermaid Live Editor'dan PNG export et.
- Diyagramda frontend'i de ekle: React Cockpit -> FastAPI -> Application -> Domain -> Repository -> PostgreSQL.

### 5.1.2 Katmanlarin Sorumluluklari

Mevcut:

- README'de katman sorumluluk tablosu var.

Eksik:

- Raporda her katmana ornek dosya verilerek aciklanmali.

Sorumlu: Melike

### 5.2 Tasarim Desenleri

Mevcut desenler:

- Repository Pattern
- Dependency Injection
- Factory Pattern
- Strategy benzeri Agent interface

Eksik:

- Her pattern icin kisa kod parcasi secilmeli.

Onerilen kod referanslari:

- Repository: `app/domain/repositories.py`, `app/infrastructure/repositories/scenario_repository.py`
- DI: `app/presentation/dependencies.py`
- Factory: `app/domain/agents/factory.py`
- Strategy/ABC: `app/domain/agents/base.py`

Sorumlu: Melike

## 6. Veritabani Tasarimi ve ORM

### 6.1 E-R Modeli

Mevcut DB modelleri:

- `ScenarioORM`
- `AgentOutputORM`
- `FinalDecisionORM`

Iliskiler:

- Scenario 1-N AgentOutput
- Scenario 1-1 FinalDecision

Eksik:

- E-R diyagrami yok. Rapor icin cizilmeli.

Onerilen ER yapisi:

```text
Scenario
  id PK
  name
  description
  budget_million_usd
  expected_roi_percent
  risk_level
  team_readiness
  created_at

AgentOutput
  id PK
  scenario_id FK -> Scenario.id
  agent_name
  score
  rationale

FinalDecision
  id PK
  scenario_id FK UNIQUE -> Scenario.id
  final_score
  decision
```

Sorumlu: Melike

### 6.2 Iliskisel Sema

Eksik:

- Rapor tablosu olarak yazilmali.

Sorumlu: Melike

### 6.3 ORM Konfigurasyonu ve Entity Siniflari

Mevcut kaynak:

- `app/infrastructure/database/models.py`
- `app/infrastructure/database/session.py`
- `alembic/versions/0001_initial_tables.py`

Eksik:

- Rapora en az bir entity kod parcasi eklenmeli.

Sorumlu: Melike

### 6.4 Tablo Iliskilerinin Modellenmesi

Mevcut:

- SQLAlchemy `relationship`, `ForeignKey`, cascade delete var.

Eksik:

- 1-N ve 1-1 iliski kod ornegi rapora eklenmeli.

Sorumlu: Melike

### 6.5 Migration Yonetimi

Mevcut:

- Alembic dosyalari var.

Eksik:

- Migration sureci raporda aciklanmali: `alembic upgrade head`, migration dosyasi, Docker DB.

Sorumlu: Melike

## 7. Uygulama Gelistirme

### 7.1 Moduller ve Bilesenler

Onerilen modul listesi:

| Modul | Bilesenler | Sorumluluk |
|---|---|---|
| Scenario API | routes, schemas | HTTP istek/yanitlari |
| Scenario Service | application use cases | Simulasyon akisi |
| Agent Layer | CEO, CFO, HR, factory | Ajan analizleri |
| Debate Orchestrator | discussion service | Round-based konusma |
| Classifier | scenario classifier | Scenario type ve weights |
| Persistence | ORM, repositories | DB kayitlari |
| Frontend Cockpit | React panels | Scenario list, debate console, report |
| Data Pipeline | scripts, dataset | Normalize/validate/analyze |

Eksik:

- Frontend bilesenlerinin rapor icin ekran goruntuleri alinmali.

Sorumlu: Afgra + Melike + Helin

### 7.2 API / Servis Katmani

Mevcut:

- `README.md`
- `docs/backend_simulation_contract.md`
- FastAPI docs: `http://localhost:8000/docs`

Rapor endpoint tablosu:

| Method | Endpoint | Yetki | Aciklama |
|---|---|---|---|
| POST | `/api/v1/scenarios` | Anonim/demo | Yeni karar senaryosu olusturur. |
| GET | `/api/v1/scenarios` | Anonim/demo | Senaryo listesini sayfali doner. |
| GET | `/api/v1/scenarios/{id}` | Anonim/demo | Tek senaryo detayini doner. |
| POST | `/api/v1/scenarios/{id}/simulate` | Anonim/demo | Ajan simulasyonunu calistirir. |
| GET | `/api/v1/scenarios/{id}/simulation` | Anonim/demo | Daha onceki simulasyon sonucunu doner. |
| POST | `/api/v1/classify` | Anonim/demo | Senaryo tipini siniflandirir. |
| POST | `/api/v1/weights` | Anonim/demo | Scenario type'a gore agent weights doner. |

Eksik:

- Rapor icin 1 adet request/response JSON ornegi konulmali.

Sorumlu: Melike

### 7.3 Onemli Kod Parcalari

Onerilen 4 kod parcasi:

1. `ScenarioSimulationService.run_simulation` - simulasyon akisi
2. `DiscussionOrchestrator.run_discussion` - ajanlarin tur bazli konusmasi
3. `ScenarioClassifier.classify` - scenario type ve confidence
4. `SqlAlchemyScenarioRepository.create/list/get_by_id` - repository pattern

Eksik:

- Kod parcalari rapor metnine kisa aciklamalariyla eklenmeli.

Sorumlu: Melike

## 8. Birim Test Calismalari

### 8.1 Test Stratejisi

Mevcut:

- pytest testleri var.
- Domain agent testleri, API testleri, schema snapshot testleri var.
- Full test suite son durumda 104 passed olarak raporlandi.

Eksik:

- Rapor icin test stratejisi resmi dille yazilmali.

Sorumlu: Melike

### 8.2 Test Senaryolari

Onerilen tablo:

| ID | Test Edilen Sinif / Metot | Senaryo | Beklenen Sonuc |
|---|---|---|---|
| UT-01 | CEOAgent.analyze | ROI/risk bilgisiyle CEO analizi | AgentMessage doner, skor/stance tutarlidir. |
| UT-02 | CFOAgent.analyze | Finansal risk ve butce analizi | CFO gerekcesi ve metrikleri uretilir. |
| UT-03 | HRAgent.analyze | Team readiness analizi | HR ekip kapasitesi yorumunu uretir. |
| UT-04 | DiscussionOrchestrator | Round 2 mesajlari | Ajanlar onceki mesajlara referans verir. |
| UT-05 | SimulationResponse Schema | Bos rounds/messages engeli | minItems kontrati korunur. |
| UT-06 | Scenario API simulate | Gecerli scenario simulasyonu | Detailed response alanlari doner. |
| UT-07 | ScenarioClassifier | Scenario type belirleme | `scenario_type` None olmaz. |
| UT-08 | OpenAPI snapshot | Response kontrati degisimi | Schema beklenen property/enum setini korur. |

Eksik:

- Test komutu ve ekran ciktisi rapora eklenmeli.
- CI ekran goruntusu varsa eklenmeli.

Sorumlu: Melike

## 9. Bonus Ozellikler

Format bonus bolumunu sadece uygulanan ozellikler icin istiyor.

Yazilabilecek bonuslar:

- Docker Compose ile containerized calisma
- GitHub Actions CI
- React/Vite cockpit frontend
- Round-based multi-agent debate
- Scenario classification ve dynamic agent weights
- Real dataset normalization/validation pipeline
- OpenAPI schema snapshot testleri
- LLM/Ollama destekli reasoning altyapisi mevcutsa kisa aciklama

Eksik:

- Hangi bonuslarin gercekten calistigi net secilmeli; abartili iddia yazilmamali.

Sorumlu: Tum ekip

## 10. Takim Calismasi ve Gorev Dagilimi

Mevcut kaynak:

- `TESLIM_GOREV_PLANI.md`
- `DATA_PR_REVIEW_REAL_DATA_HELIN.md`
- PR #5 ve PR #6 bilgileri

Rapor tablosu:

| Takim Uyesi | Ogrenci No | Temel Rol | Ana Katki |
|---|---|---|---|
| Melike | Yazilacak | Agent mimarisi ve backend integration | Detailed simulation response, schema, API contract, tests, Docker/API dogrulama |
| Helin | Yazilacak | Veri bilimi ve analiz | Agile dataset, mapping, normalization, validation, dataset analysis, calibration hazirligi |
| Afgra | Yazilacak | Frontend | React cockpit, backend API entegrasyonu, debate console, executive report UI |

Eksik:

- Ogrenci numaralari ve resmi ad/soyad bilgileri eklenmeli.
- Her uyeye 3-5 somut dosya/PR katkisi yazilmali.

Sorumlu: Tum ekip

## 11. Sonuc ve Degerlendirme

### 11.1 Kazanimlar

Yazilabilecekler:

- Clean Architecture ile katmanli backend gelistirme
- Async FastAPI + PostgreSQL + SQLAlchemy deneyimi
- Multi-agent reasoning ve debate flow tasarimi
- Frontend-backend sozlesmesi ve API entegrasyonu
- Dataset normalization/validation sureci
- PR/code review ve Kanban sureci

### 11.2 Zorluklar ve Cozumler

Onerilen maddeler:

| Zorluk | Cozum |
|---|---|
| Frontend mock veriden gercek API'ye gecis | `docs/backend_simulation_contract.md` ile response sozlesmesi sabitlendi. |
| Ajanlarin gercek tartisma yaptigini kanitlama | Round-based response ve HR cross-analysis testi eklendi. |
| Response kontratinin frontend'i kirmasi | Pydantic schema sertlestirme ve OpenAPI snapshot testi eklendi. |
| Dataset alanlarini domain modeline map etme | Mapping dokumani ve validation scriptleri planlandi. |
| Docker imajinin eski kodu calistirmasi | Image rebuild ve live endpoint dogrulamasi yapildi. |

### 11.3 Gelecek Calismalar

Onerilenler:

- Agent calibration pipeline'inin real dataset ile tamamlanmasi
- Agent bazli accuracy/confusion matrix raporu
- Frontend'de dataset summary paneli
- Auth/role-based access
- Production deployment
- Export edilebilir PDF/Markdown executive report

Sorumlu: Tum ekip

## 12. Kaynakca ve Ekler

### 12.1 Kaynakca

Eklenebilecek kaynaklar:

- FastAPI documentation
- Pydantic v2 documentation
- SQLAlchemy documentation
- Alembic documentation
- React/Vite documentation
- Tailwind CSS documentation
- Jira/Kanban kaynaklari
- Clean Architecture / Robert C. Martin referansi

Eksik:

- Kaynakca resmi formatta yazilmali.

### 12.2 Ekler

Eklenmesi gerekenler:

- UI ekran goruntuleri
- FastAPI Swagger ekran goruntusu
- Docker Desktop/container ekran goruntusu
- Test sonucu ekran goruntusu
- Jira board ekran goruntusu
- Jira kart detay/history ekran goruntuleri
- GitHub repo/branches/PR ekran goruntuleri
- Mimari diyagram
- E-R diyagram
- Kod parcalari metin olarak

Eksik:

- Eklerin dosya olarak toplanacagi klasor olusturulmali.

Onerilen klasor:

```text
docs/report_assets/
  jira/
  github/
  frontend/
  backend/
  diagrams/
  tests/
```

## Kisi Bazli Aksiyon Listesi

### Melike

1. Rapor bolumleri: 1.1, 2.4, 5, 6, 7.2, 7.3, 8
2. E-R diyagrami hazirla.
3. Mimari diyagrami frontend dahil olacak sekilde gorsellestir.
4. API request/response ornegini rapora koy.
5. Test senaryolari tablosunu ve test ciktisini hazirla.
6. GitHub PR/test kanitlarini ekibe gonder.

### Helin

1. Rapor bolumleri: 2.1 US-05, 2.2 FR-08, 2.3 NFR-06, 7.1 Data Pipeline, 9 bonus data pipeline, 10 katkilar
2. `docs/data_mapping_agile.md` hazirla.
3. Dataset normalize/validate ciktisini rapora uygun ozetle.
4. Veri analiz metriklerini hazirla: kayit sayisi, karar dagilimi, ROI/risk/team readiness ortalamalari, missing value.
5. Calibration pipeline'a baglanma durumunu "tamamlanan" ve "gelecek calisma" diye ayir.

### Afgra

1. Rapor bolumleri: 1.2, 2.1 US-01/US-04, 2.2 FR-07, 7.1 Frontend Cockpit, 9 bonus frontend
2. Frontend calistirma adimlarini README/rapora ekle.
3. Scenario list, simulation, debate console, executive report ekran goruntulerini al.
4. Loading/error/empty state varsa kanitla.
5. UI'nin mock data yerine backend response kullandigini kisaca acikla.

### Tum Ekip

1. Jira ekran goruntulerini tamamla.
2. GitHub branch/commit/PR review ekran goruntulerini tamamla.
3. Kapak bilgilerini doldur: grup no, ogrenci no, ad soyad, repo linki, Jira linki, teslim tarihi.
4. Word icindekiler tablosunu teslimden once guncelle.
5. Ekler klasorunu duzenle ve rapora referansla.

## Minimum Teslim Icin Kapanmasi Gerekenler

Bu maddeler kapanmadan rapor eksik kalir:

- [ ] Kapak bilgileri dolduruldu.
- [ ] User story ve gereksinim tablolari yazildi.
- [ ] Jira Kanban, kart detay ve history ekran goruntuleri eklendi.
- [ ] GitHub repo, branch, commit, PR review ekran goruntuleri eklendi.
- [ ] Mimari diyagram gorsel olarak eklendi.
- [ ] E-R diyagram ve iliskisel sema eklendi.
- [ ] API endpoint tablosu ve JSON ornegi eklendi.
- [ ] Test senaryolari tablosu ve test ciktisi eklendi.
- [ ] Veri bilimi mapping/analysis ozeti eklendi.
- [ ] Frontend ekran goruntuleri eklendi.
- [ ] Takim gorev dagilimi resmi bilgilerle tamamlandi.
- [ ] Kaynakca ve ekler tamamlandi.

