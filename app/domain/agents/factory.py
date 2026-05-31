import os
from pathlib import Path

from app.domain.agents.base import Agent
from app.domain.agents.calibrated import load_calibrated_agent
from app.domain.agents.ceo_agent import CEOAgent
from app.domain.agents.cfo_agent import CFOAgent
from app.domain.agents.hr_agent import HRAgent


class AgentFactory:
    @staticmethod
    def create_default_agents() -> list[Agent]:
        agents: list[Agent] = [CEOAgent(), CFOAgent(), HRAgent()]
        weights_dir = os.getenv("MADE_AGENT_WEIGHTS_DIR")
        if not weights_dir:
            return agents
        return AgentFactory.create_calibrated_agents(weights_dir=weights_dir, fallback_agents=agents)

    @staticmethod
    def create_calibrated_agents(
        weights_dir: str | Path,
        fallback_agents: list[Agent] | None = None,
    ) -> list[Agent]:
        agents = fallback_agents or [CEOAgent(), CFOAgent(), HRAgent()]
        root = Path(weights_dir)
        calibrated: list[Agent] = []
        for agent in agents:
            weights_file = root / f"{agent.__class__.__name__[:-5].lower()}_real_weights.json"
            if not weights_file.exists():
                return agents
            calibrated.append(load_calibrated_agent(agent, weights_file))
        return calibrated
