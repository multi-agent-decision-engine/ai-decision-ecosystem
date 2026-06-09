# 3-Minute Demo Script

This script demonstrates the complete workflow of the AI Decision Ecosystem Engine.

**Prerequisites:**
- Docker and Docker Compose installed
- Terminal/PowerShell open in project directory
- Port 8000 is free, or is held only by the deterministic backend container `ai_decision_app`

**Expected demo runtime layout:**

| Service   | Container name        | Port  | Mode                                       |
|-----------|-----------------------|-------|--------------------------------------------|
| Backend   | `ai_decision_app`     | 8000  | Deterministic (`MADE_USE_LLM` unset / `0`) |
| Database  | `ai_decision_db`      | 5432  | Postgres, must be healthy                  |

> The optional LLM backend runs as `ai_decision_app_llm` and is reserved for the
> bonus demo. It must **not** be on port 8000 during the standard demo.
> `start.ps1` aborts with a clear error if another container or host process is
> already listening on port 8000, and runs `scripts/demo_smoke_check.ps1` as the
> final readiness gate before the demo begins.

> **Demo hazırlığı ≠ `/health`.** `GET /health` 200 dönse bile DB endpoint'leri
> bozuk olabilir, port 8000'i başka bir process serviyor olabilir veya senaryo
> listesi boş olabilir. Demo öncesi zorunlu kontrol `scripts/demo_smoke_check.ps1`:
> health → scenarios list → isimli demo senaryosunu garantile → `POST /simulate`
> → `final_decision` doğrulaması. Bu adımların hepsi yeşil dönmeden sahneye çıkma.

### Failed recreate sonrası temizlik (ISSUE-005)

`docker compose up --build` port çakışması veya başka bir nedenle yarıda
kaldıysa, `ai_decision_app` container'ı `running` görünmesine rağmen
`NetworkSettings.Networks` boş kalabilir ve port yayını yapılmaz. Bu durumda
`/health` 200 dönebilir ama DB endpoint'leri 500 verir. Doğrulama ve temizlik:

```powershell
# 1) App container'in DB-bagli healthcheck'i healthy mi?
docker inspect -f '{{.State.Health.Status}}' ai_decision_app
# beklenen: healthy

# 2) Port gercekten host'a yayinlaniyor mu?
docker compose ps
# beklenen: app satirinda '0.0.0.0:8000->8000/tcp'

# 3) Host tarafindan DB-bagli endpoint 200 doner mi?
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/api/v1/scenarios?limit=1
# beklenen: 200

# Yukaridakilerden biri eksikse temiz baslangic:
docker compose down --remove-orphans
docker ps --filter "publish=8000" --format "{{.Names}}"   # bossa devam
.\start.ps1
```

---

## Bonus Demo: LLM-backed Agents (Optional)

The final live demo is **deterministic** — `start.ps1` forces `MADE_USE_LLM=0`
and the simulation endpoint responds in ~0.2 s. The LLM-backed path is shipped
as an **optional bonus** because `POST /api/v1/scenarios/{id}/simulate` can
take 30–90 s end-to-end and has been observed to time out at 60 s in unwarmed
states.

Run the bonus demo **alongside** (not instead of) the standard demo:

```powershell
# After .\start.ps1 has finished successfully:
.\start-llm-demo.ps1                       # port 8010, model qwen2.5:7b
.\start-llm-demo.ps1 -HostPort 8010 -Model qwen2.5:7b
```

`start-llm-demo.ps1`:

1. Verifies the standard demo container `ai_decision_app` is up (DB + image
   are reused).
2. Launches a separate container `ai_decision_app_llm` on `HostPort` (default
   `8010`) with `MADE_USE_LLM=1` and `OLLAMA_BASE_URL=http://host.docker.internal:11434`.
3. Waits for `/health`, then runs `scripts/llm_smoke_check.ps1`, which:
   - checks Ollama is reachable at `localhost:11434`,
   - confirms the requested model is present (`ollama pull qwen2.5:7b` if not),
   - **warms the model** with one short completion (eliminates cold-start),
   - runs a full LLM simulation with a 180 s timeout and verifies `final_decision`.

If any of those steps fail, the bonus demo aborts before you go on stage —
you only ever present the LLM path when smoke is green.

> The LLM bonus is **never** the path used in the main live demo. If you want
> to show LLM reasoning during the talk, open `http://localhost:8010/docs`
> after `start-llm-demo.ps1` finishes — keep the deterministic backend on
> `http://localhost:8000` as the primary surface.

