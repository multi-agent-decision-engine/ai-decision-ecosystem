# Melike — Rapor Bölümleri (Word'e Yapıştırılabilir Metin)

Bu dosya BMU326 dönem projesi rapor formatında Melike'nin sorumlu olduğu tüm bölümlerin yazıya dökülmüş hâlidir. Her başlık doğrudan Word raporuna kopyalanabilir.

İlgili görseller:
- Mimari diyagram: `docs/report_assets/diagrams/architecture.png` (Graphviz ile render)
- E-R diyagramı: `docs/report_assets/diagrams/er_diagram.png` (Graphviz ile render)

---

## 1.1 Projenin Amacı ve Kapsamı

**Amaç.** Multi-Agent Decision Engine, iş senaryolarını CEO, CFO ve HR perspektiflerinden eş zamanlı olarak değerlendiren bir karar destek sistemidir. Sistem; bir senaryonun bütçesi, beklenen ROI, risk seviyesi ve takım hazır olma durumu bilgilerini girdi olarak alır. Üç farklı uzman ajan, çok turlu (round-based) bir tartışma yürütür: ilk turda ajanlar bağımsız analiz üretir, sonraki turlarda birbirlerinin gerekçelerine yanıt verir. Tartışma sonunda ağırlıklı bir nihai skor (`final_score`) ve karar (`APPROVE`, `REVISE`, `REJECT`) üretilir. Sonuç, React tabanlı bir Decision Cockpit ekranında yöneticiye sunulur.

**Kapsam (in scope).**
- CEO, CFO, HR ajanlarının analizini içeren round-based simulation akışı.
- Scenario CRUD (POST/GET) ve simulation/simulation-result endpoint'leri.
- Scenario classification ve dinamik ajan ağırlıkları (`agent_weights`).
- React/Vite cockpit: scenario listesi, debate console, executive report.
- PostgreSQL + Alembic ile kalıcı senaryo, ajan çıktısı ve final karar kaydı.
- pytest ile domain ve API davranışlarının doğrulanması; OpenAPI snapshot ile sözleşme koruması.
- Docker Compose ile backend + DB ortamı.

**Kapsam dışı (out of scope).**
- Gerçek kurumsal finans/ERP sistemlerine canlı entegrasyon yapılmamaktadır.
- Rol bazlı kullanıcı kimlik doğrulama (auth) bu teslimin ana kapsamında değildir; demo amaçlı anonim erişim kullanılır.
- Sistem üretilen kararı **karar destek** çıktısı olarak sunar; nihai iş kararı insan kullanıcıya aittir.
- Üretim ortamı dağıtımı (production deployment) ve ölçeklendirme bu teslimin kapsamı dışındadır.

---

## 2.4 İş Kuralları ve Kısıtlamalar

Sistem aşağıdaki iş kurallarını backend domain katmanında ve Pydantic şemalarında zorunlu kılar.

| ID | Kural | Uygulandığı Yer |
|---|---|---|
| BR-01 | `risk_level` 1 ile 10 arasında tam sayıdır. | `app/presentation/schemas/scenario.py` |
| BR-02 | `team_readiness` 1 ile 10 arasında tam sayıdır. | `app/presentation/schemas/scenario.py` |
| BR-03 | `budget_million_usd` pozitif (> 0) olmalıdır. | `app/presentation/schemas/scenario.py` |
| BR-04 | `expected_roi_percent` sayısal bir değerdir; negatif ROI'ler kabul edilir (zarar senaryoları). | `app/presentation/schemas/scenario.py` |
| BR-05 | `final_score >= 75` → `APPROVE`. | `app/domain/services/aggregator.py` |
| BR-06 | `50 <= final_score < 75` → `REVISE`. | `app/domain/services/aggregator.py` |
| BR-07 | `final_score < 50` → `REJECT`. | `app/domain/services/aggregator.py` |
| BR-08 | `scenario_type` yalnızca şu enum değerlerinden biri olabilir: `high_growth`, `cost_optimization`, `team_expansion`, `strategic_pivot`, `maintenance`. | `app/domain/services/classifier.py` |
| BR-09 | `agent_weights` yalnızca `CEO`, `CFO`, `HR` anahtarlarını taşır ve toplamı 1.0'a yakındır. | `DecisionAggregator.aggregate` |
| BR-10 | Simulation response içinde `rounds`, `messages` ve `agent_outputs` boş dönemez (minItems=1). | OpenAPI snapshot testi |
| BR-11 | Mevcut olmayan bir `scenario_id` için simulation endpoint'i `404` döner. | `app/presentation/api/v1/routes/scenarios.py` |
| BR-12 | Ajan mesajının `stance` değeri yalnızca `support`, `neutral`, `oppose` olabilir; `confidence` ∈ [0.0, 1.0]. | Domain `AgentMessage` modeli |

