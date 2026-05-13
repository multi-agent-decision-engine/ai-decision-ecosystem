from datetime import datetime

from pydantic import BaseModel, Field


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
    score: int
    rationale: str


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


class SimulationResponse(BaseModel):
    scenario_id: int
    agent_outputs: list[AgentOutputResponse]
    final_score: float
    final_decision: str


class SimulationDetailResponse(BaseModel):
    scenario: ScenarioResponse
    agent_outputs: list[AgentOutputResponse]
    final_score: float
    final_decision: str


# Classification schemas
class ClassificationRequest(BaseModel):
    """Request to classify a scenario without saving it."""
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1)
    budget_million_usd: float = Field(gt=0)
    expected_roi_percent: float = Field(ge=0)
    risk_level: int = Field(ge=1, le=10)
    team_readiness: int = Field(ge=1, le=10)


class AgentWeightsResponse(BaseModel):
    """Recommended agent weights based on scenario type."""
    CEO: float
    CFO: float
    HR: float


class ClassificationResponse(BaseModel):
    """Scenario classification result with ML-derived insights."""
    primary_type: str = Field(description="Primary scenario classification")
    confidence: float = Field(ge=0.0, le=1.0, description="Classification confidence")
    secondary_type: str | None = Field(description="Secondary classification if applicable")
    type_scores: dict[str, float] = Field(description="Confidence scores for all types")
    recommended_weights: AgentWeightsResponse = Field(description="Suggested agent weights")
    classification_reasoning: str = Field(description="Human-readable reasoning")
