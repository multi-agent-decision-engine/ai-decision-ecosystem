"""Inference-time dataset retrieval (LLM prompt grounding).

`DatasetLoader` kalibrasyon icin tasarlanmis. Bu modul ise **inference**
sirasinda LLM agent prompt'unu **gercek tarihsel projelerle** ground'lar:
agent gerekce yazarken "datasetimdeki benzer 20 vakanin %X'i REVISE oldu"
gibi atif yapabilir.

Veri sema (`data/real_datasets/COMBINED_DATASET.json`):
    [{source, budget, risk, readiness, decision}, ...]

Onemli: bu modul kararı **degistirmez**. Sadece LLM'in dilini zenginlestirir.
Stance/confidence/metrics base agent'tan gelir.
"""
from __future__ import annotations

import json
import os
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Iterable


# Bu sirayla aranir; ilk var olan kullanilir.
_DEFAULT_PATH_CANDIDATES: tuple[str, ...] = (
    # 1) env override
    # 2) repo-relative (host)
    "data/real_datasets/COMBINED_DATASET.json",
    # 3) container WORKDIR-relative
    "/app/data/real_datasets/COMBINED_DATASET.json",
)


def _resolve_dataset_path(explicit_path: str | None = None) -> Path | None:
    # Explicit path verildiyse: sadece o yolu kontrol et, default'lara
    # fallback yapma. Yoksa env + standart adaylar.
    if explicit_path is not None:
        p = Path(explicit_path)
        return p if p.exists() else None

    candidates: Iterable[str] = filter(
        None,
        (
            os.getenv("MADE_DATASET_PATH"),
            *_DEFAULT_PATH_CANDIDATES,
        ),
    )
    for c in candidates:
        p = Path(c)
        if p.exists():
            return p
    return None


@lru_cache(maxsize=4)
def _load_records(path_str: str) -> tuple[dict, ...]:
    """Cached load (tuple ensures hashability for lru_cache).

    path_str string olarak alinir cunku Path lru_cache key olarak uygun degil.
    """
    with open(path_str, "r", encoding="utf-8") as f:
        data = json.load(f)
    return tuple(data)


