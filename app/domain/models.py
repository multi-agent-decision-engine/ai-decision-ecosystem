from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Literal


class FinalDecision(str, Enum):
    """Final decision outcome from the aggregator."""
    APPROVE = "APPROVE"
    REVISE = "REVISE"
    REJECT = "REJECT"


# Type alias for agent stance
Stance = Literal["support", "oppose", "neutral"]


@dataclass(frozen=True)
class ScenarioInput:
    """
    Unified scenario input contract for all agents.
    
    Financial (CFO Agent):
      - budget_million_usd: Investment cost in millions (float, > 0)
      - expected_roi_percent: Expected return on investment % (float, any)
    
    HR (HR Agent):
      - team_readiness: Team capability level (int, 1-10)
    
    Strategic (CEO Agent):
      - expected_roi_percent: Strategic fit indicator % (float, any)
      - risk_level: Overall project risk (int, 1-10)
    
    All agents normalize these to 0-1 scales internally.
    """
    name: str
    description: str
    budget_million_usd: float
    expected_roi_percent: float
    risk_level: int
    team_readiness: int


@dataclass(frozen=True)
class ScenarioRecord:
    id: int
    name: str
    description: str
    budget_million_usd: float
    expected_roi_percent: float
    risk_level: int
    team_readiness: int
    created_at: datetime


@dataclass(frozen=True)
class AgentResult:
    """Legacy agent result for backward compatibility with aggregator."""
    agent_name: str
    score: int
    rationale: str


@dataclass(frozen=True)
class AgentMessage:
    """
    Standardized agent communication message following the project protocol.
    
    Each agent produces this message format during discussion rounds.
    Agents can read previous messages and update their stance/confidence.
    
    Attributes:
        agent: Agent identifier (e.g., "CEO", "CFO", "HR")
        stance: Position on the scenario ("support", "oppose", "neutral")
        confidence: Confidence level in the stance (0.0 to 1.0)
        reasoning: Explanation of the agent's analysis and position
        metrics: Agent-specific numerical metrics dict
            - CEO: {"growth_potential": 0-10, "market_alignment": 0-10}
            - CFO: {"risk_score": 0-10, "cost_impact": float, "roi_estimate": float}
            - HR: {"talent_availability": 0-10, "team_impact": 0-10, "workload_score": 0-10}
        round_number: The discussion round this message was produced in (1-indexed)
    """
    agent: str
    stance: Stance
    confidence: float
    reasoning: str
    metrics: dict = field(default_factory=dict)
    round_number: int = 1
    
    def __post_init__(self):
        """Validate field constraints."""
        if self.stance not in ("support", "oppose", "neutral"):
            raise ValueError(f"Invalid stance: {self.stance}. Must be 'support', 'oppose', or 'neutral'.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")
        if self.round_number < 1:
            raise ValueError(f"round_number must be >= 1, got {self.round_number}")
    
    def to_legacy_result(self) -> "AgentResult":
        """
        Convert to legacy AgentResult for backward compatibility with aggregator.
        
        Score mapping:
            - support: confidence * 100
            - neutral: 50
            - oppose: (1 - confidence) * 100
        """
        if self.stance == "support":
            score = int(self.confidence * 100)
        elif self.stance == "oppose":
            score = int((1 - self.confidence) * 100)
        else:  # neutral
            score = 50
        
        return AgentResult(
            agent_name=self.agent,
            score=max(0, min(100, score)),
            rationale=self.reasoning,
        )


def get_agent_metrics(
    previous_messages: list["AgentMessage"] | None,
    agent_name: str,
) -> dict | None:
    """
    Önceki mesajlardan belirli bir agent'ın metriklerini al.
    Birden fazla mesaj varsa en son turunkini döndürür.
    """
    if not previous_messages:
        return None
    agent_msgs = [m for m in previous_messages if m.agent == agent_name]
    if not agent_msgs:
        return None
    latest = max(agent_msgs, key=lambda m: m.round_number)
    return latest.metrics


def get_agent_stance(
    previous_messages: list["AgentMessage"] | None,
    agent_name: str,
) -> tuple[Stance, float] | None:
    """
    Önceki mesajlardan belirli bir agent'ın stance ve confidence'ını al.
    """
    if not previous_messages:
        return None
    agent_msgs = [m for m in previous_messages if m.agent == agent_name]
    if not agent_msgs:
        return None
    latest = max(agent_msgs, key=lambda m: m.round_number)
    return (latest.stance, latest.confidence)


@dataclass(frozen=True)
class AggregatedDecision:
    final_score: float
    decision: FinalDecision
