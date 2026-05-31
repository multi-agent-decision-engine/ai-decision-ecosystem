"""Phase 2 — `scripts/phase2_train_agents.py` script smoke testleri.

Script'in `run()` fonksiyonunu doğrudan çağırarak:
- Beklenen output dosyalarının üretildiğini,
- Rapor JSON şemasının CEO/CFO/HR alanlarını ve baseline blokunu içerdiğini,
- Calibrator val_acc'in baseline ile karşılaştırıldığını
doğrular. Böylece script imzasında veya rapor şemasında sessiz bir kırılma
olursa CI bunu yakalar (unit testler tek başına `AgentCalibrator.train`'i
çağırıyor; script entry-point'i ayrı bir yüzey).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REAL_DATASET_PATH = "data/real_datasets/agile_dataset_normalized.json"


pytestmark = pytest.mark.skipif(
    not Path(REAL_DATASET_PATH).exists(),
    reason="agile_dataset_normalized.json yok; normalize scriptini çalıştır.",
)


def test_phase2_script_run_produces_weights_and_report(tmp_path):
    """End-to-end: script çağrılır, 3 ajan için weights ve metric raporu üretilir."""
    from scripts.phase2_train_agents import run

    weights_dir = tmp_path / "weights"
    report_path = tmp_path / "report.json"

    result = run(
        dataset_path=REAL_DATASET_PATH,
        weights_dir=str(weights_dir),
        report_path=str(report_path),
        epochs=2,
        batch_size=8,
        verbose=False,
    )

    # 1. Her ajan için weight dosyası oluştu
    for agent_name in ("ceo", "cfo", "hr"):
        weight_file = weights_dir / f"{agent_name}_real_weights.json"
        assert weight_file.exists(), f"{agent_name} weight dosyası yazılmadı"
        loaded = json.loads(weight_file.read_text(encoding="utf-8"))
        assert loaded["agent_name"] == agent_name.upper()
        assert 0.0 <= loaded["confidence_base"] <= 1.0

    # 2. Rapor dosyası diskte ve return değeriyle aynı şemada
    assert report_path.exists()
    on_disk = json.loads(report_path.read_text(encoding="utf-8"))
    assert on_disk.keys() == result.keys()

    # 3. Rapor sözleşmesi (Phase 2 sözleşmesi sabit)
    assert "dataset" in result
    assert "hyperparameters" in result
    assert "baselines" in result
    assert "agents" in result
    assert "limitations" in result

    assert set(result["agents"]) == {"CEO", "CFO", "HR"}
    for agent_result in result["agents"].values():
        metrics = agent_result["metrics"]["validation"]
        assert "accuracy" in metrics
        assert 0.0 <= metrics["accuracy"] <= 1.0
        comparison = agent_result["baseline_comparison"]
        assert "val_accuracy" in comparison
        assert "always_majority_accuracy" in comparison
        assert "delta_vs_majority" in comparison
        assert comparison["beats_majority_baseline"] in (True, False)


def test_phase2_report_includes_honest_baselines(tmp_path):
    """Baseline metrikleri rapora yazılmalı — `beats_majority` kanıtlanabilir
    bir iddia olmalı, sessizce True varsayılmamalı."""
    from scripts.phase2_train_agents import run

    result = run(
        dataset_path=REAL_DATASET_PATH,
        weights_dir=str(tmp_path / "weights"),
        report_path=str(tmp_path / "report.json"),
        epochs=2,
        batch_size=8,
        verbose=False,
    )

    val_baselines = result["baselines"]["validation"]
    assert "majority_class" in val_baselines
    assert 0.0 <= val_baselines["always_majority"] <= 1.0
    assert 0.0 <= val_baselines["random_uniform_expected"] <= 1.0
    assert "APPROVE" in val_baselines["class_distribution"] or \
           "REJECT" in val_baselines["class_distribution"]

    # Calibrator'lardan en az birinin baseline_comparison'u dolu olmalı
    comps = [a["baseline_comparison"] for a in result["agents"].values()]
    assert all(c["delta_vs_majority"] is not None for c in comps)


def test_phase2_script_raises_when_dataset_missing(tmp_path):
    """Olmayan dataset path'i → açık hata. Sessiz pas geçme yok."""
    from scripts.phase2_train_agents import run

    with pytest.raises(FileNotFoundError):
        run(
            dataset_path=str(tmp_path / "does_not_exist.json"),
            weights_dir=str(tmp_path / "weights"),
            report_path=str(tmp_path / "report.json"),
            epochs=1,
            batch_size=4,
            verbose=False,
        )
