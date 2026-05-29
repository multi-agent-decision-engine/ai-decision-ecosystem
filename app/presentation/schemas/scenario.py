from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


DecisionLabel = Literal["APPROVE", "REVISE", "REJECT"]
ScenarioTypeLabel = Literal[
    "high_growth",
    "cost_optimization",
    "team_expansion",
    "strategic_pivot",
    "maintenance",
]
StanceLabel = Literal["support", "oppose", "neutral"]


class CreateScenarioRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1)
    budget_million_usd: float = Field(gt=0)
    expected_roi_percent: float = Field(ge=0)
    risk_level: int = Field(ge=1, le=10)
    team_readiness: int = Field(ge=1, le=10)


class CreateScenarioResponse(BaseModel):
    scenario_id: int


class AgentOutputResponse(BaseModel):
    agent_name: str
    score: float
    rationale: str


class AgentMessageResponse(BaseModel):
    agent: str
    stance: StanceLabel
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    metrics: dict[str, Any]
    round_number: int


class RoundResponse(BaseModel):
    round_number: int
    messages: list[AgentMessageResponse] = Field(min_length=1)


class ScenarioResponse(BaseModel):
    id: int
    name: str
    description: str
    budget_million_usd: float
    expected_roi_percent: float
    risk_level: int
    team_readiness: int
    created_at: datetime


class ScenarioListResponse(BaseModel):
    items: list[ScenarioResponse]
    limit: int
    offset: int


class AgentWeightsResponse(BaseModel):
    """Recommended agent weights based on scenario type."""
    CEO: float
    CFO: float
    HR: float


class SimulationResponse(BaseModel):
    scenario_id: int
    rounds: list[RoundResponse] = Field(min_length=1)
    total_rounds: int
    consensus_reached: bool
    stability_reached: bool
    agent_outputs: list[AgentOutputResponse] = Field(min_length=1)
    final_score: float
    final_decision: DecisionLabel
    scenario_type: ScenarioTypeLabel | None = None
    scenario_type_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    agent_weights: AgentWeightsResponse | None = None


class SimulationDetailResponse(BaseModel):
    scenario: ScenarioResponse
    agent_outputs: list[AgentOutputResponse]
    final_score: float
    final_decision: DecisionLabel


class SimulationDetailedResponse(BaseModel):
    """Detailed simulation response including full round-by-round debate."""

    scenario_id: int
    rounds: list[RoundResponse]
    total_rounds: int = Field(ge=1)
    consensus_reached: bool
    stability_reached: bool
    final_score: float
    final_decision: str

    # Optional classification info (used to explain weighting)
    scenario_type: str | None = None
    scenario_type_confidence: float | None = None
    classification_reasoning: str | None = None
    agent_weights: dict[str, float] | None = None


# Classification schemas
class ClassificationRequest(BaseModel):
    """Request to classify a scenario without saving it."""
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1)
    budget_million_usd: float = Field(gt=0)
    expected_roi_percent: float = Field(ge=0)
    risk_level: int = Field(ge=1, le=10)
    team_readiness: int = Field(ge=1, le=10)


class ClassificationResponse(BaseModel):
    """Scenario classification result with ML-derived insights."""
    primary_type: str = Field(description="Primary scenario classification")
    confidence: float = Field(ge=0.0, le=1.0, description="Classification confidence")
    secondary_type: str | None = Field(description="Secondary classification if applicable")
    type_scores: dict[str, float] = Field(description="Confidence scores for all types")
    recommended_weights: AgentWeightsResponse = Field(description="Suggested agent weights")
    classification_reasoning: str = Field(description="Human-readable reasoning")
