# Backend Simulation Contract

Sorumlu: Melike  
Kapsam: Agent mimarisi, round-based simulation response ve frontend/backend veri sozlesmesi.

Bu dokuman frontend'in simulation sonucunu hangi alanlardan okuyacagini ve backend'in teslim icin hangi response sozlesmesini saglamasi gerektigini tanimlar.

## Endpoint

```text
POST /api/v1/scenarios/{scenario_id}/simulate
```

## Amac

Secilen senaryo icin CEO, CFO ve HR ajanlarini calistirir. Ajanlar round-based olarak analiz uretir, onceki ajan mesajlarini okuyabilir ve sonuc olarak final decision uretilir.

## Response Alanlari

```json
{
  "scenario_id": 5,
  "rounds": [
    {
      "round_number": 1,
      "messages": [
        {
          "agent": "CEO",
          "stance": "support",
          "confidence": 0.82,
          "reasoning": "Strategic upside is strong.",
          "metrics": {
            "growth_potential": 8
          },
          "round_number": 1
        }
      ]
    }
  ],
  "total_rounds": 2,
  "consensus_reached": false,
  "stability_reached": true,
  "agent_outputs": [
    {
      "agent_name": "CEO",
      "score": 78,
      "rationale": "CEO still supports after CFO risk note."
    }
  ],
  "final_score": 64.0,
  "final_decision": "REVISE",
  "scenario_type": "strategic_pivot",
  "scenario_type_confidence": 0.72,
  "agent_weights": {
    "CEO": 0.45,
    "CFO": 0.30,
    "HR": 0.25
  }
}
```

## Frontend Alan Kullanimi

| UI Bolumu | Backend Alani |
|---|---|
| Scenario simulation result | `final_score`, `final_decision` |
| Agent cards | `agent_outputs` |
| Debate Console | `rounds[].messages[]` |
| Consensus chips | `consensus_reached`, `stability_reached`, `total_rounds` |
| Contribution chart | `agent_weights` veya `agent_outputs[].score` |
| Executive report | `rounds`, `agent_outputs`, `final_score`, `final_decision` |

## Agent Message Contract

Her ajan mesaji su alanlari tasir:

```text
agent
stance
confidence
reasoning
metrics
round_number
```

Gecerli stance degerleri:

```text
support
neutral
oppose
```

Confidence araligi:

```text
0.0 - 1.0
```

## Backend Kabul Kriterleri

1. Endpoint `200` donmeli.
2. Response en az bir `round` icermeli.
3. Her round en az bir agent message icermeli.
4. `agent_outputs` final round sonucuyla uyumlu olmali.
5. `final_decision` sadece `APPROVE`, `REVISE`, `REJECT` degerlerinden biri olmali.
6. `scenario_type` ve `agent_weights` classification aktifse dolu gelmeli.
7. Scenario yoksa endpoint `404` donmeli.
8. `agent_weights` sadece `CEO`, `CFO`, `HR` key'lerini tasir.
9. `scenario_type` sadece su degerlerden biri olabilir:

```text
high_growth
cost_optimization
team_expansion
strategic_pivot
maintenance
```

## Test Komutu

```bash
pytest tests/test_api_scenario_get_endpoints.py tests/test_round_based_discussion.py
```

Beklenen sonuc:

```text
27 passed
```

## Live Kontrol Komutlari

Backend ve DB Docker uzerinden calisirken:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/scenarios
curl -X POST http://localhost:8000/api/v1/scenarios/5/simulate
```

Windows PowerShell:

```powershell
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health
Invoke-WebRequest -UseBasicParsing 'http://localhost:8000/api/v1/scenarios?limit=5&offset=0'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/api/v1/scenarios/5/simulate'
```
