<div align="center">

# AI Decision Ecosystem Engine

### Çok Ajanlı Karar Destek ve Senaryo Değerlendirme Sistemi

Kurumsal karar senaryolarını CEO, CFO ve HR bakış açılarıyla analiz eden;
deterministik karar motorunu, veri bilimi katmanını ve isteğe bağlı yerel LLM
açıklama desteğini aynı mimaride birleştiren yazılım mühendisliği projesi.

**Hızlı bağlantılar**

[Proje Yol Haritası](docs/project/ROADMAP.md) |
[API Sözleşmesi](docs/backend_simulation_contract.md) |
[Veri Bilimi](docs/data_science/DATA_SCIENCE_OVERVIEW.md) |
[Rapor Taslağı](docs/report/final_report_draft.md) |
[Hızlı Başlangıç](QUICKSTART.md)

**Proje**

![status](https://img.shields.io/badge/status-active-brightgreen)
![scope](https://img.shields.io/badge/scope-academic%20project-blue)
![architecture](https://img.shields.io/badge/architecture-clean%20architecture-orange)
![decision](https://img.shields.io/badge/decision-approve%20%7C%20revise%20%7C%20reject-informational)

**Teknoloji**

![python](https://img.shields.io/badge/python-3.11-blue)
![fastapi](https://img.shields.io/badge/backend-FastAPI-009688)
![react](https://img.shields.io/badge/frontend-React%20%2B%20TypeScript-149ECA)
![postgresql](https://img.shields.io/badge/database-PostgreSQL-336791)
![docker](https://img.shields.io/badge/container-Docker%20Compose-2496ED)
![llm](https://img.shields.io/badge/LLM-Ollama%20optional-purple)

**Kalite**

![tests](https://img.shields.io/badge/tests-pytest-brightgreen)
![api](https://img.shields.io/badge/API-OpenAPI-lightgrey)
![orm](https://img.shields.io/badge/ORM-SQLAlchemy-red)
![migrations](https://img.shields.io/badge/migrations-Alembic-yellow)
![frontend-build](https://img.shields.io/badge/frontend%20build-Vite-blueviolet)

</div>

---

## İçindekiler

- [Özet](#özet)
- [Yönetici Özeti](#yönetici-özeti)
- [Problem ve Çözüm](#problem-ve-çözüm)
- [Mevcut Uygulama Durumu](#mevcut-uygulama-durumu)
- [Sistem Mimarisi](#sistem-mimarisi)
- [Karar Akışı](#karar-akışı)
- [Agent Rolleri](#agent-rolleri)
- [Teknoloji Yığını](#teknoloji-yığını)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Hızlı Başlangıç](#hızlı-başlangıç)
- [LLM Modu](#llm-modu)
- [API Özeti](#api-özeti)
- [Veri Bilimi Katmanı](#veri-bilimi-katmanı)
- [Test ve Doğrulama](#test-ve-doğrulama)
- [Repo Yapısı](#repo-yapısı)
- [Dokümantasyon Haritası](#dokümantasyon-haritası)
- [Bilinen Sınırlamalar](#bilinen-sınırlamalar)
- [Sorun Giderme](#sorun-giderme)
- [Proje Yönetimi](#proje-yönetimi)
- [Lisans ve Kapsam](#lisans-ve-kapsam)

---

## Özet

AI Decision Ecosystem Engine, şirketlerin stratejik kararlarını tek bir bakış
açısından değil, farklı kurumsal rollerin değerlendirmeleri üzerinden analiz
eder. Sistem bir senaryo girdisini alır, üç farklı agent ile yorumlar, skorları
birleştirir ve karar sonucunu açıklanabilir şekilde üretir.

Proje; backend API, veritabanı, frontend, Docker, test otomasyonu, veri bilimi
hazırlığı, LLM entegrasyonu ve raporlama sürecini birlikte ele alan uçtan uca
bir yazılım mühendisliği çalışmasıdır.

---

## Yönetici Özeti

| Başlık | Açıklama |
| --- | --- |
| Proje adı | AI Decision Ecosystem Engine |
| Temel amaç | Kurumsal karar senaryolarını çok ajanlı analizle değerlendirmek |
| Ana kullanıcı | Yönetici ekipler, proje ekipleri, karar destek sistemi geliştiricileri |
| Karar çıktıları | `APPROVE`, `REVISE`, `REJECT` |
| Backend | FastAPI, PostgreSQL, SQLAlchemy, Alembic |
| Frontend | React, TypeScript, Vite |
| Agent rolleri | CEO, CFO, HR |
| LLM yaklaşımı | Yerel Ollama ile isteğe bağlı açıklama zenginleştirme |
| Test yaklaşımı | Pytest, API testleri, frontend build kontrolü |
| Teslim bağlamı | BMU326 Yazılım Mühendisliği dönem projesi |

---

## Problem ve Çözüm

| Problem | Projedeki çözüm |
| --- | --- |
| Kararların tek bir perspektifle verilmesi | CEO, CFO ve HR agent rolleriyle çok yönlü değerlendirme |
| Skorların açıklamasız kalması | Agent bazlı gerekçe ve tartışma mesajları |
| Frontend ve backend ayrımının belirsiz olması | REST API sözleşmesi ve React cockpit arayüzü |
| LLM kullanımının deterministik kararı bozma riski | LLM yalnızca reasoning alanını zenginleştirir, karar motoru korunur |
| Rapor ve teslim sürecinde dağınık dokümantasyon | `docs/` altında ayrılmış proje, veri bilimi, rapor ve iç not klasörleri |

---

## Mevcut Uygulama Durumu

| Alan | Durum | Not |
| --- | --- | --- |
| Backend API | Tamamlandı | FastAPI endpointleri çalışır durumda |
| Veritabanı | Tamamlandı | PostgreSQL, SQLAlchemy repository katmanı ve Alembic kullanılıyor |
| Agent karar motoru | Tamamlandı | CEO, CFO ve HR agent skorları üretiliyor |
| Tartışma akışı | Tamamlandı | Turlu agent mesajları API yanıtında dönüyor |
| LLM entegrasyonu | Çalışır durumda | `MADE_USE_LLM=1` ile aktif ediliyor |
| Frontend temel akışı | Mevcut | React arayüz backend ile bağlanabiliyor |
| Frontend demo iyileştirmeleri | Devam ediyor | Debate console ve executive report tarafı geliştirilecek |
| Veri bilimi hazırlığı | Büyük ölçüde tamamlandı | Dataset mapping ve kalibrasyon stratejisi belgelendi |
| Rapor | Devam ediyor | Taslak `docs/report/final_report_draft.md` altında |
| Jira görselleri | Planlandı | Pano düzeni rapor öncesi iyileştirilecek |

---

## Sistem Mimarisi

### Katmanlı yapı

```text
+--------------------------------------------------------------------------------+
|                                Presentation                                    |
| FastAPI routes, request/response schemas, dependency wiring                     |
+--------------------------------------------------------------------------------+
|                                Application                                     |
| Use-case servisleri, senaryo akışı, API işlemlerinin orkestrasyonu             |
+--------------------------------------------------------------------------------+
|                                  Domain                                        |
| Agent modelleri, karar kuralları, classifier, aggregator, LLM port sözleşmesi  |
+--------------------------------------------------------------------------------+
|                              Infrastructure                                    |
| PostgreSQL, SQLAlchemy repository implementasyonları, Ollama LLM client        |
+--------------------------------------------------------------------------------+
```

### Modül sorumlulukları

| Modül | Sorumluluk |
| --- | --- |
| `app/domain/agents/` | CEO, CFO, HR agent sınıfları, LLM wrapper ve agent factory |
| `app/domain/services/` | Senaryo sınıflandırma, tartışma orkestrasyonu ve karar toplama |
| `app/domain/learning/` | Dataset loader, agent calibrator, sentetik veri ve debate orchestrator |
| `app/application/use_cases/` | Senaryo oluşturma, listeleme ve simülasyon use-case akışları |
| `app/infrastructure/database/` | Veritabanı modelleri, session ve temel ORM yapılandırması |
| `app/infrastructure/repositories/` | Domain repository arayüzlerinin SQLAlchemy implementasyonları |
| `app/presentation/api/` | FastAPI endpointleri |
| `frontend/src/` | React arayüzü, karar tipleri ve kullanıcı etkileşimi |

### Tasarım ilkeleri

| İlke | Uygulamadaki karşılığı |
| --- | --- |
| Katman ayrımı | Domain katmanı veritabanı ve web framework detaylarından bağımsız tutulur |
| Test edilebilirlik | Agent ve servis davranışları bağımsız test edilebilir yapıdadır |
| Açıklanabilirlik | Her agent skorla birlikte gerekçe üretir |
| Güvenli LLM kullanımı | LLM çıktısı kararın kendisini değil, açıklama alanını zenginleştirir |
| Genişletilebilirlik | Yeni agent, yeni classifier veya yeni veri kaynağı eklenebilir |

---

## Karar Akışı

```text
Senaryo girdisi
  -> doğrulama ve normalizasyon
  -> senaryo sınıflandırma
  -> CEO / CFO / HR agent analizleri
  -> turlu tartışma ve mesaj üretimi
  -> skorların birleştirilmesi
  -> nihai karar
  -> API ve frontend çıktısı
```

| Adım | Açıklama |
| --- | --- |
| 1. Senaryo oluşturma | Kullanıcı senaryo başlığı, açıklama, bütçe, ROI, risk ve ekip hazırlığı girer |
| 2. Sınıflandırma | Sistem senaryonun bağlamını belirler |
| 3. Agent analizi | Her agent kendi uzmanlık alanına göre skor ve gerekçe üretir |
| 4. Tartışma | Agent mesajları turlar halinde izlenebilir |
| 5. Toplama | Aggregator ortak skoru ve nihai kararı hesaplar |
| 6. Sunum | Sonuç API ve frontend üzerinden gösterilir |

---

## Agent Rolleri

| Agent | Odak alanı | Değerlendirme örnekleri |
| --- | --- | --- |
| CEO | Stratejik uygunluk ve büyüme potansiyeli | Pazar etkisi, ROI, uzun vadeli fırsat |
| CFO | Finansal sürdürülebilirlik | Bütçe, maliyet riski, yatırım geri dönüşü |
| HR | Ekip kapasitesi ve uygulanabilirlik | Takım hazırlığı, insan kaynağı ihtiyacı, operasyonel yük |

### Karar eşikleri

| Ortalama skor | Karar | Yorum |
| --- | --- | --- |
| 75 ve üzeri | `APPROVE` | Senaryo genel olarak uygulanabilir görülür |
| 50-74 | `REVISE` | Senaryo potansiyel taşır fakat iyileştirme ister |
| 50 altı | `REJECT` | Risk veya uygulanabilirlik problemi yüksektir |

---

## Teknoloji Yığını

| Katman | Teknolojiler |
| --- | --- |
| Backend | Python 3.11, FastAPI, Pydantic, Uvicorn |
| Veritabanı | PostgreSQL 16, SQLAlchemy, Alembic, asyncpg, psycopg2 |
| Frontend | React 19, TypeScript, Vite, React Query, Recharts |
| LLM | Ollama, OpenAI uyumlu local endpoint, LangChain portları |
| Veri bilimi | Pandas, dataset mapping, agent kalibrasyonu |
| Test | Pytest, pytest-asyncio, HTTPX |
| DevOps | Docker, Docker Compose, PowerShell helper scriptleri |
| Raporlama | Markdown, Mermaid/DOT diyagramları, ekran görüntüsü varlıkları |

---

## Gereksinimler

| Gereksinim | Sürüm / Not |
| --- | --- |
| Python | 3.11 önerilir |
| Node.js | Frontend için güncel LTS sürümü önerilir |
| npm | Frontend bağımlılıkları için kullanılır |
| Docker Desktop | PostgreSQL ve backend container akışı için |
| PostgreSQL | Docker Compose içinde `postgres:16-alpine` |
| Ollama | Sadece LLM açık demo için gerekir |

---

## Kurulum

### Depoyu klonlama

```bash
git clone https://github.com/multi-agent-decision-engine/ai-decision-ecosystem.git
cd ai-decision-ecosystem
```

### Python ortamı

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Bağımlılık kurulumu:

```bash
pip install -r requirements.txt
```

Ortam dosyası:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

---

## Hızlı Başlangıç

### Docker ile backend ve veritabanı

```bash
docker compose up --build
```

API dokümantasyonu:

```text
http://localhost:8000/docs
```

Servisleri durdurma:

```bash
docker compose down
```

### Backend local çalışma

```bash
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload
```

Backend adresi:

```text
http://localhost:8000
```

### Frontend çalışma

```bash
cd frontend
npm install
npm run dev
```

Frontend adresi:

```text
http://127.0.0.1:5173
```

Build kontrolü:

```bash
npm run build
```

---

## LLM Modu

LLM modu zorunlu değildir. Sistem LLM kapalıyken deterministik agent karar
motoruyla çalışır. LLM açıldığında yalnızca agent gerekçe metinleri
zenginleştirilir; skor, stance ve nihai karar korunur.

| Değişken | Açıklama |
| --- | --- |
| `MADE_USE_LLM=1` | LLM wrapper katmanını aktif eder |
| `LLM_BASE_URL=http://host.docker.internal:11434/v1` | Docker içinden host Ollama endpointine erişim sağlar |
| `LLM_MODEL=qwen2.5:7b` | Kullanılacak yerel model adı |

Linux/macOS:

```bash
export MADE_USE_LLM=1
export LLM_BASE_URL=http://host.docker.internal:11434/v1
```

Windows PowerShell:

```powershell
$env:MADE_USE_LLM="1"
$env:LLM_BASE_URL="http://host.docker.internal:11434/v1"
```

---

## API Özeti

### Endpoint tablosu

| Method | Endpoint | Açıklama |
| --- | --- | --- |
| `POST` | `/api/v1/scenarios` | Yeni senaryo oluşturur |
| `GET` | `/api/v1/scenarios` | Senaryoları sayfalı olarak listeler |
| `GET` | `/api/v1/scenarios/{id}` | Tek bir senaryonun detayını getirir |
| `POST` | `/api/v1/scenarios/{id}/simulate` | Agent simülasyonunu çalıştırır |
| `GET` | `/api/v1/scenarios/{id}/simulation` | Senaryo, agent mesajları ve nihai kararı getirir |

### Örnek senaryo girdisi

```json
{
  "name": "Market Expansion Initiative",
  "description": "Expand into Southeast Asia market",
  "budget_million_usd": 5.0,
  "expected_roi_percent": 45.0,
  "risk_level": 6,
  "team_readiness": 7
}
```

### Örnek simülasyon yanıtı

```json
{
  "scenario_id": 5,
  "total_rounds": 2,
  "consensus_reached": false,
  "final_score": 46.0,
  "final_decision": "REJECT",
  "scenario_type": "team_expansion",
  "agent_weights": {
    "CEO": 0.25,
    "CFO": 0.25,
    "HR": 0.5
  }
}
```

Detaylı sözleşme:

```text
docs/backend_simulation_contract.md
```

---

## Veri Bilimi Katmanı

Veri bilimi çalışması, agent kararlarının ileride yalnızca sabit kurallarla
değil, veriyle kalibre edilebilir bir yapıyla desteklenmesini hedefler.

| Başlık | Açıklama |
| --- | --- |
| Veri mapping | Agile proje verileri karar senaryosu özelliklerine dönüştürülür |
| Feature aileleri | Finansal, stratejik, operasyonel ve ekip kapasitesi sinyalleri |
| Agent kalibrasyonu | Agent skor ağırlıklarının veriyle iyileştirilmesi hedeflenir |
| Outcome based learning | Gerçek sonuçların ileride karar modeline geri beslenmesi planlanır |
| Rapor kaynağı | `docs/data_science/DATA_SCIENCE_OVERVIEW.md` |

---

## Test ve Doğrulama

| Kontrol | Komut |
| --- | --- |
| Backend testleri | `pytest` |
| Belirli test dosyası | `pytest tests/test_llm_agent.py -v` |
| Frontend build | `cd frontend && npm run build` |
| Demo smoke (tam akış) | `.\start.ps1` (sonunda `scripts/demo_smoke_check.ps1` koşar) |
| Demo smoke (tek başına) | `.\scripts\demo_smoke_check.ps1 -BaseUrl http://localhost:8000` |
| API dokümantasyonu | `http://localhost:8000/docs` |

> `GET /health` tek başına demo hazırlığı **değildir**. Health endpoint 200
> dönse bile DB endpoint'leri bozuk olabilir, port 8000'i başka bir process
> servis ediyor olabilir veya senaryo listesi boş olabilir. Demo öncesi tam
> akış kontrolü için `scripts/demo_smoke_check.ps1` (health → scenarios list
> → isimli demo senaryosunu garantile → `POST /simulate` → `final_decision`
> doğrulaması) zorunlu adımdır ve `start.ps1` bunu son adım olarak otomatik
> çalıştırır.

---

## Repo Yapısı

```text
.
|-- app/
|   |-- application/
|   |-- domain/
|   |-- infrastructure/
|   |-- presentation/
|-- frontend/
|-- alembic/
|-- data/
|-- docs/
|   |-- data_science/
|   |-- internal_notes/
|   |-- project/
|   |-- report/
|-- reports/
|-- scripts/
|-- tests/
|-- weights/
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
|-- README.md
```

---

## Dokümantasyon Haritası

| Dosya / klasör | Kullanım amacı |
| --- | --- |
| `docs/project/ROADMAP.md` | Projenin güncel teknik yol haritası |
| `docs/data_science/DATA_SCIENCE_OVERVIEW.md` | Veri bilimi ve modelleme özeti |
| `docs/report/final_report_draft.md` | Dönem projesi rapor taslağı |
| `docs/internal_notes/PROJECT_MEMORY.md` | Çalışma hafızası ve teslim notları |
| `docs/report_assets/` | Rapor ekran görüntüleri ve diyagramlar |
| `QUICKSTART.md` | Kısa çalıştırma rehberi |
| `README_DATA_SCIENCE.md` | Veri bilimi dosyaları için hızlı rehber |

---

## Bilinen Sınırlamalar

| Alan | Sınırlama | Not |
| --- | --- | --- |
| LLM | Yerel modele ve Ollama durumuna bağlıdır | Demo için kapalı mod kullanılabilir |
| Veri bilimi | Tam üretim ML pipeline hedeflenmemiştir | Rapor kapsamında modelleme stratejisi gösterilir |
| Frontend | Bazı demo ekranları geliştirme aşamasındadır | Issue bazlı takip edilmektedir |
| Jira | Pano görselleri rapor öncesi düzenlenecektir | Süreç bölümü için kullanılacaktır |

---

## Sorun Giderme

| Sorun | Olası neden | Çözüm |
| --- | --- | --- |
| Backend açılmıyor | Veritabanı hazır değildir | `docker compose up -d db` ve `alembic upgrade head` çalıştırın |
| API bağlantısı alınamıyor | Backend portu farklıdır | `http://localhost:8000/docs` adresini kontrol edin |
| Frontend API sonucu göstermiyor | Backend çalışmıyor olabilir | Backend ve browser network tab kontrol edilmeli |
| LLM reasoning boş geliyor | Ollama kapalı veya model yoktur | LLM kapalı demo akışını kullanın veya modeli indirin |
| Docker içinde Ollama görülmüyor | Host adresi yanlış olabilir | `host.docker.internal:11434` değerini kontrol edin |

---

## Proje Yönetimi

Proje GitHub branch, pull request ve issue akışıyla ilerletilir. Rapor tarafında
Jira panosu ayrıca görselleştirilecektir.

| Süreç | Kullanım |
| --- | --- |
| Branch | Özellik ve düzeltmeler ayrı branchlerde geliştirilir |
| Pull request | Kod değişiklikleri review ve kontrol sonrası merge edilir |
| Issue | Frontend, backend, veri bilimi ve rapor işleri takip edilir |
| Jira | Ders raporu için görev panosu ve süreç kanıtı olarak kullanılır |
| Dokümantasyon | Rapor ve teknik notlar `docs/` altında tutulur |

---

## Lisans ve Kapsam

Bu depo, BMU326 Yazılım Mühendisliği dönem projesi kapsamında geliştirilen
akademik bir çalışmadır. Kod, rapor ve dokümantasyon; proje teslimi, demo ve
ekip içi iş takibini desteklemek amacıyla düzenlenmiştir.
