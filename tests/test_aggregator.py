from app.domain.models import AgentMessage, FinalDecision
from app.domain.services.aggregator import DecisionAggregator


def test_aggregator_returns_approve_for_high_average() -> None:
    aggregator = DecisionAggregator()
    result = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="support", confidence=0.90, reasoning="", metrics={}),
            AgentMessage(agent="CFO", stance="support", confidence=0.85, reasoning="", metrics={}),
            AgentMessage(agent="HR", stance="support", confidence=0.80, reasoning="", metrics={}),
        ]
    )

    assert result.final_score == 85.0
    assert result.decision == FinalDecision.APPROVE


def test_aggregator_returns_revise_for_mid_average() -> None:
    aggregator = DecisionAggregator()
    result = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="support", confidence=0.60, reasoning="", metrics={}),
            AgentMessage(agent="CFO", stance="neutral", confidence=0.50, reasoning="", metrics={}),
            AgentMessage(agent="HR", stance="support", confidence=0.55, reasoning="", metrics={}),
        ]
    )

    assert result.final_score == 55.0
    assert result.decision == FinalDecision.REVISE


def test_aggregator_returns_reject_for_low_average() -> None:
    aggregator = DecisionAggregator()
    result = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="oppose", confidence=0.70, reasoning="", metrics={}),
            AgentMessage(agent="CFO", stance="oppose", confidence=0.60, reasoning="", metrics={}),
            AgentMessage(agent="HR", stance="oppose", confidence=0.65, reasoning="", metrics={}),
        ]
    )

    assert result.final_score == 35.0
    assert result.decision == FinalDecision.REJECT


def test_aggregator_boundary_approve_threshold() -> None:
    """Test boundary at 75: score=74.99 should be REVISE, score=75 should be APPROVE."""
    aggregator = DecisionAggregator()
    
    # Average of ~74.99 should be REVISE
    result_below = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="support", confidence=0.74, reasoning="", metrics={}),
            AgentMessage(agent="CFO", stance="support", confidence=0.75, reasoning="", metrics={}),
            AgentMessage(agent="HR", stance="support", confidence=0.75, reasoning="", metrics={}),
        ]
    )
    # (74 + 75 + 75) / 3 = 74.67
    assert result_below.final_score == 74.67
    assert result_below.decision == FinalDecision.REVISE
    
    # Average of 75 should be APPROVE
    result_at = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="support", confidence=0.75, reasoning="", metrics={}),
            AgentMessage(agent="CFO", stance="support", confidence=0.75, reasoning="", metrics={}),
            AgentMessage(agent="HR", stance="support", confidence=0.75, reasoning="", metrics={}),
        ]
    )
    assert result_at.final_score == 75.0
    assert result_at.decision == FinalDecision.APPROVE


def test_aggregator_boundary_revise_threshold() -> None:
    """Test boundary at 50: score=49.99 should be REJECT, score=50 should be REVISE."""
    aggregator = DecisionAggregator()
    
    # Average of ~49.67 should be REJECT
    result_below = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="oppose", confidence=0.51, reasoning="", metrics={}), # 49
            AgentMessage(agent="CFO", stance="neutral", confidence=0.50, reasoning="", metrics={}), # 50
            AgentMessage(agent="HR", stance="neutral", confidence=0.50, reasoning="", metrics={}), # 50
        ]
    )
    # (49 + 50 + 50) / 3 = 49.67
    assert result_below.final_score == 49.67
    assert result_below.decision == FinalDecision.REJECT
    
    # Average of 50 should be REVISE
    result_at = aggregator.aggregate(
        [
            AgentMessage(agent="CEO", stance="neutral", confidence=0.50, reasoning="", metrics={}), # 50
            AgentMessage(agent="CFO", stance="neutral", confidence=0.50, reasoning="", metrics={}), # 50
            AgentMessage(agent="HR", stance="neutral", confidence=0.50, reasoning="", metrics={}), # 50
        ]
    )
    assert result_at.final_score == 50.0
    assert result_at.decision == FinalDecision.REVISE

def test_aggregator_empty_list_raises_value_error() -> None:
    import pytest
    aggregator = DecisionAggregator()
    with pytest.raises(ValueError, match="messages boş olamaz"):
        aggregator.aggregate([])
