# Phase 2 Kickoff — DatasetLoader ↔ AgentCalibrator runtime integration

## Özet

PR #12 ile gelen `DatasetLoader` ile var olan `AgentCalibrator` arasındaki **bağlantı boşluğunu kapatır**, runtime'da kullanılabilir bir kalibrasyon altyapısı ekler ve Phase 2 eğitim sonuçlarını **kanıtlanabilir baseline'larla** raporlar. Phase 2'nin "kickoff"u — Phase 1 altyapısının üzerine ajan kalibrasyonu için ilk somut iskelet.

## Eklenen / Değişen Dosyalar

| Dosya | Tür | Açıklama |
|---|---|---|
| `scripts/phase2_train_agents.py` | **new** | End-to-end training pipeline. `DatasetLoader → train/val split → AgentCalibrator → save weights → write report`. CLI argparse, baseline metrikleri, per-class recall. |
| `app/domain/agents/calibrated.py` | **new** | `CalibratedAgent` runtime adapter — base agent çıktısını Phase 2 kalibre edilmiş ağırlıklarla yeniden değerlendirir. `load_calibrated_agent()` factory helper. |
| `app/domain/agents/factory.py` | modified | `MADE_AGENT_WEIGHTS_DIR` env var set ise `weights/{ceo,cfo,hr}_real_weights.json` okuyup `CalibratedAgent` döndürür; eksik dosya varsa sessizce orijinal ajanlara fallback. |
| `tests/test_dataset_loader_calibrator_integration.py` | **new** | 4 entegrasyon testi: contract, 3-epoch eğitim, weights round-trip, REVISE invariant. |
| `tests/test_phase2_runtime_calibration.py` | **new** | Factory env-var davranışı (with/without/missing), CalibratedAgent runtime, gitignore koruması. |
| `tests/test_phase2_train_agents_script.py` | **new** | Script entry-point smoke testi: weights üretimi, rapor şeması, baseline blokları, dataset eksikse açık hata. |
| `reports/phase2_training_results.json` | **new** | Örnek baseline rapor (3 epoch). |
| `README.md` | modified | "Current Status" bölümü — 4 fazlı progress bar, Phase 2 runtime kullanım talimatları. |
| `.gitignore` | modified | `weights/` training artifact ignore. |

## Honest Baseline Reporting

Script `reports/phase2_training_results.json`'a şu baseline'ları ekler:

- `always_majority` — her zaman majority sınıfı tahmin
- `always_approve` / `always_reject` — sabit sınıf
- `random_uniform_expected` — uniform dağılım beklenen accuracy
- Her ajan için `baseline_comparison.beats_majority_baseline` boolean

**Mevcut 3-epoch run sonuçları (val=40):**

```
majority_class:     REJECT
always_majority:    0.600
random_uniform:     0.500

CEO: val_acc=0.400  delta=-0.200  beats_majority=False
CFO: val_acc=0.275  delta=-0.325  beats_majority=False
HR:  val_acc=0.300  delta=-0.300  beats_majority=False
```

**Yorum (intellectual honesty):** Mevcut veri ve hiperparametrelerle ajanlardan hiçbiri "her zaman REJECT" baseline'ını geçemiyor. Bu **beklenen** bir bulgudur, çünkü:

- Kaynak veri 2 sınıflıdır (REVISE yok) → 3-sınıflı karar mekanizması veriden öğrenemez.
- 200 kayıt CLAUDE.md'nin önerdiği 1000+ örneklem hedefinin altında.
- `budget_million_usd=5.0` sabit imputation → bu feature training'de sinyal değil.
- `risk_level` / `team_readiness` ham veri kısıtı nedeniyle yalnızca 5 ayrık değer ([2,4,6,8,10]) içerir.

Bu sınırlamalar `docs/real_dataset_analysis_summary.md` ve script raporundaki `limitations` bloğunda yazılıdır.

**"Tam kalibre edildi" iddiası kurulmaz** — bu PR'ın ana mesajı: pipeline çalışır halde + baseline ölçülebilir + accuracy hedefi henüz yakalanmadı, çünkü veri çeşitliliği yetersiz. Sonraki sprint: Helin'in ek veri kaynakları + REVISE pseudo-label stratejisi.

## Runtime Kullanım (Yeni)

```bash
# 1. Phase 2 ağırlıklarını eğit
python scripts/phase2_train_agents.py

# 2. Uygulamayı kalibre edilmiş ağırlıklarla başlat
export MADE_AGENT_WEIGHTS_DIR=weights
uvicorn app.main:app --reload

# Veya kapalı tut (default deterministic agents çalışır)
unset MADE_AGENT_WEIGHTS_DIR
```

`AgentFactory.create_default_agents()` env var'ı kontrol eder, eksik file fallback'i otomatik.

## Test Sonucu

```
pytest -q
119 passed, 1 skipped in 1.94s
```

- **+10 yeni test** (4 entegrasyon + 4 runtime + 3 script smoke − 1 kasten skip REVISE invariant)
- 109 → 119 passed
- Sıfır regresyon

## Açık Bırakılan / Sonraki PR'lar

| # | Eksik | Sonraki PR / Sprint |
|---|---|---|
| 1 | Stratified train/val split | Helin's next data PR |
| 2 | Hiperparametre arama (grid / `optuna`) | Phase 2 sprint 2 |
| 3 | `SimulationResponse.calibration_metadata` alanı + frontend rozeti | Frontend sprint |
| 4 | LLM (Ollama) prompt'larına calibrated weights enjeksiyonu | Phase 3 |
| 5 | CI'da `scripts/phase2_train_agents.py --epochs 3 --quiet` smoke step | DevOps PR |
| 6 | Versionlanmış weights (`weights/v20260530/` veya DB `active_calibration_version`) | Production hardening |

## Veri Bilimi Sınırlamaları (Engineering ile Kapanmaz, Veri ile Kapanır)

- REVISE örneği yok
- Tek scenario_type (`project_management`)
- `budget_million_usd` sabit (5.0 imputation)

Bunlar Helin'in veri çeşitlendirme PR'ında ele alınacaktır.
