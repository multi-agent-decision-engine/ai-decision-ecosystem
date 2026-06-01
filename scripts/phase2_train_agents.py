"""Phase 2 — CEO / CFO / HR ajan kalibrasyon pipeline'ı.

Bu script DatasetLoader -> AgentCalibrator zincirini uçtan uca çalıştırır,
her ajan için öğrenilmiş ağırlıkları diske yazar ve eğitim sonuçlarını
JSON rapor olarak üretir.

Kullanım:
    python scripts/phase2_train_agents.py
    python scripts/phase2_train_agents.py --epochs 50 --batch-size 16

Çıktılar:
    weights/<agent>_real_weights.json   (her ajan için final ağırlıklar)
    reports/phase2_training_results.json (özet metrikler + history)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Script doğrudan `python scripts/phase2_train_agents.py` ile çalıştırıldığında
# proje kökünü sys.path'e ekle (paket olmayan scripts/ dizini için standart).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from app.domain.learning.agent_calibrator import AgentCalibrator  # noqa: E402
from app.domain.learning.dataset_loader import DatasetLoader  # noqa: E402


AGENTS = ("CEO", "CFO", "HR")
DEFAULT_DATASET = "data/real_datasets/agile_dataset_normalized.json"
DEFAULT_WEIGHTS_DIR = "weights"
DEFAULT_REPORT = "reports/phase2_training_results.json"


def _ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _evaluate_accuracy(calibrator: AgentCalibrator, dataset: list[dict]) -> dict:
    correct = 0
    by_decision = {"APPROVE": [0, 0], "REVISE": [0, 0], "REJECT": [0, 0]}
    for record in dataset:
        pred, _ = calibrator._predict(record)
        gt = record["ground_truth_decision"]
        if gt in by_decision:
            by_decision[gt][1] += 1
            if pred == gt:
                by_decision[gt][0] += 1
                correct += 1
    total = len(dataset)
    return {
        "accuracy": correct / total if total else 0.0,
        "per_class": {
            d: {
                "correct": c,
                "total": t,
                "recall": (c / t) if t else None,
            }
            for d, (c, t) in by_decision.items()
        },
    }


def _accuracy_if_constant(dataset: list[dict], prediction: str) -> float:
    """Bütün kayıtlara aynı sınıfı atayan baseline'ın accuracy'si."""
    if not dataset:
        return 0.0
    correct = sum(1 for r in dataset if r["ground_truth_decision"] == prediction)
    return correct / len(dataset)


def _baseline_metrics(dataset: list[dict]) -> dict:
    """Calibrator değerlendirmesi için karşılaştırma baseline'ları.

    Kalibratörün gerçekten *öğrenmiş* olduğunu iddia edebilmek için
    val_acc'in en azından bu naive baseline'ları geçmesi beklenir.
    """
    if not dataset:
        return {
            "always_majority": None,
            "majority_class": None,
            "always_approve": None,
            "always_reject": None,
            "random_uniform_expected": None,
            "class_distribution": {},
        }

    distribution: dict[str, int] = {}
    for record in dataset:
        gt = record["ground_truth_decision"]
        distribution[gt] = distribution.get(gt, 0) + 1
    majority_class = max(distribution, key=distribution.get)

    classes_present = list(distribution.keys()) or ["APPROVE", "REJECT", "REVISE"]
    random_expected = sum(
        (count / len(dataset)) * (1.0 / len(classes_present))
        for count in distribution.values()
    )

    return {
        "majority_class": majority_class,
        "always_majority": _accuracy_if_constant(dataset, majority_class),
        "always_approve": _accuracy_if_constant(dataset, "APPROVE"),
        "always_reject": _accuracy_if_constant(dataset, "REJECT"),
        "random_uniform_expected": random_expected,
        "class_distribution": distribution,
    }


def _calibrator_vs_baseline(
    val_accuracy: float, baselines: dict
) -> dict:
    """Calibrator val_acc'in baseline'a göre konumu — honest reporting için."""
    majority = baselines.get("always_majority")
    delta_vs_majority = (
        round(val_accuracy - majority, 4) if majority is not None else None
    )
    beats_majority = (
        bool(delta_vs_majority > 0) if delta_vs_majority is not None else None
    )
    return {
        "val_accuracy": round(val_accuracy, 4),
        "always_majority_accuracy": majority,
        "delta_vs_majority": delta_vs_majority,
        "beats_majority_baseline": beats_majority,
    }


def train_agent(
    agent_name: str,
    train_data: list[dict],
    val_data: list[dict],
    *,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    l2: float,
    verbose: bool,
) -> dict:
    calibrator = AgentCalibrator(
        agent_name=agent_name,
        learning_rate=learning_rate,
        l2_regularization=l2,
        verbose=verbose,
    )
    history = calibrator.train(
        training_data=list(train_data),
        validation_data=list(val_data),
        epochs=epochs,
        batch_size=batch_size,
    )
    train_eval = _evaluate_accuracy(calibrator, list(train_data))
    val_eval = _evaluate_accuracy(calibrator, list(val_data))
    return {
        "agent": agent_name,
        "history": history,
        "weights": calibrator.weights.to_dict(),
        "metrics": {
            "train": train_eval,
            "validation": val_eval,
            "train_loss_curve": calibrator.train_losses,
            "val_loss_curve": calibrator.val_losses,
        },
    }


def run(
    *,
    dataset_path: str = DEFAULT_DATASET,
    weights_dir: str = DEFAULT_WEIGHTS_DIR,
    report_path: str = DEFAULT_REPORT,
    epochs: int = 50,
    batch_size: int = 16,
    learning_rate: float = 0.01,
    l2: float = 0.001,
    train_ratio: float = 0.8,
    seed: int = 42,
    verbose: bool = True,
) -> dict:
    if not Path(dataset_path).exists():
        raise FileNotFoundError(
            f"Normalize edilmiş veri seti bulunamadı: {dataset_path}. "
            "Önce `python scripts/normalize_agile_dataset.py` çalıştırın."
        )

    loader = DatasetLoader(file_path=dataset_path)
    data = loader.load_calibration_data()
    train_data, val_data = loader.train_validation_split(
        data, train_ratio=train_ratio, seed=seed
    )
    if verbose:
        print(f"Dataset: {len(data)} kayıt -> train={len(train_data)} val={len(val_data)}")

    weights_path = _ensure_dir(weights_dir)
    val_baselines = _baseline_metrics(val_data)
    train_baselines = _baseline_metrics(train_data)
    results: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "path": dataset_path,
            "total_records": len(data),
            "train_records": len(train_data),
            "val_records": len(val_data),
            "train_ratio": train_ratio,
            "seed": seed,
        },
        "hyperparameters": {
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "l2_regularization": l2,
        },
        "baselines": {
            "train": train_baselines,
            "validation": val_baselines,
        },
        "agents": {},
        "limitations": [
            "Veri yalnız APPROVE/REJECT içerir; REVISE bu kaynaktan öğrenilemez.",
            "budget_million_usd=5.0 sabit imputation — budget sensitivity sınırlı.",
            "Tek scenario_type (project_management) — dynamic weighting sığ.",
        ],
    }

    for agent_name in AGENTS:
        if verbose:
            print(f"\n--- {agent_name} eğitimi başlıyor ---")
        agent_result = train_agent(
            agent_name,
            train_data,
            val_data,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            l2=l2,
            verbose=verbose,
        )
        agent_result["baseline_comparison"] = _calibrator_vs_baseline(
            agent_result["metrics"]["validation"]["accuracy"], val_baselines
        )
        weights_file = weights_path / f"{agent_name.lower()}_real_weights.json"
        weights_file.write_text(
            json.dumps(agent_result["weights"], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        if verbose:
            comp = agent_result["baseline_comparison"]
            print(
                f"{agent_name}: val_acc={comp['val_accuracy']:.3f} "
                f"(majority baseline={comp['always_majority_accuracy']:.3f}, "
                f"delta={comp['delta_vs_majority']:+.3f}, "
                f"beats={comp['beats_majority_baseline']}) "
                f"-> {weights_file}"
            )
        results["agents"][agent_name] = agent_result

    report_file = Path(report_path)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    if verbose:
        print(f"\nRapor yazıldı: {report_file}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--weights-dir", default=DEFAULT_WEIGHTS_DIR)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--l2", type=float, default=0.001)
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    run(
        dataset_path=args.dataset,
        weights_dir=args.weights_dir,
        report_path=args.report,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        l2=args.l2,
        train_ratio=args.train_ratio,
        seed=args.seed,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
