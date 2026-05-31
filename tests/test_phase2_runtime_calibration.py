import json
from pathlib import Path

from app.domain.agents.calibrated import CalibratedAgent
from app.domain.agents.factory import AgentFactory
from app.domain.models import ScenarioInput


def _write_weight_file(path: Path, agent_name: str) -> None:
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


def test_agent_factory_keeps_default_agents_without_weights_env(monkeypatch):
    monkeypatch.delenv("MADE_AGENT_WEIGHTS_DIR", raising=False)

    agents = AgentFactory.create_default_agents()

    assert [agent.__class__.__name__ for agent in agents] == [
        "CEOAgent",
        "CFOAgent",
        "HRAgent",
    ]


def test_agent_factory_loads_phase2_weights_from_env(tmp_path, monkeypatch):
    for agent_name in ("CEO", "CFO", "HR"):
        _write_weight_file(tmp_path / f"{agent_name.lower()}_real_weights.json", agent_name)
    monkeypatch.setenv("MADE_AGENT_WEIGHTS_DIR", str(tmp_path))

    agents = AgentFactory.create_default_agents()

    assert len(agents) == 3
    assert all(isinstance(agent, CalibratedAgent) for agent in agents)

    scenario = ScenarioInput(
        name="Runtime calibration smoke test",
        description="Verifies Phase 2 weights influence runtime agent messages.",
        budget_million_usd=5.0,
        expected_roi_percent=40.0,
        risk_level=2,
        team_readiness=8,
    )
    message = agents[0].analyze(scenario)

    assert message.agent == "CEO"
    assert message.metrics["calibration"]["prediction"] in {"APPROVE", "REVISE", "REJECT"}
    assert "Phase 2 calibration adjusted" in message.reasoning


def test_agent_factory_falls_back_when_any_weight_file_is_missing(tmp_path, monkeypatch):
    _write_weight_file(tmp_path / "ceo_real_weights.json", "CEO")
    _write_weight_file(tmp_path / "cfo_real_weights.json", "CFO")
    monkeypatch.setenv("MADE_AGENT_WEIGHTS_DIR", str(tmp_path))

    agents = AgentFactory.create_default_agents()

    assert [agent.__class__.__name__ for agent in agents] == [
        "CEOAgent",
        "CFOAgent",
        "HRAgent",
    ]


def test_gitignore_excludes_phase2_training_artifacts():
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert "weights/" in gitignore.splitlines()