---

## 5. Yazılım Mimarisi ve Tasarımı

### 5.1 Sistem Mimarisi

Sistem **Clean Architecture / Layered Architecture** prensiplerine göre dört katmana ayrılmıştır. Bağımlılıklar yalnızca dış katmandan iç katmana doğru akar; domain katmanı framework'ten bağımsızdır.

- **Presentation Layer.** Dış dünya ile iletişim. FastAPI route'ları (`app/presentation/api/v1/routes/`), Pydantic şemaları (`app/presentation/schemas/`) ve React/Vite cockpit frontend'i (`frontend/`).
- **Application Layer.** Use case servisleri (`app/application/use_cases/`). Senaryo simülasyonu, classification ve liste sorguları gibi iş akışlarını orkestre eder; framework ve DB detaylarından habersizdir.
- **Domain Layer.** Sistemin kalbi. Ajanlar (`app/domain/agents/`), tartışma orkestratörü, classifier, aggregator ve domain modelleri (`app/domain/models.py`, `app/domain/repositories.py`). Saf Python; dış kütüphane bağımlılığı minimumdur.
- **Infrastructure Layer.** SQLAlchemy Async tabanlı repository implementasyonları (`app/infrastructure/repositories/`), veritabanı oturumu (`app/infrastructure/database/`), LLM/logger adaptörleri ve konfigürasyon.

### 5.1.1 Mimari Diyagram

Aşağıdaki diyagram katmanlar arası veri akışını gösterir. Kaynak: `docs/report_assets/diagrams/architecture.dot` (Graphviz ile render edilmiş PNG: `architecture.png`).

```
[React Cockpit] ──HTTPS/JSON──▶ [FastAPI Routes + Pydantic]
                                        │
                                        ▼
                              [Application Use Cases]
                                        │
              ┌─────────────────────────┼───────────────────────┐
              ▼                         ▼                       ▼
       [Agents CEO/CFO/HR]      [DiscussionOrchestrator]  [Classifier / Aggregator]
              │                         │                       │
              └────────────► [Domain Models] ◀──────────────────┘
                                        │
                                        ▼
                            [SQLAlchemy Repositories]
                                        │
                                        ▼
                                   [PostgreSQL]
```

### 5.1.2 Katmanların Sorumlulukları

| Katman | Sorumluluk | Örnek Dosya |
|---|---|---|
| Presentation | HTTP isteğini parse etmek, şemayı doğrulamak, response üretmek. | `app/presentation/api/v1/routes/scenarios.py` |
| Application | İş akışını koordine etmek (örn. senaryo getir → ajanları çalıştır → kararı kaydet). | `app/application/use_cases/` |
| Domain | İş kurallarını ve ajan davranışını içermek. Framework bağımsız. | `app/domain/agents/hr_agent.py`, `app/domain/services/aggregator.py` |
| Infrastructure | Kalıcılık, dış sistem entegrasyonları, oturum yönetimi. | `app/infrastructure/repositories/scenario_repository.py` |

