from datetime import datetime

from fastapi.testclient import TestClient

from app.application.exceptions import ScenarioNotFoundError, SimulationNotFoundError
from app.application.models import SimulationReadResult
from app.domain.models import AgentResult, AggregatedDecision, FinalDecision, ScenarioRecord
from app.main import app
from app.presentation.dependencies import get_scenario_query_service, get_scenario_service

from app.application.models import RoundBasedSimulationResult, RoundResult
from app.domain.models import AgentMessage


class FakeScenarioQueryService:
    def __init__(self) -> None:
        self.scenario = ScenarioRecord(
            id=1,
            name="Expansion",
            description="Expand to new market",
            budget_million_usd=4.0,
            expected_roi_percent=22.0,
            risk_level=4,
            team_readiness=7,
            created_at=datetime(2026, 2, 26, 10, 0, 0),
        )

    async def list_scenarios(self, limit: int = 20, offset: int = 0):
        return [self.scenario][offset : offset + limit]

    async def get_scenario(self, scenario_id: int):
        return self.scenario

    async def get_simulation(self, scenario_id: int) -> SimulationReadResult:
        return SimulationReadResult(
            scenario=self.scenario,
            agent_outputs=[
                AgentResult(agent_name="CEO", score=80, rationale="ok"),
                AgentResult(agent_name="CFO", score=70, rationale="ok"),
                AgentResult(agent_name="HR", score=75, rationale="ok"),
            ],
            aggregated_decision=AggregatedDecision(
                final_score=75.0,
                decision=FinalDecision.APPROVE,
            ),
        )


class FakeScenarioNotFoundQueryService(FakeScenarioQueryService):
    async def get_scenario(self, scenario_id: int):
        raise ScenarioNotFoundError(f"Scenario {scenario_id} not found")


class FakeSimulationNotFoundQueryService(FakeScenarioQueryService):
    async def get_simulation(self, scenario_id: int) -> SimulationReadResult:
        raise SimulationNotFoundError(f"Simulation for scenario {scenario_id} not found")


def test_get_list_scenarios_happy_path() -> None:
    app.dependency_overrides[get_scenario_query_service] = lambda: FakeScenarioQueryService()
    client = TestClient(app)

    response = client.get("/api/v1/scenarios")

    assert response.status_code == 200
    payload = response.json()
    assert payload["limit"] == 20
    assert payload["offset"] == 0
    assert len(payload["items"]) == 1
    assert payload["items"][0]["id"] == 1

    app.dependency_overrides.clear()


def test_get_scenario_detail_happy_path() -> None:
    app.dependency_overrides[get_scenario_query_service] = lambda: FakeScenarioQueryService()
    client = TestClient(app)

    response = client.get("/api/v1/scenarios/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["name"] == "Expansion"

    app.dependency_overrides.clear()


def test_get_simulation_happy_path() -> None:
    app.dependency_overrides[get_scenario_query_service] = lambda: FakeScenarioQueryService()
    client = TestClient(app)

    response = client.get("/api/v1/scenarios/1/simulation")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario"]["id"] == 1
    assert len(payload["agent_outputs"]) == 3
    assert payload["final_decision"] == "APPROVE"

    app.dependency_overrides.clear()


def test_get_scenario_detail_returns_404_when_not_found() -> None:
    app.dependency_overrides[get_scenario_query_service] = lambda: FakeScenarioNotFoundQueryService()
    client = TestClient(app)

    response = client.get("/api/v1/scenarios/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Scenario 999 not found"

    app.dependency_overrides.clear()


def test_get_simulation_returns_404_when_not_run() -> None:
    app.dependency_overrides[get_scenario_query_service] = lambda: FakeSimulationNotFoundQueryService()
    client = TestClient(app)

    response = client.get("/api/v1/scenarios/1/simulation")

    assert response.status_code == 404
    assert response.json()["detail"] == "Simulation for scenario 1 not found"

    app.dependency_overrides.clear()


class FakeScenarioSimulationService:
    async def run_simulation(self, scenario_id: int, n_rounds: int = 2, use_classification: bool = True):
        # Minimal deterministic transcript for UI/API testing
        round1 = RoundResult(
            round_number=1,
            messages=[
                AgentMessage(agent="CEO", stance="support", confidence=0.8, reasoning="CEO round1", metrics={"growth_potential": 8.0}, round_number=1),
                AgentMessage(agent="CFO", stance="neutral", confidence=0.6, reasoning="CFO round1", metrics={"risk_score": 6.0}, round_number=1),
                AgentMessage(agent="HR", stance="support", confidence=0.7, reasoning="HR round1", metrics={"team_impact": 7.0}, round_number=1),
            ],
        )
        round2 = RoundResult(
            round_number=2,
            messages=[
                AgentMessage(agent="CEO", stance="neutral", confidence=0.55, reasoning="CEO round2", metrics={"growth_potential": 7.0}, round_number=2),
                AgentMessage(agent="CFO", stance="neutral", confidence=0.62, reasoning="CFO round2", metrics={"risk_score": 6.5}, round_number=2),
                AgentMessage(agent="HR", stance="support", confidence=0.72, reasoning="HR round2", metrics={"team_impact": 7.2}, round_number=2),
            ],
        )

        agent_outputs = [m.to_legacy_result() for m in round2.messages]
        aggregated = AggregatedDecision(final_score=66.0, decision=FinalDecision.REVISE)

        return RoundBasedSimulationResult(
            scenario_id=scenario_id,
            rounds=[round1, round2],
            total_rounds=2,
            consensus_reached=False,
            stability_reached=False,
            final_messages=round2.messages,
            agent_outputs=agent_outputs,
            aggregated_decision=aggregated,
            classification=None,
            agent_weights=None,
        )


def test_post_simulate_detailed_returns_rounds() -> None:
    app.dependency_overrides[get_scenario_service] = lambda: FakeScenarioSimulationService()
    client = TestClient(app)

    response = client.post("/api/v1/scenarios/1/simulate/detailed")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario_id"] == 1
    assert payload["total_rounds"] == 2
    assert len(payload["rounds"]) == 2
    assert payload["rounds"][0]["round_number"] == 1
    assert len(payload["rounds"][0]["messages"]) == 3
    assert payload["final_decision"] == "REVISE"

    app.dependency_overrides.clear()