### LLM Bonus: Gercek Metin Tartismasi (kanit)

`app/domain/agents/llm_agent.py` `LLMAgent` wrapper'i Round 2+'da agent'a
**onceki turun tum mesaj metinlerini** sunar ve "en guclu argumani tanimla;
somut sayilarla destekle ya da acikca karsi cik" diye prompt eder. Yani LLM
modunda agent'lar **gercek karsi-argumanli muzakere** yapar; stance /
confidence / metrics base agent'tan gelir (karar mantigi LLM
hallucination'a maruz kalmaz).

**Kanit:** [`docs/demo-evidence/llm_debate_id10_n3.txt`](demo-evidence/llm_debate_id10_n3.txt)
ornek bir cikti icerir — id=10 senaryosunda CFO Round 2'de HR'a aciktan atif
yapiyor ("Eski HR baskanimin belirttigi gibi..."), HR varsayim bir CEO
cagrisini reddiyor ("'hizla baslayalim' cagrisini nazikce reddetmekteyim"),
Round 3'te CEO ve CFO HR'in endisesini kabul edip ortak bir strateji
oneriyor ("phased rollout"). Final karar deterministik akistaki ile birebir
ayni: REVISE / 59.9.

**Latency:**
- CPU-only mode (`docs/demo-evidence/qwen-cpu.Modelfile`): ~50s/cagri,
  3 agent x 3 tur = **~8 dakika** tek senaryo icin
- GPU mode (varsayilan `qwen2.5:7b`): ~10s/cagri, **~90 saniye** tek senaryo
  (GPU bellegi yeterliyse)

CPU latency'si canli sahnede izlenemez. Sunum stratejisi:

1. **Pre-record video clip** — bonus akisi onceden kaydet, sunumda oynat.
   En guvenli ve etkileyici secenek.
2. **GPU varsa canli kos** — `start-llm-demo.ps1` ile bonus port 8010,
   ~90 saniye beklerken sunumun deterministik kismina (radar, signal
   matrix) gec.
3. **Sadece sozlu anlat + kanit dosyasini ekrana yansit** — en hizli, en
   az risk, ama gorsel sok yaratmaz.

**Calistirma (CPU-only):**

```powershell
# 1) qwen-cpu varyantini olustur (bir kez)
ollama create qwen-cpu -f docs/demo-evidence/qwen-cpu.Modelfile

# 2) Bonus akis ile baslat (start.ps1 calismis olmali)
.\start-llm-demo.ps1 -Model qwen-cpu

# 3) Smoke check `LLM_MODEL=qwen-cpu` env'i ile model'i ister; 180s timeout
#    GPU varsa Model parametresini gonderme: qwen2.5:7b default kalsin
```

## Step 1: Start the Application (1 min)

### Linux/macOS:
```bash
make start
```

### Windows (PowerShell):
```powershell
.\start.ps1
```

**Expected output:**
```
Starting containers...
Waiting for db to be healthy...
Running migrations...
API docs: http://localhost:8000/docs
```

The application is now running at `http://localhost:8000`.

---

## Step 2: Open Swagger UI (30 sec)

Open browser to: **http://localhost:8000/docs**

You'll see the interactive API documentation with all endpoints listed.

---

## Step 3: Create a Scenario (1 min)

In Swagger UI, click on `POST /api/v1/scenarios` and expand it.

Click "Try it out" and enter this JSON in the request body:

```json
{
  "name": "Southeast Asia Expansion",
  "description": "Enter Southeast Asian market with new product line",
  "budget_million_usd": 8.5,
  "expected_roi_percent": 35.0,
  "risk_level": 6,
  "team_readiness": 8
}
```

Click "Execute".

**Expected response:**
```json
{
  "scenario_id": 1
}
```

**Note the scenario_id (should be 1 for first scenario).**

---

## Step 4: Run Simulation (1 min)

Click on `POST /api/v1/scenarios/{id}/simulate`.

Click "Try it out" and enter: `1` for the scenario_id.

Click "Execute".

**Expected response:**
```json
{
  "scenario_id": 1,
  "agent_outputs": [
    {
      "agent_name": "CEO",
      "score": 70,
      "rationale": "Strategic fit 35% with market risk 0.6 yields strategic score 70."
    },
    {
      "agent_name": "CFO",
      "score": 61,
      "rationale": "ROI 41.2% with risk factor 0.6 yields financial score 61."
    },
    {
      "agent_name": "HR",
      "score": 72,
      "rationale": "Team readiness 8/10 with 8 hires needed and 3 months to readiness yields HR score 72."
    }
  ],
  "final_score": 67.67,
  "final_decision": "REVISE"
}
```

