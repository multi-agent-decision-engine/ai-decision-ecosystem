import os
from pathlib import Path

from app.domain.agents.base import Agent
from app.domain.agents.calibrated import load_calibrated_agent
from app.domain.agents.ceo_agent import CEOAgent
from app.domain.agents.cfo_agent import CFOAgent
from app.domain.agents.hr_agent import HRAgent
from app.domain.agents.llm_agent import LLMAgent
from app.domain.agents.llm_port import LLMClient
from app.infrastructure.llm_client import OllamaLLMClient


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


class AgentFactory:
    @staticmethod
    def create_default_agents(llm_client: LLMClient | None = None) -> list[Agent]:
        """Create agents, optionally composed as calibrated -> LLM wrappers."""
        agents: list[Agent] = [CEOAgent(), CFOAgent(), HRAgent()]
        weights_dir = os.getenv("MADE_AGENT_WEIGHTS_DIR")
        if weights_dir:
            agents = AgentFactory.create_calibrated_agents(
                weights_dir=weights_dir,
                fallback_agents=agents,
            )

        if llm_client is not None:
            return AgentFactory.wrap_with_llm(agents, llm_client)

        if _truthy(os.getenv("MADE_USE_LLM")):
            return AgentFactory.wrap_with_llm(agents, OllamaLLMClient())

        return agents

    @staticmethod
    def wrap_with_llm(agents: list[Agent], llm_client: LLMClient) -> list[Agent]:
        return [LLMAgent(base_agent=agent, llm_client=llm_client) for agent in agents]

    @staticmethod
    def create_calibrated_agents(
        weights_dir: str | Path,
        fallback_agents: list[Agent] | None = None,
    ) -> list[Agent]:
        agents = fallback_agents or [CEOAgent(), CFOAgent(), HRAgent()]
        root = Path(weights_dir)
        calibrated: list[Agent] = []
        for agent in agents:
            name = _agent_name(agent)
            weights_file = root / f"{name.lower()}_real_weights.json"
            if not weights_file.exists():
                return agents
            calibrated.append(load_calibrated_agent(agent, weights_file))
        return calibrated


def _agent_name(agent: Agent) -> str:
    base = getattr(agent, "base_agent", agent)
    name = base.__class__.__name__
    if name.endswith("Agent"):
        name = name[:-5]
    return name.upper()