### 5.2 Tasarım Desenleri

| Desen | Amaç | Proje Kullanımı |
|---|---|---|
| **Repository Pattern** | Domain'i kalıcılık detaylarından izole etmek. | `app/domain/repositories.py` arayüzü; `app/infrastructure/repositories/scenario_repository.py` SQLAlchemy implementasyonu. |
| **Dependency Injection** | Bağımlılıkları runtime'da enjekte etmek, test edilebilirliği artırmak. | `app/presentation/dependencies.py` içinde FastAPI `Depends` ile repository ve servis enjeksiyonu. |
| **Factory Pattern** | Ajan örneklerini merkezi olarak üretmek. | `app/domain/agents/factory.py` — scenario type ve weights'e göre `Agent` listesi döner. |
| **Strategy (ABC tabanlı)** | Aynı arayüz arkasında farklı ajan davranışları sunmak. | `app/domain/agents/base.py` `Agent` ABC; CEO/CFO/HR farklı `analyze()` stratejileri. |

---

## 6. Veritabanı Tasarımı ve ORM

### 6.1 E-R Modeli

Üç çekirdek varlık vardır: **Scenario**, **AgentOutput**, **FinalDecision**.

İlişkiler:
- `Scenario` 1 — N `AgentOutput` (bir senaryonun her ajandan bir analiz çıktısı vardır).
- `Scenario` 1 — 1 `FinalDecision` (bir senaryonun en fazla bir nihai kararı vardır; FK `UNIQUE`).
- Her iki ilişkide de `ON DELETE CASCADE` aktiftir: senaryo silinirse bağlı ajan çıktıları ve nihai karar da silinir.

Görsel: `docs/report_assets/diagrams/er_diagram.png`.

### 6.2 İlişkisel Şema

**scenarios**

| Kolon | Tip | Kısıt |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| name | VARCHAR(120) | NOT NULL |
| description | TEXT | NOT NULL |
| budget_million_usd | FLOAT | NOT NULL, > 0 |
| expected_roi_percent | FLOAT | NOT NULL |
| risk_level | INTEGER | NOT NULL, 1..10 |
| team_readiness | INTEGER | NOT NULL, 1..10 |
| created_at | DATETIME | NOT NULL, default `utcnow` |

**agent_outputs**

| Kolon | Tip | Kısıt |
|---|---|---|
| id | INTEGER | PK |
| scenario_id | INTEGER | FK → scenarios.id, ON DELETE CASCADE, NOT NULL |
| agent_name | VARCHAR(30) | NOT NULL (CEO / CFO / HR) |
| score | INTEGER | NOT NULL |
| rationale | TEXT | NOT NULL |

**final_decisions**

| Kolon | Tip | Kısıt |
|---|---|---|
| id | INTEGER | PK |
| scenario_id | INTEGER | FK → scenarios.id, ON DELETE CASCADE, **UNIQUE**, NOT NULL |
| final_score | FLOAT | NOT NULL |
| decision | VARCHAR(20) | NOT NULL (APPROVE / REVISE / REJECT) |

### 6.3 ORM Konfigürasyonu ve Entity Sınıfları

ORM olarak **SQLAlchemy 2.x** kullanılır; oturum yönetimi `AsyncSession` üzerinden yapılır (`app/infrastructure/database/session.py`). Aşağıda `ScenarioORM` örnek alınmıştır (`app/infrastructure/database/models.py`):

```python
class ScenarioORM(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    budget_million_usd: Mapped[float] = mapped_column(Float, nullable=False)
    expected_roi_percent: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[int] = mapped_column(Integer, nullable=False)
    team_readiness: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    agent_outputs = relationship(
        "AgentOutputORM", back_populates="scenario", cascade="all, delete-orphan"
    )
    final_decision = relationship(
        "FinalDecisionORM", back_populates="scenario",
        uselist=False, cascade="all, delete-orphan",
    )
```

