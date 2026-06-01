from __future__ import annotations

from pathlib import Path

from app.domain.agents.base import Agent
from app.domain.learning.agent_calibrator import AgentCalibrator, AgentWeights
from app.domain.models import AgentMessage, ScenarioInput


_DECISION_TO_STANCE = {
    "APPROVE": "support",
    "REVISE": "neutral",
    "REJECT": "oppose",
}


class CalibratedAgent(Agent):
    """Runtime adapter that applies Phase 2 calibrated weights to an agent."""

    def __init__(self, base_agent: Agent, weights: AgentWeights) -> None:
        self.base_agent = base_agent
        self.weights = weights
        self._calibrator = AgentCalibrator(agent_name=weights.agent_name, verbose=False)
        self._calibrator.weights = weights

    @property
    def agent_name(self) -> str:
        return self.weights.agent_name

    def _build_reasoning_prompt(self, scenario_inputs: ScenarioInput) -> str:
        return self.base_agent._build_reasoning_prompt(scenario_inputs)

    def analyze(
        self,
        scenario_inputs: ScenarioInput,
        previous_messages: list[AgentMessage] | None = None,
    ) -> AgentMessage:
        base_message = self.base_agent.analyze(
            scenario_inputs,
            previous_messages=previous_messages,
        )
        prediction, calibrated_confidence = self._calibrator._predict(
            {
                "budget_million_usd": scenario_inputs.budget_million_usd,
                "expected_roi_percent": scenario_inputs.expected_roi_percent,
                "risk_level": scenario_inputs.risk_level,
                "team_readiness": scenario_inputs.team_readiness,
            }
        )

        stance = _DECISION_TO_STANCE[prediction]
        metrics = dict(base_message.metrics)
        metrics["calibration"] = {
            "prediction": prediction,
            "roi_weight": round(float(self.weights.roi_weight), 6),
            "risk_weight": round(float(self.weights.risk_weight), 6),
            "team_weight": round(float(self.weights.team_weight), 6),
        }

        reasoning = (
            f"{base_message.reasoning} Phase 2 calibration adjusted "
            f"{base_message.agent} stance to {stance} from {prediction} "
            f"(confidence {float(calibrated_confidence):.2f})."
        )

        return AgentMessage(
            agent=base_message.agent,
            stance=stance,
            confidence=round(float(calibrated_confidence), 2),
            reasoning=reasoning,
            metrics=metrics,
            round_number=base_message.round_number,
        )


def load_calibrated_agent(base_agent: Agent, weights_file: str | Path) -> CalibratedAgent:
    calibrator = AgentCalibrator(agent_name=_agent_name_for(base_agent), verbose=False)
    calibrator.load_weights(str(weights_file))
    return CalibratedAgent(base_agent=base_agent, weights=calibrator.weights)


def _agent_name_for(agent: Agent) -> str:
    base = getattr(agent, "base_agent", agent)
    name = base.__class__.__name__
    if name.endswith("Agent"):
        name = name[:-5]
    return name.upper()
