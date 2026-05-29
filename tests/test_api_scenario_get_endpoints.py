from datetime import datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.application.exceptions import ScenarioNotFoundError, SimulationNotFoundError
from app.application.models import RoundBasedSimulationResult, RoundResult, SimulationReadResult
from app.domain.models import AgentMessage, AgentResult, AggregatedDecision, FinalDecision, ScenarioInput, ScenarioRecord
from app.main import app
from app.presentation.dependencies import get_scenario_query_service, get_scenario_service


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


class FakeScenarioSimulationService:
    async def create_scenario(self, scenario: ScenarioInput) -> int:
        return 1

    async def run_simulation(self, scenario_id: int) -> RoundBasedSimulationResult:
        round_one = RoundResult(
            round_number=1,
            messages=[
                AgentMessage(
                    agent="CEO",
                    stance="support",
                    confidence=0.82,
                    reasoning="Strategic upside is strong.",
                    metrics={"growth_potential": 8},
                    round_number=1,
                ),
                AgentMessage(
                    agent="CFO",
                    stance="neutral",
                    confidence=0.64,
                    reasoning="ROI is acceptable but budget risk remains.",
                    metrics={"risk_score": 5},
                    round_number=1,
                ),
            ],
        )
        round_two = RoundResult(
            round_number=2,
            messages=[
                AgentMessage(
                    agent="CEO",
                    stance="support",
                    confidence=0.78,
                    reasoning="CEO still supports after CFO risk note.",
                    metrics={"growth_potential": 8},
                    round_number=2,
                ),
                AgentMessage(
                    agent="CFO",
                    stance="neutral",
                    confidence=0.66,
                    reasoning="CFO remains cautious after CEO input.",
                    metrics={"risk_score": 5},
                    round_number=2,
                ),
            ],
        )

        return RoundBasedSimulationResult(
            scenario_id=scenario_id,
            rounds=[round_one, round_two],
            total_rounds=2,
            consensus_reached=False,
            stability_reached=True,
            final_messages=round_two.messages,
            agent_outputs=[
                AgentResult(agent_name="CEO", score=78, rationale="CEO still supports after CFO risk note."),
                AgentResult(agent_name="CFO", score=50, rationale="CFO remains cautious after CEO input."),
            ],
            aggregated_decision=AggregatedDecision(
                final_score=64.0,
                decision=FinalDecision.REVISE,
            ),
            classification=SimpleNamespace(
                primary_type=SimpleNamespace(value="strategic_pivot"),
                confidence=0.72,
            ),
            agent_weights={"CEO": 0.45, "CFO": 0.30, "HR": 0.25},
        )


class FakeScenarioNotFoundSimulationService(FakeScenarioSimulationService):
    async def run_simulation(self, scenario_id: int) -> RoundBasedSimulationResult:
        raise ScenarioNotFoundError(f"Scenario {scenario_id} not found")


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


def test_run_simulation_returns_detailed_round_response() -> None:
    app.dependency_overrides[get_scenario_service] = lambda: FakeScenarioSimulationService()
    client = TestClient(app)

    response = client.post("/api/v1/scenarios/1/simulate")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario_id"] == 1
    assert payload["consensus_reached"] is False
    assert payload["stability_reached"] is True
    assert payload["final_score"] == 64.0
    assert payload["final_decision"] == "REVISE"
    assert payload["scenario_type"] is not None
    assert payload["scenario_type"] == "strategic_pivot"
    assert payload["scenario_type_confidence"] == 0.72
    assert payload["agent_weights"] == {"CEO": 0.45, "CFO": 0.30, "HR": 0.25}
    assert set(payload["agent_weights"]) == {"CEO", "CFO", "HR"}
    assert len(payload["rounds"]) == 2
    assert payload["rounds"][0]["round_number"] == 1
    assert payload["rounds"][0]["messages"][0]["agent"] == "CEO"
    assert payload["rounds"][0]["messages"][0]["stance"] == "support"
    assert payload["rounds"][0]["messages"][0]["metrics"] == {"growth_potential": 8}
    assert len(payload["agent_outputs"]) == 2

    app.dependency_overrides.clear()


def test_run_simulation_returns_404_when_scenario_not_found() -> None:
    app.dependency_overrides[get_scenario_service] = lambda: FakeScenarioNotFoundSimulationService()
    client = TestClient(app)

    response = client.post("/api/v1/scenarios/999/simulate")

    assert response.status_code == 404
    assert response.json()["detail"] == "Scenario 999 not found"

    app.dependency_overrides.clear()
