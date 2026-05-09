from fastapi import APIRouter, Depends, HTTPException

from app.application.exceptions import ScenarioNotFoundError, SimulationNotFoundError
from app.application.use_cases.scenario_query_service import ScenarioQueryService
from app.application.use_cases.scenario_service import ScenarioSimulationService
from app.domain.models import AgentResult, ScenarioInput, ScenarioRecord
from app.domain.services.classifier import ScenarioClassifier
from app.presentation.dependencies import get_scenario_query_service, get_scenario_service
from app.presentation.schemas.scenario import (
    AgentMessageResponse,
    AgentOutputResponse,
    AgentWeightsResponse,
    ClassificationRequest,
    ClassificationResponse,
    CreateScenarioRequest,
    CreateScenarioResponse,
    RoundResponse,
    ScenarioListResponse,
    ScenarioResponse,
    SimulationDetailResponse,
    SimulationDetailedResponse,
    SimulationResponse,
)

router = APIRouter()


def _to_scenario_response(scenario: ScenarioRecord) -> ScenarioResponse:
    return ScenarioResponse(
        id=scenario.id,
        name=scenario.name,
        description=scenario.description,
        budget_million_usd=scenario.budget_million_usd,
        expected_roi_percent=scenario.expected_roi_percent,
        risk_level=scenario.risk_level,
        team_readiness=scenario.team_readiness,
        created_at=scenario.created_at,
    )


def _to_agent_output_response(agent_result: AgentResult) -> AgentOutputResponse:
    return AgentOutputResponse(
        agent_name=agent_result.agent_name,
        score=agent_result.score,
        rationale=agent_result.rationale,
    )


def _to_agent_message_response(msg) -> AgentMessageResponse:
    return AgentMessageResponse(
        agent=msg.agent,
        stance=msg.stance,
        confidence=msg.confidence,
        reasoning=msg.reasoning,
        metrics=msg.metrics,
        round_number=msg.round_number,
    )


@router.get("/scenarios", response_model=ScenarioListResponse)
async def list_scenarios(
    limit: int = 20,
    offset: int = 0,
    service: ScenarioQueryService = Depends(get_scenario_query_service),
) -> ScenarioListResponse:
    items = await service.list_scenarios(limit=limit, offset=offset)
    return ScenarioListResponse(
        items=[_to_scenario_response(item) for item in items],
        limit=limit,
        offset=offset,
    )


@router.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: int,
    service: ScenarioQueryService = Depends(get_scenario_query_service),
) -> ScenarioResponse:
    try:
        scenario = await service.get_scenario(scenario_id)
    except ScenarioNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _to_scenario_response(scenario)


