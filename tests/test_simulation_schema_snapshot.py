"""
OpenAPI schema snapshot for the /simulate response contract.

Locks the frontend-facing shape of SimulationResponse + nested models.
If the contract changes intentionally, update EXPECTED_SCHEMAS below
and notify the frontend team.
"""
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


EXPECTED_SCHEMAS = {
    "SimulationResponse": {
        "required": [
            "scenario_id",
            "rounds",
            "total_rounds",
            "consensus_reached",
            "stability_reached",
            "agent_outputs",
            "final_score",
            "final_decision",
        ],
        "properties": {
            "scenario_id",
            "rounds",
            "total_rounds",
            "consensus_reached",
            "stability_reached",
            "agent_outputs",
            "final_score",
            "final_decision",
            "scenario_type",
            "scenario_type_confidence",
            "agent_weights",
        },
    },
    "RoundResponse": {
        "required": ["round_number", "messages"],
        "properties": {"round_number", "messages"},
    },
    "AgentMessageResponse": {
        "required": ["agent", "stance", "confidence", "reasoning", "metrics", "round_number"],
        "properties": {"agent", "stance", "confidence", "reasoning", "metrics", "round_number"},
    },
    "AgentOutputResponse": {
        "required": ["agent_name", "score", "rationale"],
        "properties": {"agent_name", "score", "rationale"},
    },
    "AgentWeightsResponse": {
        "required": ["CEO", "CFO", "HR"],
        "properties": {"CEO", "CFO", "HR"},
    },
}

EXPECTED_STANCE_VALUES = {"support", "oppose", "neutral"}
EXPECTED_DECISION_VALUES = {"APPROVE", "REVISE", "REJECT"}
EXPECTED_SCENARIO_TYPES = {
    "high_growth",
    "cost_optimization",
    "team_expansion",
    "strategic_pivot",
    "maintenance",
}


def _schemas() -> dict:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    return response.json()["components"]["schemas"]


def test_simulation_response_contract_shape():
    schemas = _schemas()
    for name, expected in EXPECTED_SCHEMAS.items():
        assert name in schemas, f"Missing schema: {name}"
        actual = schemas[name]
        assert set(actual.get("required", [])) == expected["required"] if isinstance(
            expected["required"], set
        ) else set(actual.get("required", [])) == set(expected["required"]), (
            f"{name}.required drifted: {actual.get('required')}"
        )
        assert set(actual.get("properties", {}).keys()) == expected["properties"], (
            f"{name}.properties drifted: {set(actual.get('properties', {}).keys())}"
        )


def test_confidence_fields_have_unit_range():
    schemas = _schemas()
    msg = schemas["AgentMessageResponse"]["properties"]["confidence"]
    assert msg.get("minimum") == 0.0 and msg.get("maximum") == 1.0

    sim_conf = schemas["SimulationResponse"]["properties"]["scenario_type_confidence"]
    # Optional field: pydantic emits anyOf with the constrained float branch.
    branches = sim_conf.get("anyOf", [sim_conf])
    bounded = [b for b in branches if b.get("minimum") == 0.0 and b.get("maximum") == 1.0]
    assert bounded, f"scenario_type_confidence missing [0,1] bound: {sim_conf}"


def test_enum_contracts_are_locked():
    schemas = _schemas()

    stance = schemas["AgentMessageResponse"]["properties"]["stance"]
    assert set(stance["enum"]) == EXPECTED_STANCE_VALUES

    decision = schemas["SimulationResponse"]["properties"]["final_decision"]
    assert set(decision["enum"]) == EXPECTED_DECISION_VALUES

    scenario_type = schemas["SimulationResponse"]["properties"]["scenario_type"]
    branches = scenario_type.get("anyOf", [scenario_type])
    enum_branch = next((b for b in branches if "enum" in b), None)
    assert enum_branch is not None, f"scenario_type missing enum: {scenario_type}"
    assert set(enum_branch["enum"]) == EXPECTED_SCENARIO_TYPES


def test_non_empty_list_constraints():
    schemas = _schemas()
    sim = schemas["SimulationResponse"]["properties"]
    assert sim["rounds"].get("minItems") == 1
    assert sim["agent_outputs"].get("minItems") == 1
    assert schemas["RoundResponse"]["properties"]["messages"].get("minItems") == 1