class DatasetRetriever:
    """Senaryoya en benzer N kayidi cagirir ve ozet uretir.

    Mesafe metrigi: weighted L1 normalized.
        budget   / 50  (dataset araligi 10-48)
        risk     / 10  (1-10 scale)
        readiness / 10
    """

    def __init__(self, dataset_path: str | None = None):
        self.path = _resolve_dataset_path(dataset_path)

    @property
    def is_available(self) -> bool:
        return self.path is not None

    def _records(self) -> tuple[dict, ...]:
        if self.path is None:
            return ()
        return _load_records(str(self.path))

    @staticmethod
    def _distance(record: dict, budget: float, risk: float, readiness: float) -> float:
        return (
            abs(record.get("budget", 0) - budget) / 50.0
            + abs(record.get("risk", 0) - risk) / 10.0
            + abs(record.get("readiness", 0) - readiness) / 10.0
        )

    def find_similar(
        self,
        budget: float,
        risk: float,
        readiness: float,
        k: int = 20,
    ) -> tuple[list[dict], dict]:
        """En benzer k kayit + ozet istatistikleri doner."""
        records = self._records()
        if not records:
            return [], {}

        ranked = sorted(
            records, key=lambda r: self._distance(r, budget, risk, readiness)
        )
        top = ranked[:k]

        decisions = Counter(r.get("decision") for r in top if r.get("decision"))
        budgets = [r["budget"] for r in top if isinstance(r.get("budget"), (int, float))]
        risks = [r["risk"] for r in top if isinstance(r.get("risk"), (int, float))]
        readinesses = [
            r["readiness"] for r in top if isinstance(r.get("readiness"), (int, float))
        ]

        def _safe_range(vals):
            return (min(vals), max(vals)) if vals else (None, None)

        def _safe_mean(vals):
            return sum(vals) / len(vals) if vals else None

        stats = {
            "k": len(top),
            "total_records": len(records),
            "decisions": dict(decisions),
            "budget_range": _safe_range(budgets),
            "budget_mean": _safe_mean(budgets),
            "risk_range": _safe_range(risks),
            "risk_mean": _safe_mean(risks),
            "readiness_range": _safe_range(readinesses),
            "readiness_mean": _safe_mean(readinesses),
        }
        return top, stats

    def outcome_alignment(
        self,
        budget: float,
        risk: float,
        readiness: float,
        stance: str,
        k: int = 20,
    ) -> dict:
        """Agent'in stance'i dataset kanitiyla uyumlu mu? Sayisal ozet doner.

        Dataset yalniz APPROVE/REJECT etiketleri icerir (REVISE yok). Bu
        yuzden:
            - stance == "support"  -> APPROVE'a yakin
            - stance == "oppose"   -> REJECT'e yakin
            - stance == "neutral"  -> 50/50'ye yakin esleme arar

        Donus alanlari:
            available: bool        - dataset bulunduysa True
            k: int                 - kullanilan ornek sayisi
            approve_ratio: float   - 0..1 (REJECT 1-approve_ratio)
            alignment: float       - -1..+1 (+1 stance veri ile tam uyumlu,
                                    -1 tam ters; 0 belirsiz)
            distance_penalty: float - 0..1 (1 = senaryomuz dataset'e cok yakin,
                                    0 = cok uzak; alignment'i bu agirlikla
                                    kullan)
            confidence_delta: float - onerilen -0.20..+0.20 araliginda
                                    confidence guncellemesi
            note: str | None       - reasoning'e eklenmek uzere insan-okur not
        """
        if not self.is_available:
            return {
                "available": False,
                "k": 0,
                "approve_ratio": 0.5,
                "alignment": 0.0,
                "distance_penalty": 0.0,
                "confidence_delta": 0.0,
                "note": None,
            }

        records, stats = self.find_similar(budget, risk, readiness, k=k)
        if not records:
            return {
                "available": False,
                "k": 0,
                "approve_ratio": 0.5,
                "alignment": 0.0,
                "distance_penalty": 0.0,
                "confidence_delta": 0.0,
                "note": None,
            }

        decisions = stats["decisions"]
        approve_count = decisions.get("APPROVE", 0)
        reject_count = decisions.get("REJECT", 0)
        total = approve_count + reject_count
        approve_ratio = approve_count / total if total > 0 else 0.5

        # Stance-spesifik alignment skoru:
        # - support: yuksek approve_ratio +1, dusuk -1
        # - oppose:  yuksek reject_ratio +1, dusuk -1
        # - neutral: 0.5'e yakin +1, ucta -1
        if stance == "support":
            alignment = (approve_ratio - 0.5) * 2  # 0->-1, 1->+1
        elif stance == "oppose":
            alignment = ((1 - approve_ratio) - 0.5) * 2
        else:  # neutral
            # 0.5 -> +1, 0 veya 1 -> -1
            alignment = 1 - abs(approve_ratio - 0.5) * 4
            alignment = max(-1.0, alignment)

        # Distance penalty: bizim senaryomuz dataset dagiliminin disindaysa,
        # historical signal'in agirligini dusur. budget_mean farki en buyuk
        # gostergesi.
        budget_mean = stats.get("budget_mean") or 0.0
        risk_mean = stats.get("risk_mean") or 0.0
        readiness_mean = stats.get("readiness_mean") or 0.0
        dist = (
            abs(budget - budget_mean) / 50.0
            + abs(risk - risk_mean) / 10.0
            + abs(readiness - readiness_mean) / 10.0
        )
        # dist 0 -> 1 (tam yakin), dist 1 -> 0 (cok uzak)
        distance_penalty = max(0.0, 1.0 - dist)

        # Confidence delta: alignment ve distance_penalty carpimi; uc cap 0.20.
        # Negatif alignment confidence dusurur, pozitif yukseltir.
        confidence_delta = alignment * distance_penalty * 0.20
        confidence_delta = max(-0.20, min(0.20, confidence_delta))

        # Insan-okunabilir not.
        approve_pct = int(approve_ratio * 100)
        reject_pct = 100 - approve_pct
        note_parts = [
            f"Datasetimdeki en yakin {stats['k']} vakanin "
            f"%{approve_pct}'i APPROVE, %{reject_pct}'i REJECT."
        ]
        if distance_penalty < 0.5:
            note_parts.append(
                f"(Ancak bu vakalar dagilim olarak senaryomuzdan uzak; "
                f"butce ort. ${budget_mean:.1f}M, readiness ort. {readiness_mean:.1f}; "
                f"agirlik dusuruldu.)"
            )
        if abs(confidence_delta) >= 0.03:
            direction = "yukseldi" if confidence_delta > 0 else "dustu"
            note_parts.append(
                f"Stance '{stance}' icin veri uyumu {alignment:+.2f}; "
                f"confidence {direction} ({confidence_delta:+.2f})."
            )
        note = " ".join(note_parts)

        return {
            "available": True,
            "k": stats["k"],
            "approve_ratio": approve_ratio,
            "alignment": alignment,
            "distance_penalty": distance_penalty,
            "confidence_delta": confidence_delta,
            "note": note,
        }

    def format_for_prompt(
        self,
        budget: float,
        risk: float,
        readiness: float,
        k: int = 20,
    ) -> str:
        """LLM prompt'una eklemek icin insan-okunabilir blok dondur.

        Veriseti yoksa bos string doner (cagiran bunu kontrol etmek zorunda degil;
        bos string prompt'a eklenebilir).
        """
        if not self.is_available:
            return ""

        records, stats = self.find_similar(budget, risk, readiness, k=k)
        if not records or not stats:
            return ""

        decisions_str = ", ".join(
            f"{d}: {c}" for d, c in sorted(stats["decisions"].items())
        )
        br = stats["budget_range"]
        rr = stats["risk_range"]
        rer = stats["readiness_range"]
        return (
            f"## Tarihsel Veri (benzer vakalar)\n"
            f"Veriseti: {stats['total_records']} kayit (kaynak: Agile projeler).\n"
            f"Senaryona en benzer {stats['k']} vaka ozet:\n"
            f"- Outcome dagilimi: {decisions_str}\n"
            f"- Butce araligi: ${br[0]:.0f}M - ${br[1]:.0f}M "
            f"(ortalama ${stats['budget_mean']:.1f}M)\n"
            f"- Risk araligi: {rr[0]:.0f} - {rr[1]:.0f} "
            f"(ortalama {stats['risk_mean']:.1f})\n"
            f"- Readiness araligi: {rer[0]:.0f} - {rer[1]:.0f} "
            f"(ortalama {stats['readiness_mean']:.1f})\n"
            f"\nNOT: Bu dataset yalniz APPROVE/REJECT etiketleri icerir (REVISE yok). "
            f"Senaryon dataset dagiliminin disindaysa, bunu **acikca belirt** ve karari "
            f"hesaplanan analize gore ver — veriden direkt cikarim yapma."
        )
