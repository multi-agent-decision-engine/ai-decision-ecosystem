import pytest
from app.domain.models import AgentMessage, ScenarioInput
from app.domain.agents.base import Agent
from app.domain.services.discussion_orchestrator import DiscussionOrchestrator


class MockAgent(Agent):
    """
    Testler için sahte veri üreten MockAgent sınıfı.
    Gelen 'previous_messages' listesinin uzunluğunu kaydeder ki assertion yapabilelim.
    """
    def __init__(self, name: str):
        self.name = name
        self.seen_messages_count = []

    def _build_reasoning_prompt(self, scenario_inputs: ScenarioInput) -> str:
        return "mock prompt"

    def analyze(
        self, 
        scenario_inputs: ScenarioInput,
        previous_messages: list[AgentMessage] | None = None,
    ) -> AgentMessage:
        msg_count = len(previous_messages) if previous_messages else 0
        self.seen_messages_count.append(msg_count)
        
        return AgentMessage(
            agent=self.name,
            stance="support",
            confidence=0.8,
            reasoning=f"{self.name} analyzing {scenario_inputs.name}",
            metrics={}
        )


@pytest.fixture
def mock_scenario() -> ScenarioInput:
    return ScenarioInput(
        name="Test Scenario",
        description="A scenario for testing",
        budget_million_usd=1.5,
        expected_roi_percent=15.0,
        risk_level=5,
        team_readiness=8
    )


def test_orchestrator_returns_messages_for_all_rounds(mock_scenario: ScenarioInput) -> None:
    orchestrator = DiscussionOrchestrator()
    agents = [MockAgent("AgentA"), MockAgent("AgentB")]
    
    rounds = 2
    messages = orchestrator.run_discussion(scenario=mock_scenario, agents=agents, rounds=rounds)
    
    # 2 tur * 2 ajan = 4 mesaj
    assert len(messages) == 4
    
    # Tur bilgilerinin doğru atanıp atanmadığını kontrol edelim
    assert messages[0].round_number == 1
    assert messages[1].round_number == 1
    assert messages[2].round_number == 2
    assert messages[3].round_number == 2


def test_orchestrator_each_agent_called_per_round(mock_scenario: ScenarioInput) -> None:
    orchestrator = DiscussionOrchestrator()
    agent_a = MockAgent("AgentA")
    agent_b = MockAgent("AgentB")
    
    orchestrator.run_discussion(scenario=mock_scenario, agents=[agent_a, agent_b], rounds=2)
    
    # Her ajan iki turda da iki kez çalışmış olmalı
    assert len(agent_a.seen_messages_count) == 2
    assert len(agent_b.seen_messages_count) == 2


def test_orchestrator_passes_previous_messages_correctly(mock_scenario: ScenarioInput) -> None:
    orchestrator = DiscussionOrchestrator()
    agent_a = MockAgent("AgentA")
    agent_b = MockAgent("AgentB")
    
    orchestrator.run_discussion(scenario=mock_scenario, agents=[agent_a, agent_b], rounds=2)
    
    # 1. Tur: AgentA -> 0 mesaj görür
    assert agent_a.seen_messages_count[0] == 0
    # 1. Tur: AgentB -> 1 mesaj görür (AgentA'nın 1. tur mesajı)
    assert agent_b.seen_messages_count[0] == 1
    
    # 2. Tur: AgentA -> 2 mesaj görür (1. turdaki kendi mesajı + AgentB'nin 1. tur mesajı)
    assert agent_a.seen_messages_count[1] == 2
    # 2. Tur: AgentB -> 3 mesaj görür (1. turun tümü + AgentA'nın 2. tur mesajı)
    assert agent_b.seen_messages_count[1] == 3


def test_orchestrator_valid_scenario_input(mock_scenario: ScenarioInput) -> None:
    orchestrator = DiscussionOrchestrator()
    agents = [MockAgent("AgentA")]
    
    try:
        messages = orchestrator.run_discussion(scenario=mock_scenario, agents=agents, rounds=1)
        assert len(messages) == 1
        assert messages[0].reasoning == "AgentA analyzing Test Scenario"
    except Exception as e:
        pytest.fail(f"Geçerli ScenarioInput ile çalışırken hata fırlattı: {e}")