**Decision interpretation:**
- Average score: 67.67
- Since 50 ≤ 67.67 < 75: Decision = **REVISE**
- Recommendation: Study feedback and resubmit with improvements

---

## Step 5: Retrieve Simulation Results (1 min)

### Option A: Get Scenario Details
Click on `GET /api/v1/scenarios/{id}`.

Enter scenario_id: `1`

You'll see the scenario metadata and creation timestamp.

### Option B: Get Simulation with All Outputs
Click on `GET /api/v1/scenarios/{id}/simulation`.

Enter scenario_id: `1`

You'll see:
- Full scenario record
- All agent outputs with scores and rationale
- Final aggregated score and decision

### Option C: List All Scenarios
Click on `GET /api/v1/scenarios`.

You can paginate with `limit` and `offset` parameters (default: limit=20, offset=0).

---

## Alternative: Using curl

Instead of Swagger, you can use curl from terminal:

```bash
# 1. Create scenario
SCENARIO=$(curl -s -X POST http://localhost:8000/api/v1/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Launch",
    "description": "Q2 product release",
    "budget_million_usd": 3.0,
    "expected_roi_percent": 25.0,
    "risk_level": 4,
    "team_readiness": 9
  }')

echo "Created: $SCENARIO"
SCENARIO_ID=$(echo $SCENARIO | grep -o '"scenario_id":[0-9]*' | grep -o '[0-9]*')

# 2. Run simulation
curl -s -X POST http://localhost:8000/api/v1/scenarios/$SCENARIO_ID/simulate | jq .

# 3. Get simulation results
curl -s http://localhost:8000/api/v1/scenarios/$SCENARIO_ID/simulation | jq .
```

---

## Alternative: Using Python

```python
import requests
import json

base_url = "http://localhost:8000/api/v1"

# 1. Create scenario
scenario_data = {
    "name": "Digital Transformation",
    "description": "Cloud infrastructure modernization",
    "budget_million_usd": 12.0,
    "expected_roi_percent": 50.0,
    "risk_level": 5,
    "team_readiness": 7,
}

scenario = requests.post(f"{base_url}/scenarios", json=scenario_data).json()
scenario_id = scenario["scenario_id"]
print(f"✓ Created scenario {scenario_id}\n")

# 2. Run simulation
simulation = requests.post(f"{base_url}/scenarios/{scenario_id}/simulate").json()
print(f"Final Decision: {simulation['final_decision']} (score: {simulation['final_score']})\n")

# 3. Display agent opinions
for agent in simulation["agent_outputs"]:
    print(f"{agent['agent_name']}: {agent['score']}")
    print(f"  → {agent['rationale']}\n")

# 4. Get full results
full_results = requests.get(f"{base_url}/scenarios/{scenario_id}/simulation").json()
print(f"Final result stored with timestamp: {full_results['scenario']['created_at']}")
```

---

## Testing Edge Cases

### Low Score Scenario (Should result in REJECT)

```json
{
  "name": "Risky Venture",
  "description": "Uncertain market with low ROI",
  "budget_million_usd": 15.0,
  "expected_roi_percent": 5.0,
  "risk_level": 9,
  "team_readiness": 2
}
```

Expected: Low scores from all agents → REJECT decision

### High Score Scenario (Should result in APPROVE)

```json
{
  "name": "Safe Bet",
  "description": "Clear market opportunity, expert team",
  "budget_million_usd": 2.0,
  "expected_roi_percent": 80.0,
  "risk_level": 2,
  "team_readiness": 10
}
```

Expected: High scores from all agents → APPROVE decision

---

## Stopping the Application

### Linux/macOS:
```bash
make stop
```

### Windows (PowerShell):
```powershell
.\stop.ps1
```

This runs `docker compose down` and stops all containers.

---

## Summary

You've now:
1. ✓ Started the application with Docker Compose
2. ✓ Created a scenario with normalized inputs
3. ✓ Ran multi-agent simulation
4. ✓ Retrieved results with agent reasoning
5. ✓ Verified decision logic (CEO/CFO/HR scoring → aggregation)

The system demonstrates clean architecture, deterministic agent logic, and complete API coverage.
