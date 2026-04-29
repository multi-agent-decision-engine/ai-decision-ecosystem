# Development Workflow

## Kanban Process

This project follows a Jira Kanban workflow for task management and code delivery.

### Workflow Stages

```
To Do → In Progress → Code Review → Done
```

1. **To Do**: Backlog of prioritized tasks
2. **In Progress**: Actively being developed
3. **Code Review**: Pull request submitted, awaiting approval
4. **Done**: Merged to main, deployed

## Branch Strategy

### Naming Convention

All feature branches follow this pattern:

```
feature/JIRA-XX-short-description
```

**Examples:**
- `feature/JIRA-12-add-cfo-agent`
- `feature/JIRA-34-implement-scenario-retrieval`
- `feature/JIRA-56-docker-compose-setup`

### Development Flow

1. **Pick Task**: Move Jira card from "To Do" to "In Progress"
2. **Create Branch**: 
   ```bash
   git checkout -b feature/JIRA-XX-description
   ```
3. **Develop**: Implement changes following clean architecture principles
4. **Test Locally**:
   ```bash
   pytest -q
   ```
5. **Push Branch**:
   ```bash
   git push origin feature/JIRA-XX-description
   ```
6. **Open Pull Request**: Move Jira card to "Code Review"

## Pull Request Requirements

Every PR must include:

- **Linked Jira Task**: Reference `JIRA-XX` in PR title/description
- **Clear Description**: 
  - What was changed
  - Why it was changed
  - How to test it
- **CI Status**: All GitHub Actions checks must pass
- **Code Review**: At least 1 approval required

### PR Template

```
## Jira Task
JIRA-XX: [Task Title]

## Changes
- Added/Modified/Fixed [component]
- Updated [file/module]

## Testing
- [ ] Unit tests pass
- [ ] API tests pass
- [ ] Manual testing completed

## Checklist
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] Clean architecture maintained
```

## Code Review Policy

### Reviewer Responsibilities
- Check code follows clean architecture principles
- Verify domain layer has no infrastructure dependencies
- Ensure all DB operations use repositories (no raw SQL)
- Confirm tests cover new functionality
- Validate SOLID principles are maintained

### Approval Criteria
- At least **1 approval** required to merge
- CI pipeline must be green
- No unresolved comments

### Merge Process
1. PR approved by reviewer(s)
2. CI passes
3. Squash and merge to `main`
4. Delete feature branch
5. Move Jira card to "Done"

## CI Pipeline

GitHub Actions runs on every PR:
- Install Python dependencies
- Run pytest suite
- Report status to PR

## Best Practices

- Keep PRs small and focused (single task)
- Write meaningful commit messages
- Update tests alongside code changes
- Keep domain logic pure (no infrastructure coupling)
- Follow existing patterns (Repository, Factory, DI)

# BMU326 Çoklu Etmenli Karar Destek Sistemi (Multi-Agent Decision Ecosystem)
## Akademik Teknik Durum Raporu

**Değerlendirme Tarihi:** 6-10 Nisan 2026  
**Proje Takımı:** 3 Kişi (MZ — Etmen Mimarisi, HM — Makine Öğrenmesi ve Veri, Kişi 3 — Test ve Dokümantasyon)  
**Metodoloji:** Çevik (Agile/Scrum), Sprint Bazlı Yinelemeli Geliştirme  

---

## 1. YÖNETİCİ ÖZETİ (EXECUTIVE SUMMARY)

Bu rapor, "Multi-Agent Decision Ecosystem" (MADE) projesinin akademik ve mühendislik pratikleri bağlamındaki mevcut durumunu, mimari tasarım kararlarını ve versiyon kontrol süreçlerindeki teknik borç analizini sunmaktadır. Proje, otonom etmenlerin (CEO, CFO, HR) belirli senaryoları analiz ederek ortak bir karara vardığı, mikroservis odaklı ve deterministik bir karar destek sistemi olarak kurgulanmıştır. 

Sprint 1 ve Sprint 2 hedefleri **%100 başarıyla tamamlanmış**, sistemin çekirdek mimarisi ve Büyük Dil Modeli (LLM) entegrasyonu stabil hale getirilmiştir. Sprint 3 itibarıyla analitik karar alma mekanizması ML tabanlı bir modele evrilmekte olup, bu süreçte versiyon kontrol sistemi akademik ve profesyonel standartlara yükseltilmiştir.

---

## 2. SİSTEM MİMARİSİ VE METODOLOJİ (SYSTEM ARCHITECTURE)