### 6.4 Tablo İlişkilerinin Modellenmesi

**1-N (Scenario → AgentOutput).**

```python
class AgentOutputORM(Base):
    __tablename__ = "agent_outputs"
    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False
    )
    scenario = relationship("ScenarioORM", back_populates="agent_outputs")
```

**1-1 (Scenario → FinalDecision).** `uselist=False` ve FK `unique=True` ile tek değerli ilişki garanti edilir:

```python
class FinalDecisionORM(Base):
    __tablename__ = "final_decisions"
    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False, unique=True,
    )
    scenario = relationship("ScenarioORM", back_populates="final_decision")
```

### 6.5 Migration Yönetimi

Şema değişiklikleri **Alembic** ile sürdürülür (`alembic/versions/`).

- İlk şema: `alembic/versions/0001_initial_tables.py` (scenarios, agent_outputs, final_decisions).
- Yeni bir kolon/tablo değişikliği için: `alembic revision --autogenerate -m "<mesaj>"`.
- Üretim/Docker ortamında uygulama açılışında: `alembic upgrade head`.
- Docker Compose ortamında PostgreSQL servisi ile birlikte migration'lar entry-point üzerinden uygulanır.

---

## 7.2 API / Servis Katmanı

### Endpoint Tablosu

| # | Method | Endpoint | Açıklama |
|---|---|---|---|
| 1 | POST | `/api/v1/scenarios` | Yeni karar senaryosu oluşturur, 201 döner. |
| 2 | GET | `/api/v1/scenarios?limit=&offset=` | Sayfalı senaryo listesi döner. |
| 3 | GET | `/api/v1/scenarios/{id}` | Tek senaryo detayını döner; bulunamazsa 404. |
| 4 | POST | `/api/v1/scenarios/{id}/simulate` | CEO/CFO/HR round-based simülasyon çalıştırır, detaylı sonuç döner. |
| 5 | GET | `/api/v1/scenarios/{id}/simulation` | Daha önce kaydedilmiş simülasyon sonucunu döner. |
| 6 | POST | `/api/v1/classify` | Senaryoyu sınıflandırır, `scenario_type` ve `confidence` döner. |
| 7 | POST | `/api/v1/weights` | Scenario type'a göre `agent_weights` döner. |

### Örnek İstek / Yanıt — `POST /api/v1/scenarios/5/simulate`

**Request (gövdesiz; senaryo `id=5` üzerinden çalışır):**

