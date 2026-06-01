"""AgentFactory LLM and calibration composition tests."""

from __future__ import annotations

import json
from pathlib import Path

from app.domain.agents.calibrated import CalibratedAgent
from app.domain.agents.ceo_agent import CEOAgent
from app.domain.agents.cfo_agent import CFOAgent
from app.domain.agents.factory import AgentFactory
from app.domain.agents.hr_agent import HRAgent
from app.domain.agents.llm_agent import LLMAgent
from app.infrastructure.llm_client import StubLLMClient


def _write_weight(path: Path, agent_name: str) -> None:
    path.write_text(
        json.dumps(
            {
                "agent_name": agent_name,
                "roi_weight": 0.5,
                "risk_weight": 0.3,
                "team_weight": 0.2,
                "confidence_base": 0.65,
                "confidence_scaling": 1.0,
            }
        ),
        encoding="utf-8",
    )


def test_factory_returns_plain_agents_without_env(monkeypatch):
    monkeypatch.delenv("MADE_USE_LLM", raising=False)
    monkeypatch.delenv("MADE_AGENT_WEIGHTS_DIR", raising=False)

    agents = AgentFactory.create_default_agents()

    assert [type(agent) for agent in agents] == [CEOAgent, CFOAgent, HRAgent]


def test_factory_returns_plain_agents_when_env_is_falsy(monkeypatch):
    monkeypatch.delenv("MADE_AGENT_WEIGHTS_DIR", raising=False)
    for falsy in ("", "0", "false", "no", "off", "FALSE"):
        monkeypatch.setenv("MADE_USE_LLM", falsy)
        agents = AgentFactory.create_default_agents()
        assert all(not isinstance(agent, LLMAgent) for agent in agents)


def test_factory_wraps_with_llm_when_env_is_truthy(monkeypatch):
    monkeypatch.delenv("MADE_AGENT_WEIGHTS_DIR", raising=False)
    monkeypatch.setenv("MADE_USE_LLM", "1")

    agents = AgentFactory.create_default_agents()

    assert len(agents) == 3
    assert all(isinstance(agent, LLMAgent) for agent in agents)
    assert [agent.base_agent.__class__ for agent in agents] == [
        CEOAgent,
        CFOAgent,
        HRAgent,
    ]


def test_factory_accepts_explicit_llm_client_override(monkeypatch):
    monkeypatch.delenv("MADE_USE_LLM", raising=False)
    monkeypatch.delenv("MADE_AGENT_WEIGHTS_DIR", raising=False)
    stub = StubLLMClient(default_response="explicit DI stub")

    agents = AgentFactory.create_default_agents(llm_client=stub)

    assert all(isinstance(agent, LLMAgent) for agent in agents)
    assert all(agent.llm_client is stub for agent in agents)


def test_factory_composes_calibration_before_llm(tmp_path, monkeypatch):
    for agent_name in ("CEO", "CFO", "HR"):
        _write_weight(tmp_path / f"{agent_name.lower()}_real_weights.json", agent_name)
    monkeypatch.setenv("MADE_AGENT_WEIGHTS_DIR", str(tmp_path))
    monkeypatch.setenv("MADE_USE_LLM", "1")

    agents = AgentFactory.create_default_agents()

    assert all(isinstance(agent, LLMAgent) for agent in agents)
    assert all(isinstance(agent.base_agent, CalibratedAgent) for agent in agents)
    assert [agent.base_agent.base_agent.__class__ for agent in agents] == [
        CEOAgent,
        CFOAgent,
        HRAgent,
    ]