Projenin teknik altyapısı, yüksek ölçeklenebilirlik, test edilebilirlik ve ayrıklaştırma (decoupling) prensiplerine göre 4 katmanlı Domain-Driven Design (DDD) yaklaşımıyla inşa edilmiştir.

### Teknik Yığın (Tech Stack)
- **Backend & API:** Python 3.10+, FastAPI
- **Yapay Zeka (LLM):** LangChain + Ollama (qwen2.5:14b modeli) — Yerel ortamda (`localhost:11434`)
- **Kalıcılık Katmanı:** PostgreSQL, SQLAlchemy (Sync)
- **Test & Doğrulama:** pytest (Güncel durum: 58/58 başarılı test)
- **İzole Ortam (Containerization):** Docker Compose
- **Versiyon Kontrol:** Git + GitHub (`multi-agent-decision-engine` org)
- **Proje Yönetimi:** Jira (MADE prefix — MADE-4, MADE-5, vs.)

### Katmanlı Mimari (4-Tier Architecture)
1. **Presentation (Sunum Katmanı):** Dış sistemlerle etkileşimi yönetir. FastAPI *route*'ları ve Pydantic *schema*'larını barındırır.
2. **Application (Uygulama Katmanı):** İş akışı orkestratörüdür. `ScenarioSimulationService` aracılığıyla çok turlu simülasyon döngülerini yönetir.
3. **Domain (Çekirdek/Etki Alanı Katmanı):** İş kurallarının merkezidir. `Agent ABC`, `CEO/CFO/HR Agent` soyutlamaları, `DecisionAggregator` ve veri modellerini içerir.
4. **Infrastructure (Altyapı Katmanı):** Dış servis entegrasyonlarını sağlar. Single Source of Truth (SSOT) prensibiyle çalışan `config.py`, yerel LLM haberleşmesini yöneten `llm.py` ve PostgreSQL veri tabanı oturumunu barındırır.

---

## 3. ETMEN MİMARİSİ VE BİLİŞSEL DÖNGÜ (AGENT & COGNITIVE DESIGN)

### 3.1. Hibrit İki Katmanlı Etmen Yaklaşımı (Temel Tasarım Kararı)
Sistemin deterministik kalabilmesi ve halüsinasyon (hallucination) riskinin eylemlere etki etmemesi adına, akademik bir gereksinim olan "Tekrarlanabilirlik" (Reproducibility) gözetilerek etmenler hibrit tasarlanmıştır:

- **Katman 1 (Deterministik Çekirdek):** Etmenin konumu (`stance`: *support*, *oppose*, *neutral*), güven skoru (`confidence`: 0.0 - 1.0) ve etmene özgü metrikler (`metrics`) tamamen kural tabanlı matematiksel formüllerle üretilir. Bu katman kesinlikle değişmez ve testlerin stabil kalmasını sağlar.
- **Katman 2 (LLM Destekli Anlamsal Katman):** Qwen2.5:14b modülü, yalnızca Katman 1'de alınan kararın mantıksal açıklamasını (`reasoning`) İngilizce metin olarak üretmekle sorumludur. LLM apisinin çökmesi durumunda sistem f-string kalıplı hata payı (fallback) ile devam eder. *(Gerekçe: LLM kararı manipüle edemez, sadece bağlamı zenginleştirir.)*

### 3.2. Bilişsel Hafıza Sistemleri (Memory Systems)
- **Kısa Süreli Hafıza (Çalışıyor):** Etmenler, aynı simülasyon içindeki turlarda "Contextual Message Passing" kullanır. `previous_messages` parametresi ile etmenler birbirinin kararını okur ve 2 tur boyunca pozisyon güncelleyebilir.
- **Uzun Süreli Hafıza (Sprint 4 - Backlog):** Farklı simülasyonlar arası öğrenme için Neo4j Graph Database planlanmıştır (Şu an kapsam dışı).

### 3.3. Çok Fazlı Tartışma Akışı (Multiphase Orchestration)
Simülasyon, `ScenarioSimulationService.run_simulation(scenario, n_rounds=2)` üzerinden yürütülür:

```text
TUR 1
 ├── CEOAgent.analyze(scenario, previous=None)  → Formül + LLM Reasoning
 ├── CFOAgent.analyze(scenario, previous=None)
 └── HRAgent.analyze(scenario, previous=None)

TUR 2
 ├── CEOAgent.analyze(scenario, previous=[tur1_mesajları])
 ├── CFOAgent.analyze(scenario, previous=[tur1_mesajları])
 └── HRAgent.analyze(scenario, previous=[tur1_mesajları])

KONSENSÜS (DecisionAggregator)
 ├── Score >= 75 → APPROVE
 ├── Score >= 50 → REVISE
 └── Score < 50  → REJECT