```http
POST /api/v1/scenarios/5/simulate HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Response (200 OK):**

```json
{
  "scenario_id": 5,
  "rounds": [
    {
      "round_number": 1,
      "messages": [
        { "agent": "CEO", "stance": "support", "confidence": 0.82,
          "reasoning": "Strategic upside is strong; ROI 22% with manageable risk.",
          "metrics": { "growth_potential": 8 }, "round_number": 1 },
        { "agent": "CFO", "stance": "oppose", "confidence": 0.61,
          "reasoning": "Budget exposure high vs. cash position.",
          "metrics": { "risk_index": 7 }, "round_number": 1 },
        { "agent": "HR",  "stance": "neutral", "confidence": 0.55,
          "reasoning": "Team readiness moderate (6/10); upskilling needed.",
          "metrics": { "readiness": 6 }, "round_number": 1 }
      ]
    },
    {
      "round_number": 2,
      "messages": [
        { "agent": "HR", "stance": "support", "confidence": 0.66,
          "reasoning": "Given CEO growth case and CFO risk note, phased rollout reduces team strain.",
          "metrics": { "readiness": 7 }, "round_number": 2 }
      ]
    }
  ],
  "total_rounds": 2,
  "consensus_reached": false,
  "stability_reached": true,
  "agent_outputs": [
    { "agent_name": "CEO", "score": 78, "rationale": "Maintains support after CFO risk note." },
    { "agent_name": "CFO", "score": 45, "rationale": "Risk index above tolerance." },
    { "agent_name": "HR",  "score": 66, "rationale": "Phased rollout viable." }
  ],
  "final_score": 64.0,
  "final_decision": "REVISE",
  "scenario_type": "strategic_pivot",
  "scenario_type_confidence": 0.72,
  "agent_weights": { "CEO": 0.45, "CFO": 0.30, "HR": 0.25 }
}
```

Frontend bu yanıttan executive report'u oluşturur: `final_score` ve `final_decision` üst panele, `agent_outputs` ajan kartlarına, `rounds[].messages` debate console'a beslenir.

---

## 7.3 Önemli Kod Parçaları

### (1) `ScenarioSimulationService.run_simulation` — Simülasyon akışını koordine eder.

Sorumluluk: senaryoyu repository'den getir → classifier ile tip belirle → ağırlıkları üret → orchestrator ile round-based debate çalıştır → aggregator ile final kararı hesapla → sonucu kaydet ve döndür.

### (2) `DiscussionOrchestrator.run_discussion` — Round-based tartışma.

İlk turda ajanlar bağımsız analiz üretir (`prior_messages=[]`). Sonraki turlarda her ajana önceki turun mesajları geçirilir; HR ajanı özel olarak CEO ve CFO çıktılarına referans verir. Convergence (skor standart sapması) ve engagement (cross-reference oranı) metrikleri hesaplanır; `stability_reached` veya maksimum tur sayısında durulur.

### (3) `ScenarioClassifier.classify` — Senaryo tipini belirler.

Bütçe, ROI, risk ve team readiness alanlarından kural tabanlı bir skorlamayla `scenario_type` ∈ {high_growth, cost_optimization, team_expansion, strategic_pivot, maintenance} ve `confidence` üretir. Sonuç, `agent_weights` üretiminde kullanılır.

### (4) `DecisionAggregator.aggregate` — Nihai skor ve kararı hesaplar.

```python
def aggregate(self, messages, weights=None):
    if not messages:
        raise ValueError("messages boş olamaz")
    total_weight, weighted_sum = 0.0, 0.0
    for m in messages:
        if   m.stance == "support": score = m.confidence * 100
        elif m.stance == "oppose":  score = (1 - m.confidence) * 100
        else:                       score = 50.0
        w = (weights or {}).get(m.agent, 1.0 / len(messages))
        weighted_sum += score * w
        total_weight += w
    average = weighted_sum / total_weight if total_weight else 0
    if   average >= 75: decision = FinalDecision.APPROVE
    elif average >= 50: decision = FinalDecision.REVISE
    else:               decision = FinalDecision.REJECT
    return AggregatedDecision(final_score=round(average, 2), decision=decision)
