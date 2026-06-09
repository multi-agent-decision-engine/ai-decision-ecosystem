"""Ad-hoc: dataset-grounded deterministik debate'i lokal goster (Docker'siz).

Mevcut deterministik agent'lar Round 2+ icin DatasetRetriever ile gercek
tarihsel verileri okur ve confidence'larini buna gore ayarlar. Bu script
ScenarioInput'u dogrudan ceker, dataset uzerinden agent'i kosturur ve
Round-bazinda neler oluyor gosterir.
"""
from __future__ import annotations

from app.domain.agents.ceo_agent import CEOAgent
from app.domain.agents.cfo_agent import CFOAgent
from app.domain.agents.hr_agent import HRAgent
from app.domain.models import ScenarioInput

SCENARIOS = [
    # (name, budget, roi, risk, readiness, kisa-yorum)
    ("Demo Final Smoke (id=10)", 5.0, 30.0, 5, 7, "Demo senaryomuz — dataset disinda"),
    ("Dataset Orta (budget=30, risk=4, readiness=3)", 30.0, 25.0, 4, 3, "Dataset dagilimina yakin"),
    ("Dataset Riskli (budget=40, risk=5, readiness=2)", 40.0, 25.0, 5, 2, "Dataset disinda, riskli profil"),
]


def run(scenario: ScenarioInput, n_rounds: int = 3) -> None:
    agents = [CEOAgent(), CFOAgent(), HRAgent()]
    print(f"\n{'=' * 80}\nSenaryo: {scenario.name}")
    print(f"  budget={scenario.budget_million_usd}M roi={scenario.expected_roi_percent}% "
          f"risk={scenario.risk_level} readiness={scenario.team_readiness}")
    print('=' * 80)

    history = []
    for rnd in range(1, n_rounds + 1):
        print(f"\n--- Round {rnd} ---")
        round_msgs = []
        for agent in agents:
            msg = agent.analyze(scenario, previous_messages=history if history else None)
            round_msgs.append(msg)
            print(f"  {msg.agent}: stance={msg.stance} confidence={msg.confidence:.2f}")
            if rnd > 1:
                # son satirin "Capraz analiz" / "Cross-analysis" parcasini goster
                reasoning = msg.reasoning
                marker = "Cross-analysis:" if "Cross-analysis:" in reasoning else "Çapraz analiz:"
                if marker in reasoning:
                    after = reasoning.split(marker, 1)[1].strip()
                    # Sonuc kismindan once kes
                    for stop in [" Sonuç:", " Result:", " Sonuc:"]:
                        if stop in after:
                            after = after.split(stop, 1)[0]
                    print(f"    >>> {marker} {after[:300]}")
        history.extend(round_msgs)


def main() -> None:
    for name, budget, roi, risk, readiness, hint in SCENARIOS:
        scenario = ScenarioInput(
            name=name,
            description=hint,
            budget_million_usd=budget,
            expected_roi_percent=roi,
            risk_level=risk,
            team_readiness=readiness,
        )
        run(scenario, n_rounds=3)


if __name__ == "__main__":
    main()