@router.get("/scenarios/{scenario_id}/simulation", response_model=SimulationDetailResponse)
async def get_simulation(
    scenario_id: int,
    service: ScenarioQueryService = Depends(get_scenario_query_service),
) -> SimulationDetailResponse:
    try:
        result = await service.get_simulation(scenario_id)
    except (ScenarioNotFoundError, SimulationNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return SimulationDetailResponse(
        scenario=_to_scenario_response(result.scenario),
        agent_outputs=[_to_agent_output_response(item) for item in result.agent_outputs],
        final_score=result.aggregated_decision.final_score,
        final_decision=result.aggregated_decision.decision.value,
    )


@router.post("/scenarios", response_model=CreateScenarioResponse)
async def create_scenario(
    payload: CreateScenarioRequest,
    service: ScenarioSimulationService = Depends(get_scenario_service),
) -> CreateScenarioResponse:
    scenario_id = await service.create_scenario(
        ScenarioInput(
            name=payload.name,
            description=payload.description,
            budget_million_usd=payload.budget_million_usd,
            expected_roi_percent=payload.expected_roi_percent,
            risk_level=payload.risk_level,
            team_readiness=payload.team_readiness,
        )
    )
    return CreateScenarioResponse(scenario_id=scenario_id)


@router.post("/scenarios/{scenario_id}/simulate", response_model=SimulationResponse)
async def run_simulation(
    scenario_id: int,
    service: ScenarioSimulationService = Depends(get_scenario_service),
) -> SimulationResponse:
    try:
        result = await service.run_simulation(scenario_id)
    except ScenarioNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return SimulationResponse(
        scenario_id=result.scenario_id,
        agent_outputs=[_to_agent_output_response(item) for item in result.agent_outputs],
        final_score=result.aggregated_decision.final_score,
        final_decision=result.aggregated_decision.decision.value,
    )


@router.post("/scenarios/{scenario_id}/simulate/detailed", response_model=SimulationDetailedResponse)
async def run_simulation_detailed(
    scenario_id: int,
    service: ScenarioSimulationService = Depends(get_scenario_service),
) -> SimulationDetailedResponse:
    """Run simulation and return full round-by-round debate transcript."""
    try:
        result = await service.run_simulation(scenario_id)
    except ScenarioNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    rounds = [
        RoundResponse(
            round_number=r.round_number,
            messages=[_to_agent_message_response(m) for m in r.messages],
        )
        for r in result.rounds
    ]

    scenario_type = None
    scenario_type_confidence = None
    classification_reasoning = None
    if result.classification:
        scenario_type = result.classification.primary_type.value
        scenario_type_confidence = result.classification.confidence
        classification_reasoning = result.classification.classification_reasoning

    return SimulationDetailedResponse(
        scenario_id=result.scenario_id,
        rounds=rounds,
        total_rounds=result.total_rounds,
        consensus_reached=result.consensus_reached,
        stability_reached=result.stability_reached,
        final_score=result.aggregated_decision.final_score,
        final_decision=result.aggregated_decision.decision.value,
        scenario_type=scenario_type,
        scenario_type_confidence=scenario_type_confidence,
        classification_reasoning=classification_reasoning,
        agent_weights=result.agent_weights,
    )


# Classifier singleton for reuse
_classifier = ScenarioClassifier()


@router.post("/classify", response_model=ClassificationResponse)
async def classify_scenario(
    payload: ClassificationRequest,
) -> ClassificationResponse:
    """
    Classify a scenario using ML-based analysis.

    Returns the scenario type classification with confidence scores
    and recommended agent weights. This endpoint does not persist
    the scenario - use POST /scenarios for that.
    """
    scenario_input = ScenarioInput(
        name=payload.name,
        description=payload.description,
        budget_million_usd=payload.budget_million_usd,
        expected_roi_percent=payload.expected_roi_percent,
        risk_level=payload.risk_level,
        team_readiness=payload.team_readiness,
    )
    result = _classifier.classify(scenario_input)
    return ClassificationResponse(
        primary_type=result.primary_type.value,
        confidence=result.confidence,
        secondary_type=result.secondary_type.value if result.secondary_type else None,
        type_scores=result.type_scores,
        recommended_weights=AgentWeightsResponse(**result.recommended_weights),
        classification_reasoning=result.classification_reasoning,
    )


@router.get("/scenarios/{scenario_id}/classify", response_model=ClassificationResponse)
async def classify_existing_scenario(
    scenario_id: int,
    service: ScenarioQueryService = Depends(get_scenario_query_service),
) -> ClassificationResponse:
    """Classify an existing scenario by ID."""
    try:
        scenario = await service.get_scenario(scenario_id)
    except ScenarioNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    scenario_input = ScenarioInput(
        name=scenario.name,
        description=scenario.description,
        budget_million_usd=scenario.budget_million_usd,
        expected_roi_percent=scenario.expected_roi_percent,
        risk_level=scenario.risk_level,
        team_readiness=scenario.team_readiness,
    )
    result = _classifier.classify(scenario_input)
    return ClassificationResponse(
        primary_type=result.primary_type.value,
        confidence=result.confidence,
        secondary_type=result.secondary_type.value if result.secondary_type else None,
        type_scores=result.type_scores,
        recommended_weights=AgentWeightsResponse(**result.recommended_weights),
        classification_reasoning=result.classification_reasoning,
    )
