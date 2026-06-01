"""Before / after demo for LLM-augmented agents.

Runs the same scenario with base agents and LLM-wrapped agents. The demo uses
StubLLMClient, so Ollama is not required.

Run:
    python scripts/demo_llm_reasoning.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from app.domain.agents.factory import AgentFactory  # noqa: E402
from app.domain.models import ScenarioInput  # noqa: E402
from app.infrastructure.llm_client import StubLLMClient  # noqa: E402


SCENARIO = ScenarioInput(
    name="Southeast Asia Expansion",
    description="Expand the platform into 3 ASEAN markets within 12 months.",
    budget_million_usd=12.0,
    expected_roi_percent=38.0,
    risk_level=7,
    team_readiness=5,
)


STUB_RESPONSES = {
    "CEO": (
        "The expansion has a real strategic upside because 38% expected ROI "
        "and three new ASEAN markets create a growth option we should not "
        "ignore. I still want a phased rollout because risk is 7/10, so I "
        "would back a six-month pilot before committing the full 12M budget."
    ),
    "CFO": (
        "The risk-adjusted return clears the minimum bar, but a 12M upfront "
        "commitment is too aggressive at risk 7/10. I agree with the CEO on "
        "testing the market, but the budget should unlock by milestone after "
        "the first pilot proves traction."
    ),
    "HR": (
        "Team readiness at 5/10 is the limiting factor, not the market idea. "
        "I prefer the CFO's milestone approach because it gives us time to "
        "hire four senior operators and avoid stretching the current team "
        "across three launches at once."
    ),
}


def _ordered_responses(agents) -> list[str]:
    return [STUB_RESPONSES[a.__class__.__name__[:-5].upper()] for a in agents]


def _print(label: str, message) -> None:
    print(f"\n--- {label} ---")
    print(
        f"Agent: {message.agent}  stance={message.stance}  "
        f"confidence={message.confidence:.2f}"
    )
    print(f"Reasoning: {message.reasoning}")


def main() -> None:
    print("=" * 70)
    print("Scenario:", SCENARIO.name)
    print(
        f"  budget={SCENARIO.budget_million_usd}M  "
        f"ROI={SCENARIO.expected_roi_percent}%  "
        f"risk={SCENARIO.risk_level}/10  "
        f"readiness={SCENARIO.team_readiness}/10"
    )
    print("=" * 70)

    print("\n>>> BEFORE: base agents (template reasoning) <<<")
    base_agents = AgentFactory.create_default_agents()
    round1_base = [agent.analyze(SCENARIO) for agent in base_agents]
    for msg in round1_base:
        _print(f"{msg.agent} round 1", msg)

    print("\n\n>>> AFTER: LLM-augmented agents (stub LLM) <<<")
    stub = StubLLMClient(responses=_ordered_responses(base_agents))
    llm_agents = AgentFactory.create_default_agents(llm_client=stub)
    round1_llm = [agent.analyze(SCENARIO) for agent in llm_agents]
    for msg in round1_llm:
        _print(f"{msg.agent} round 1 (LLM)", msg)

    print("\n\n>>> Round 2: HR responds to CEO + CFO under LLM <<<")
    stub_r2 = StubLLMClient(
        responses=[
            (
                "I stay neutral until the staffing plan is proven, but I agree "
                "with the CEO's phased rollout and the CFO's milestone budget. "
                "If the first six months focus on one pilot market, four senior "
                "hires can lift readiness toward 7/10 before a second market "
                "opens."
            )
        ]
    )
    hr_llm_round2 = AgentFactory.create_default_agents(llm_client=stub_r2)[2]
    msg2 = hr_llm_round2.analyze(SCENARIO, previous_messages=round1_llm[:2])
    _print("HR round 2 (LLM, after CEO+CFO)", msg2)

    print("\n" + "=" * 70)
    print("Key takeaways:")
    print("  - stance / confidence / metrics stay deterministic")
    print("  - LLM only enriches reasoning")
    print("  - contradictory or empty LLM output falls back to the base message")
    print("=" * 70)


if __name__ == "__main__":
    main()