```

### (5) `SqlAlchemyScenarioRepository` — Repository pattern uygulaması.

`app/infrastructure/repositories/scenario_repository.py` içinde `create`, `list`, `get_by_id` metodları async SQLAlchemy oturumuyla domain interface'ini (`app/domain/repositories.py`) gerçekler. Use case katmanı yalnızca interface'i bilir; SQL detaylarına bağımlı değildir.

---

## 8. Birim Test Çalışmaları

### 8.1 Test Stratejisi

Test piramidi üç seviyeden oluşur:

1. **Domain unit testleri** (en geniş katman) — Ajanlar, classifier, aggregator ve orchestrator saf Python ile test edilir; DB veya HTTP bağımlılığı yoktur.
2. **API integration testleri** — FastAPI `TestClient`/`httpx.AsyncClient` ile uçtan uca endpoint davranışı doğrulanır. Geçici SQLite/PostgreSQL backend'i kullanılır.
3. **Sözleşme (contract/snapshot) testleri** — `tests/test_simulation_schema_snapshot.py` OpenAPI şemasındaki kritik property ve enum setlerini sabitler; frontend-backend sözleşmesinde regresyonu önler.

Araçlar: **pytest**, **pytest-asyncio**, **httpx**. Çalıştırma: `pytest` (kök dizinden). Son tam koşum: **104 passed**.

### 8.2 Test Senaryoları

| ID | Test Edilen Sınıf / Metot | Senaryo | Beklenen Sonuç |
|---|---|---|---|
| UT-01 | `CEOAgent.analyze` | Yüksek ROI ve orta risk verilen analiz. | `AgentMessage` döner; `stance=support`, `confidence` ∈ [0,1]; metrics dolu. |
| UT-02 | `CFOAgent.analyze` | Yüksek risk ve sınırlı bütçe. | CFO `oppose` ya da düşük confidence; rationale risk vurgulu. |
| UT-03 | `HRAgent.analyze` | Düşük team readiness. | HR `neutral`/`oppose`; gerekçede kapasite/eğitim ihtiyacı. |
| UT-04 | `DiscussionOrchestrator.run_discussion` | 2. turda HR mesajı. | Mesaj CEO/CFO içeriğine referans verir; `round_number=2`. |
| UT-05 | `SimulationResponse` Pydantic şeması | `rounds=[]` veya `messages=[]` gönderimi. | ValidationError; minItems=1 kuralı korunur. |
| UT-06 | `POST /api/v1/scenarios/{id}/simulate` | Geçerli scenario id. | 200 OK; `final_score`, `final_decision`, `agent_outputs`, `rounds` dolu. |
| UT-07 | `POST /api/v1/scenarios/{id}/simulate` | Olmayan scenario id. | 404 Not Found. |
| UT-08 | `ScenarioClassifier.classify` | Tipik high-growth girdisi. | `scenario_type="high_growth"`; `confidence > 0.5`. |
| UT-09 | `DecisionAggregator.aggregate` | Eşit ağırlık, karışık stance. | `final_score` doğru ortalama; karar eşik tablosuna uyar. |
| UT-10 | OpenAPI snapshot | `/openapi.json` çıktısı. | Beklenen property ve enum seti (APPROVE/REVISE/REJECT, scenario_type değerleri) korunur. |

### 8.3 Çalıştırma Komutu ve Beklenen Çıktı

```bash
pytest -q
```

Beklenen özet (son koşum):

```
....................................................................................................    [100%]
104 passed in X.XXs
```

Sözleşme odaklı alt küme için:

```bash
pytest tests/test_api_scenario_get_endpoints.py tests/test_round_based_discussion.py tests/test_simulation_schema_snapshot.py
```

Beklenen: tüm testler `passed`. Çıktı ekran görüntüsü `docs/report_assets/tests/pytest_output.png` olarak rapora eklenir.

---

## Melike Aksiyon Takip Listesi

- [x] Bölüm 1.1 — Amaç & Kapsam yazıldı.
- [x] Bölüm 2.4 — İş kuralları tablosu yazıldı.
- [x] Bölüm 5 — Mimari, diyagram açıklaması, tasarım desenleri yazıldı.
- [x] Bölüm 6 — E-R, ilişkisel şema, ORM, ilişkiler, migration yazıldı.
- [x] Bölüm 7.2 — API endpoint tablosu + örnek JSON request/response.
- [x] Bölüm 7.3 — Önemli kod parçaları seçildi ve açıklandı.
- [x] Bölüm 8 — Test stratejisi, test senaryosu tablosu, komut/çıktı.
- [x] Mimari diyagramı PNG/SVG hazır (Graphviz).
- [x] E-R diyagramı PNG/SVG hazır (Graphviz).
- [x] `pytest -q` çıktısı kaydedildi (104 passed) + terminal stilinde PNG.
- [x] Canlı API kanıtları (`get_scenarios.json`, `simulate_response.json`).
- [ ] GitHub PR/review ekran görüntüleri (manuel — `docs/report_assets/github/`).
- [ ] Jira board/kart ekran görüntüleri (manuel — `docs/report_assets/jira/`).
