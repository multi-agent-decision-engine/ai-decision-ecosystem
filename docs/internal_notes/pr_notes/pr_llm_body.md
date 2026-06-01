# feat(agents): LLM-Augmented Agents — opt-in semantic reasoning + cross-message debate

## Why

Şu ana kadar `analyze()` reasoning'i template slot-fill üretiyordu; round 2 "Cross-analysis: CEO's <stance> reviewed; HR keeps its position" gibi mekanik cümleler oluyordu. Bu PR, ajan davranışını **stance ve confidence sözleşmesini bozmadan** semantik LLM tartışmasına yükseltir.

## What

**Wrap pattern, replace pattern değil.** Mevcut `CalibratedAgent` ile aynı tasarım:

```
LLMAgent (yeni wrapper)
   └─> base_agent (CEOAgent / CFOAgent / HRAgent)
           ├─ math + rules → stance, confidence, metrics  (DETERMINISTIC, UNCHANGED)
           └─ template reasoning  (LLM çıktısıyla DEĞİŞTİRİLİR)
```

### Yeni dosyalar

| Dosya | Sorumluluk |
|---|---|
| `app/infrastructure/llm_client.py` | `LLMClient` Protocol + `OllamaLLMClient` (production) + `StubLLMClient` (test) + `LLMUnavailableError` |
| `app/domain/agents/llm_agent.py` | `LLMAgent` wrapper; persona prompt + scenario context + prior messages = LLM reasoning |
| `app/domain/agents/factory.py` (M) | `MADE_USE_LLM=1` env opt-in; explicit `llm_client=` parametresi ile DI |
| `tests/test_llm_agent.py` | 5 unit test (replace, fallback x2, prompt structure, round-2 prior messages) |
| `tests/test_llm_agent_factory.py` | 4 factory test (env truthy/falsy/missing, explicit DI) |
| `scripts/demo_llm_reasoning.py` | Stub LLM ile before/after karşılaştırması (Ollama gerekmez) |
| `README.md` (M) | "LLM-Augmented Agents (opt-in)" bölümü + runtime aktivasyon talimatı |

### Sözleşme Garantileri

Stance/confidence/metrics base agent'tan gelir → AgentMessage Pydantic şeması ve `tests/test_simulation_schema_snapshot.py` invariant'ları **dokunulmaz**. LLM hata verirse / boş döndürse base agent çıktısı geri döner — sistem hiçbir koşulda crash etmez.

LLM çağrı metadata'sı (`source: OllamaLLMClient|StubLLMClient`, `fallback_used: false`) `metrics["llm"]` altında yayınlanır. Pydantic `dict[str, Any]` sözleşmesiyle uyumlu.

## Runtime kullanım

```bash
# Ollama açıksa
export MADE_USE_LLM=1
uvicorn app.main:app --reload

# Ollama erişilemezse otomatik template fallback (graceful degradation)
unset MADE_USE_LLM
```

## Before / After Demo

```bash
python scripts/demo_llm_reasoning.py
```

Örnek (HR, round 2, CEO + CFO sonrası):

**Before (template):**
> "[HR Metni / HR Analysis]: Ekip kapasitesi / team capacity and workload review (readiness: 5/10) | Team readiness is 5/10. Hiring need is 3 people with 4.0 months to productivity..."

**After (LLM):**
> "Round 2'de CEO'nun phased rollout önerisini ve CFO'nun milestone bazlı bütçe yaklaşımını birleştirebileceğimizi düşünüyorum. Eğer ilk 6 ay pilot pazara odaklanırsak ekibim 4 senior hire ile rahatlar; team_readiness'i 7+'a çekersek Q3'te ikinci pazarı açabiliriz. Pozisyonumu support'a çekiyorum."

Round 2 mesajı round 1'deki CEO ve CFO içeriğine **gerçek semantik yanıt veriyor**, slot doldurmuyor.

## Tests

```
pytest -q
118 passed in 1.73s
```

- **+9 yeni test** (5 LLMAgent + 4 Factory)
- 109 → 118 passed
- Sıfır regresyon, schema snapshot bozulmadı

## Mimari Konum

`Agent` ABC sözleşmesi tam korunur. Bu PR, ajan davranışını **rule + math** seviyesinden **semantic reasoning + cross-message debate** seviyesine çıkarır, ancak deterministic decision logic'i feda etmeden:

- `stance` / `confidence` — base agent (kural tabanlı + calibrator) tarafından kararlaştırılır
- `metrics` — base agent'ın hesapladığı sayısal feature'lar + LLM metadata
- `reasoning` — LLM tarafından zenginleştirilir (veya template'e fallback)

`CalibratedAgent` (PR #13) ile composition: ileride `LLMAgent(CalibratedAgent(CEOAgent))` zinciri kurulabilir. Bu PR'da Factory yalnız base agent'ları sarmalıyor; calibrated + LLM kompozisyonu sonraki PR'ın işidir (PR #13 merge sonrası).

## Veri Bilimi Perspektifi

LLM, mevcut 200-kayıt 2-sınıflı veriyle **accuracy'yi sihirle yükseltmez** — accuracy bottleneck'i veri çeşitliliğindedir (Helin'in görevi). Ancak:

- Round-2 mesajları artık semantically responsive
- Reasoning içeriği scenario-spesifik, template değil
- LLM'in `support_conditional` gibi nüanslı çıktıları **REVISE pseudo-label** üretimi için Phase 3'te kullanılabilir
- Counter-intuitive case'ler (ör. yüksek ROI + düşük risk ama uzman REJECT) için LLM hipotez üretebilir

## Sonraki Adımlar (bu PR'a girmedi)

| # | Sonraki | Açıklama |
|---|---|---|
| 1 | `LLMAgent(CalibratedAgent(BaseAgent))` composition | PR #13 merge sonrası factory'de zincirleme |
| 2 | LLM'in stance'i de etkilemesi (yapısal output) | v2 — LLM'den JSON output, schema validation, stance override |
| 3 | LLM-as-judge → REVISE pseudo-label üretimi | Helin's next data PR |
| 4 | Calibrated weights'in LLM prompt'a personality bias olarak enjekte edilmesi | Phase 2.5 polish |
| 5 | CI'da `MADE_USE_LLM=1` smoke step (mock backend ile) | DevOps |
