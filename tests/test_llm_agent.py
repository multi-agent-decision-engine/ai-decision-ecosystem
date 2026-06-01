"""LLMAgent wrapper unit tests."""

from __future__ import annotations

import pytest

from app.domain.agents.ceo_agent import CEOAgent
from app.domain.agents.hr_agent import HRAgent
from app.domain.agents.llm_agent import (
    LLMAgent,
    _detect_stance_contradiction,
    _sanitize_llm_output,
)
from app.domain.agents.llm_port import LLMUnavailableError
from app.domain.models import ScenarioInput
from app.infrastructure.llm_client import StubLLMClient


def _scenario(**overrides) -> ScenarioInput:
    defaults = dict(
        name="LLM Smoke Scenario",
        description="A scenario used to drive LLM agent tests.",
        budget_million_usd=5.0,
        expected_roi_percent=42.0,
        risk_level=3,
        team_readiness=8,
    )
    defaults.update(overrides)
    return ScenarioInput(**defaults)


def test_llm_agent_replaces_reasoning_but_preserves_stance_and_metrics():
    base = CEOAgent()
    llm = StubLLMClient(responses=["I see a strong strategic opportunity."])
    agent = LLMAgent(base_agent=base, llm_client=llm)

    scenario = _scenario(expected_roi_percent=45.0, risk_level=2, team_readiness=8)
    base_msg = base.analyze(scenario)
    llm_msg = agent.analyze(scenario)

    assert llm_msg.agent == base_msg.agent == "CEO"
    assert llm_msg.stance == base_msg.stance
    assert llm_msg.confidence == base_msg.confidence
    for key, value in base_msg.metrics.items():
        assert llm_msg.metrics[key] == value
    assert llm_msg.metrics["llm"]["source"] == "StubLLMClient"
    assert llm_msg.metrics["llm"]["fallback_used"] is False
    assert llm_msg.metrics["llm"]["sanitized"] is False
    assert llm_msg.metrics["llm"]["stance_contradiction"] is False
    assert llm_msg.reasoning == "I see a strong strategic opportunity."
    assert llm_msg.reasoning != base_msg.reasoning


def test_llm_agent_falls_back_to_base_when_llm_raises():
    base = CEOAgent()
    llm = StubLLMClient(raise_on_call=LLMUnavailableError("network down"))
    agent = LLMAgent(base_agent=base, llm_client=llm)
    scenario = _scenario()

    base_msg = base.analyze(scenario)
    llm_msg = agent.analyze(scenario)

    assert llm_msg == base_msg
    assert "llm" not in llm_msg.metrics


def test_llm_agent_falls_back_when_llm_returns_empty_text():
    base = CEOAgent()
    llm = StubLLMClient(responses=["   "])
    agent = LLMAgent(base_agent=base, llm_client=llm)
    scenario = _scenario()

    base_msg = base.analyze(scenario)
    llm_msg = agent.analyze(scenario)

    assert llm_msg == base_msg


def test_llm_prompt_includes_scenario_persona_and_structured_analysis():
    base = HRAgent()
    llm = StubLLMClient(responses=["HR LLM reasoning."])
    agent = LLMAgent(base_agent=base, llm_client=llm)

    scenario = _scenario(name="Recruitment Surge", risk_level=8, team_readiness=4)
    agent.analyze(scenario)

    assert llm.calls
    prompt = llm.calls[0]["prompt"]
    assert "CHRO" in prompt or "IK" in prompt or "HR" in prompt
    assert "burnout" in prompt.lower() or "kapasite" in prompt.lower()
    assert "Recruitment Surge" in prompt
    assert "risk seviyesi (1-10): 8" in prompt
    assert "tak" in prompt.lower()
    assert "stance:" in prompt
    assert "1. tur" in prompt.lower() or "mesaj yok" in prompt.lower()
    assert llm.calls[0]["agent_name"] == "HR"
    assert llm.calls[0]["scenario_name"] == "Recruitment Surge"


def test_llm_prompt_includes_prior_messages_with_persona_hint_in_round_two():
    base = HRAgent()
    llm = StubLLMClient(responses=["Round-2 HR reasoning."])
    agent = LLMAgent(base_agent=base, llm_client=llm)
    scenario = _scenario()

    ceo_round1 = CEOAgent().analyze(scenario)
    agent.analyze(scenario, previous_messages=[ceo_round1])

    prompt = llm.calls[0]["prompt"]
    assert "Tart" in prompt
    assert "CEO" in prompt
    assert "vizyoner" in prompt.lower() or "stratejik" in prompt.lower()
    assert ceo_round1.stance in prompt
    assert ceo_round1.reasoning in prompt
    assert "kat" in prompt.lower()


def test_llm_prompt_round_one_omits_cross_reference_command():
    base = CEOAgent()
    llm = StubLLMClient(responses=["round 1 reasoning"])
    agent = LLMAgent(base_agent=base, llm_client=llm)

    agent.analyze(_scenario())
    prompt = llm.calls[0]["prompt"]
    assert "- Tur" not in prompt
    assert "1. tur" in prompt


def test_sanitize_strips_code_fence_and_markdown_headers():
    raw = "```\n## Decision\nI support this because ROI is sufficient.\n```"
    cleaned = _sanitize_llm_output(raw)
    assert "```" not in cleaned
    assert "## Decision" not in cleaned
    assert "I support this because ROI is sufficient." in cleaned


def test_sanitize_unwraps_json_reasoning_envelope():
    raw = '"reasoning": "There is a strategic opportunity."'
    cleaned = _sanitize_llm_output(raw)
    assert cleaned == "There is a strategic opportunity."


def test_sanitize_removes_bullet_markers():
    raw = "- first argument\n- second argument"
    cleaned = _sanitize_llm_output(raw)
    assert cleaned.startswith("first argument")
    assert "- " not in cleaned


def test_sanitize_flag_set_when_text_changed():
    base = CEOAgent()
    llm = StubLLMClient(responses=["```\nText\n```"])
    agent = LLMAgent(base_agent=base, llm_client=llm)
    msg = agent.analyze(_scenario())
    assert msg.metrics["llm"]["sanitized"] is True
    assert "```" not in msg.reasoning


@pytest.mark.parametrize(
    "stance,text,expected",
    [
        ("support", "I support this and we should move ahead.", False),
        ("support", "I reject this because the budget is too risky.", True),
        ("oppose", "I reject this because risk is too high.", False),
        ("oppose", "I support this because ROI is convincing.", True),
        ("neutral", "I am not ready to decide; I need more data.", False),
        ("neutral", "I support this and we should move ahead.", True),
        ("neutral", "I reject this because risk is too high.", True),
        ("support", "I first considered rejecting this, but I support it.", False),
    ],
)
def test_detect_stance_contradiction(stance, text, expected):
    assert _detect_stance_contradiction(stance, text) is expected


def test_llm_agent_falls_back_when_text_contradicts_base_stance():
    base = CEOAgent()
    scenario = _scenario(expected_roi_percent=80.0, risk_level=2, team_readiness=9)
    llm = StubLLMClient(responses=["I reject this because it is a dead end."])
    agent = LLMAgent(base_agent=base, llm_client=llm)

    base_msg = base.analyze(scenario)
    msg = agent.analyze(scenario)

    assert msg == base_msg
    assert "llm" not in msg.metrics
