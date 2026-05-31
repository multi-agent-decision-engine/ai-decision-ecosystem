"""Phase 2 — DatasetLoader → AgentCalibrator entegrasyon testleri.

PR #12 ile gelen `DatasetLoader.load_calibration_data()` çıktısının doğrudan
`AgentCalibrator.train()`'in beklediği dict şemasıyla uyumlu olduğunu ve uçtan
uca eğitim akışının (load → split → train → save weights) hatasız
çalıştığını doğrular.
"""

import json
from pathlib import Path

import pytest

from app.domain.learning.agent_calibrator import AgentCalibrator, AgentWeights
from app.domain.learning.dataset_loader import DatasetLoader


REAL_DATASET_PATH = "data/real_datasets/agile_dataset_normalized.json"


def _has_real_dataset() -> bool:
    return Path(REAL_DATASET_PATH).exists()


pytestmark = pytest.mark.skipif(
    not _has_real_dataset(),
    reason="agile_dataset_normalized.json yok; normalize scriptini çalıştır.",
)


def test_loader_output_matches_calibrator_input_contract():
    """Loader çıktısının her kaydı, Calibrator.train()'in döngüsünde
    bekleneni karşılayan tüm anahtarlara sahip olmalı."""
    loader = DatasetLoader(file_path=REAL_DATASET_PATH)
    data = loader.load_calibration_data()

    assert len(data) > 0
    required_keys = {
        "budget_million_usd",
        "expected_roi_percent",
        "risk_level",
        "team_readiness",
        "ground_truth_decision",
        "expert_confidence",
    }
    for record in data:
        missing = required_keys - record.keys()
        assert not missing, f"Calibrator sözleşmesinde eksik alan: {missing}"
        assert isinstance(record["risk_level"], int)
        assert isinstance(record["team_readiness"], int)
        assert isinstance(record["budget_million_usd"], (int, float))
        assert record["ground_truth_decision"] in {"APPROVE", "REVISE", "REJECT"}


def test_calibrator_trains_on_real_data_for_each_agent():
    """CEO/CFO/HR için 3 epoch hızlı eğitim — pipeline'ın patlamadığını ve
    train_losses / val_losses dolduğunu doğrular."""
    loader = DatasetLoader(file_path=REAL_DATASET_PATH)
    data = loader.load_calibration_data()
    train, val = loader.train_validation_split(data, train_ratio=0.8, seed=42)

    assert len(train) >= 8 and len(val) >= 8, "Yetersiz veri"

    for agent_name in ("CEO", "CFO", "HR"):
        calibrator = AgentCalibrator(
            agent_name=agent_name,
            learning_rate=0.01,
            l2_regularization=0.001,
            verbose=False,
        )
        history = calibrator.train(
            training_data=list(train),
            validation_data=list(val),
            epochs=3,
            batch_size=8,
        )

        assert "final_train_loss" in history
        assert "final_val_loss" in history
        assert "best_weights" in history
        assert history["best_weights"]["agent_name"] == agent_name
        assert calibrator.train_losses, "train_losses dolmalı"
        assert calibrator.val_losses, "val_losses dolmalı"


def test_trained_weights_serialize_roundtrip(tmp_path):
    """Eğitim sonrası AgentWeights'in JSON'a yazılıp geri okunabildiğini doğrular —
    Phase 2 script'inin diske kaydetme adımı için sözleşme garantisi."""
    loader = DatasetLoader(file_path=REAL_DATASET_PATH)
    data = loader.load_calibration_data()
    train, val = loader.train_validation_split(data, train_ratio=0.8, seed=42)

    calibrator = AgentCalibrator(agent_name="CEO", verbose=False)
    calibrator.train(training_data=list(train), validation_data=list(val),
                     epochs=2, batch_size=8)

    out_path = tmp_path / "ceo_real_weights.json"
    out_path.write_text(json.dumps(calibrator.weights.to_dict()), encoding="utf-8")

    loaded = json.loads(out_path.read_text(encoding="utf-8"))
    restored = AgentWeights.from_dict(loaded)
    assert restored.agent_name == "CEO"
    assert restored.roi_weight == calibrator.weights.roi_weight


def test_dataset_class_distribution_warns_on_missing_revise():
    """Veri kaynağında REVISE eksikliği bilinen bir sınırlama —
    eğitimin yine de çalıştığını ama 3-sınıflı öğrenmenin kısıtlı olduğunu
    test edilebilir bir invariant olarak yakalar."""
    loader = DatasetLoader(file_path=REAL_DATASET_PATH)
    data = loader.load_calibration_data()
    decisions = {r["ground_truth_decision"] for r in data}

    # Bilinen Phase 1 sınırlaması — dokümantasyon ile uyumlu olmalı
    assert "APPROVE" in decisions
    assert "REJECT" in decisions
    if "REVISE" not in decisions:
        pytest.skip(
            "REVISE örneği yok — docs/real_dataset_analysis_summary.md "
            "sınırlamasıyla uyumlu, Phase 2 sonraki adımda ek kaynak gerekir."
        )
