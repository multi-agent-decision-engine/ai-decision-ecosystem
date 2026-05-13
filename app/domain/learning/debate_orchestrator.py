"""
app/domain/learning/debate_orchestrator.py

Multi-round tartışma sistemi: Ajanlar birbirini dinler, fikir değiştirir, konsensüse varar.
PhD-level contribution: Novel consensus protocol with adaptive agent reasoning.
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DebatePhase(str, Enum):
    """Tartışma aşamaları"""
    INITIAL_ANALYSIS = "round_1_initial"
    CROSS_ANALYSIS = "round_2_plus_cross"
    CONSENSUS_BUILDING = "consensus"


@dataclass
class AgentTurn:
    """Bir ajanın tek bir turda söylediği"""
    agent_name: str
    round_number: int
    stance: str  # "support", "neutral", "oppose"
    confidence: float  # 0.0-1.0
    reasoning: str  # Neden bu karar?
    metrics: Dict = field(default_factory=dict)
    references: List[str] = field(default_factory=list)  # Diğer ajanlara referanslar


@dataclass
class DebateTrace:
    """Tartışmanın tam kaydı"""
    scenario_id: int
    agent_turns: List[AgentTurn]
    convergence_score: float  # Agents ne kadar hemfikir? 0-1
    rounds_to_consensus: int
    final_decision: str
    final_confidence: float
    created_at: datetime


class DebateOrchestrator:
    """
    Multi-round debate yöneticisi.

    Stratejisi:
    1. Round 1: Herbir ajan bağımsız analiz yapıyor
    2. Round 2+: Ajanlar önceki turları okuyup fikir değiştiriyor
    3. Consensus: Öğrenilen ağırlıklar ve uzlaşma algoritması
    """

    def __init__(
        self,
        max_rounds: int = 3,
        convergence_threshold: float = 0.05,
        verbose: bool = True
    ):
        self.max_rounds = max_rounds
        self.convergence_threshold = convergence_threshold
        self.verbose = verbose

    def orchestrate_debate(
        self,
        scenario: Dict,
        agents_dict: Dict[str, 'Agent'],  # {"CEO": agent, "CFO": agent, "HR": agent}
        learned_weights: Dict[str, float] = None
    ) -> DebateTrace:
        """
        Ana tartışma fonksiyonu.

        agents_dict:
            {"CEO": CEOAgent(), "CFO": CFOAgent(), "HR": HRAgent()}

        learned_weights:
            {"CEO": 0.35, "CFO": 0.35, "HR": 0.30}
            (From training. If None, equal weights assumed.)

        Returns: Full debate trace with decisions
        """

        if learned_weights is None:
            learned_weights = {
                name: 1.0 / len(agents_dict) for name in agents_dict
            }

        agent_turns = []
        scores_per_round = []

        # ROUND 1: Initial Analysis (no prior messages)
        if self.verbose:
            print("\n🔵 ROUND 1: Initial Analysis")
            print("=" * 50)

        round_1_turns = []
        round_1_scores = []

        for agent_name, agent in agents_dict.items():
            # Agent analyzes scenario independently
            msg = agent.analyze(scenario, previous_messages=None)

            turn = AgentTurn(
                agent_name=agent_name,
                round_number=1,
                stance=msg.stance if hasattr(msg, 'stance') else "neutral",
                confidence=msg.confidence if hasattr(msg, 'confidence') else 0.65,
                reasoning=msg.reasoning if hasattr(msg, 'reasoning') else "",
                metrics=msg.metrics if hasattr(msg, 'metrics') else {}
            )

            round_1_turns.append(turn)
            round_1_scores.append(turn.confidence)

            if self.verbose:
                print(
                    f"\n{agent_name}: {turn.stance.upper()} "
                    f"({turn.confidence*100:.0f}%)"
                )
                print(f"  Reasoning: {turn.reasoning[:100]}...")

        agent_turns.extend(round_1_turns)
        scores_per_round.append(round_1_scores)

        # ROUND 2+: Cross-Analysis with feedback
        for round_num in range(2, self.max_rounds + 1):
            if self.verbose:
                print(f"\n\n🟢 ROUND {round_num}: Cross-Analysis")
                print("=" * 50)

            round_turns = []
            round_scores = []

            for agent_name, agent in agents_dict.items():
                # Get previous messages from all rounds
                previous_messages = [
                    turn for turn in agent_turns
                ]

                # Agent re-analyzes with cross-agent context
                msg = agent.analyze(scenario, previous_messages=previous_messages)

                # Confidence adjustment based on other agents
                adjusted_confidence = self._adjust_confidence(
                    agent_name=agent_name,
                    original_confidence=msg.confidence if hasattr(msg, 'confidence') else 0.65,
                    other_agents_scores=self._get_other_agents_scores(
                        agent_name, previous_messages
                    ),
                    scenario=scenario
                )

                turn = AgentTurn(
                    agent_name=agent_name,
                    round_number=round_num,
                    stance=msg.stance if hasattr(msg, 'stance') else "neutral",
                    confidence=adjusted_confidence,
                    reasoning=msg.reasoning if hasattr(msg, 'reasoning') else "",
                    metrics=msg.metrics if hasattr(msg, 'metrics') else {},
                    references=self._extract_references(
                        msg.reasoning if hasattr(msg, 'reasoning') else ""
                    )
                )

                round_turns.append(turn)
                round_scores.append(turn.confidence)

                if self.verbose:
                    print(
                        f"\n{agent_name}: {turn.stance.upper()} "
                        f"({turn.confidence*100:.0f}%)"
                    )
                    if turn.references:
                        print(f"  References: {', '.join(turn.references)}")
                    print(f"  Reasoning: {turn.reasoning[:100]}...")

            agent_turns.extend(round_turns)
            scores_per_round.append(round_scores)

            # Check convergence
            convergence = self._calculate_convergence(round_scores)

            if self.verbose:
                print(
                    f"\n  📊 Convergence Score: {convergence:.2f} "
                    f"(threshold: {self.convergence_threshold})"
                )

            if convergence < self.convergence_threshold:
                if self.verbose:
                    print("  ✅ Consensus reached!")
                break

        # CONSENSUS BUILDING: Aggregate with learned weights
        if self.verbose:
            print(f"\n\n🏁 CONSENSUS PHASE")
            print("=" * 50)

        final_decision, final_confidence = self._aggregate_consensus(
            agent_turns=agent_turns,
            learned_weights=learned_weights,
            scenario=scenario
        )

        if self.verbose:
            print(f"\n✨ Final Decision: {final_decision}")
            print(f"   Confidence: {final_confidence*100:.0f}%")
            print(f"   Rounds: {round_num}")

        # Create trace
        trace = DebateTrace(
            scenario_id=scenario.get("scenario_id", -1),
            agent_turns=agent_turns,
            convergence_score=self._calculate_convergence(
                scores_per_round[-1]
            ),
            rounds_to_consensus=round_num,
            final_decision=final_decision,
            final_confidence=final_confidence,
            created_at=datetime.now()
        )

        return trace

    def _adjust_confidence(
        self,
        agent_name: str,
        original_confidence: float,
        other_agents_scores: Dict[str, float],
        scenario: Dict
    ) -> float:
        """
        Agent's confidence'ını diğer ajanlar'ın kararlarına göre ayarla.

        Logic:
        - Eğer herkes hemfikir → confidence ↑
        - Eğer çelişki var → confidence ↓
        - Eğer minority opinion → slight confidence ↓
        """

        if not other_agents_scores:
            return original_confidence

        other_confidences = list(other_agents_scores.values())
        other_avg = np.mean(other_confidences)
        other_std = np.std(other_confidences) if len(other_confidences) > 1 else 0

        # Agent-specific adjustment logic
        if agent_name == "CEO":
            # CEO is strategic - might adjust for risk warnings
            if other_avg < 0.6:  # Others are cautious
                adjustment = -0.08  # Slightly reduce CEO optimism
            elif other_avg > 0.8:  # Strong consensus
                adjustment = +0.05  # CEO more confident
            else:
                adjustment = 0.0

        elif agent_name == "CFO":
            # CFO is risk-averse - validates others' support
            if other_avg > 0.75:  # Strong CEO/HR support
                adjustment = +0.10  # CFO becomes more supportive
            elif other_avg < 0.55:  # Weak support
                adjustment = -0.05  # CFO more cautious
            else:
                adjustment = 0.0

        elif agent_name == "HR":
            # HR is team-focused - responds to team readiness
            if scenario.get("team_readiness", 5) < 4 and other_avg > 0.7:
                adjustment = -0.12  # HR warns about team capacity
            else:
                adjustment = 0.0

        # Apply adjustment with bounds
        adjusted = original_confidence + adjustment
        return np.clip(adjusted, 0.3, 0.95)

    def _aggregate_consensus(
        self,
        agent_turns: List[AgentTurn],
        learned_weights: Dict[str, float],
        scenario: Dict
    ) -> Tuple[str, float]:
        """
        Final turdan all agents'ın kararlarını öğrenilen weights'le topla.

        Returns: (decision_string, confidence_0_to_1)
        """

        # Get last turn from each agent
        last_turns = {}
        for turn in reversed(agent_turns):
            if turn.agent_name not in last_turns:
                last_turns[turn.agent_name] = turn

        # Weighted average
        weighted_score = 0.0

        for agent_name, turn in last_turns.items():
            weight = learned_weights.get(agent_name, 1.0 / len(last_turns))
            # Confidence → score
            score = turn.confidence
            weighted_score += weight * score

        # Convert score to decision
        if weighted_score >= 0.75:
            decision = "APPROVE"
        elif weighted_score >= 0.50:
            decision = "REVISE"
        else:
            decision = "REJECT"

        return decision, weighted_score

    def _calculate_convergence(self, scores: List[float]) -> float:
        """
        Agents hemfikir mi? Düşük = consensus, yüksek = disagreement

        Returns: coefficient of variation (0 = perfect consensus)
        """

        if not scores or len(scores) <= 1:
            return 0.0

        mean_score = np.mean(scores)
        std_score = np.std(scores)

        if mean_score == 0:
            return 1.0

        cv = std_score / mean_score
        return cv

    def _get_other_agents_scores(
        self,
        current_agent: str,
        previous_messages: List[AgentTurn]
    ) -> Dict[str, float]:
        """
        Akım agent'dan başka tüm ajanların en son confidence'larını getir
        """

        other_scores = {}

        for turn in reversed(previous_messages):
            if turn.agent_name != current_agent and turn.agent_name not in other_scores:
                other_scores[turn.agent_name] = turn.confidence

        return other_scores

    def _extract_references(self, reasoning: str) -> List[str]:
        """
        Reasoning metininden diğer ajanlar'a referansları çıkart.
        (Simple heuristic: CFO, CEO, HR mentioned mi?)
        """

        references = []
        agents = ["CEO", "CFO", "HR"]

        for agent in agents:
            if agent in reasoning:
                references.append(agent)

        return references


class DebateAnalytics:
    """Tartışma kalitesi ve etkinliği analiz eden sınıf"""

    @staticmethod
    def analyze_trace(trace: DebateTrace) -> Dict:
        """Debate trace'i incelemeye tabi tut"""

        # Agent participation
        agent_participation = {}
        for turn in trace.agent_turns:
            if turn.agent_name not in agent_participation:
                agent_participation[turn.agent_name] = 0
            agent_participation[turn.agent_name] += 1

        # Cross-references count (agents reference each other)
        cross_refs = 0
        for turn in trace.agent_turns:
            cross_refs += len(turn.references)

        # Stance changes
        stance_changes = 0
        previous_stances = {}
        for turn in trace.agent_turns:
            if turn.agent_name in previous_stances:
                if turn.stance != previous_stances[turn.agent_name]:
                    stance_changes += 1
            previous_stances[turn.agent_name] = turn.stance

        return {
            "total_messages": len(trace.agent_turns),
            "agent_participation": agent_participation,
            "cross_references": cross_refs,
            "stance_changes": stance_changes,
            "convergence_score": trace.convergence_score,
            "rounds_to_consensus": trace.rounds_to_consensus,
            "final_decision": trace.final_decision,
            "final_confidence": trace.final_confidence,
            "debate_quality": {
                "engagement": cross_refs / max(len(trace.agent_turns), 1),  # 0-1
                "stability": 1 - (stance_changes / max(len(trace.agent_turns), 1)),  # 0-1
                "confidence_score": trace.final_confidence
            }
        }


# Usage Example
if __name__ == "__main__":
    print("\n📋 Debate Orchestrator Example")
    print("=" * 60)

    # Mock scenario
    scenario = {
        "scenario_id": 1,
        "name": "Southeast Asia Expansion",
        "budget_million_usd": 5.0,
        "expected_roi_percent": 45.0,
        "risk_level": 6,
        "team_readiness": 7
    }

    # Mock agents (would be real agent instances)
    class MockAgent:
        def __init__(self, name):
            self.name = name

        def analyze(self, scenario, previous_messages=None):
            if self.name == "CEO":
                return type('msg', (), {
                    'stance': 'support',
                    'confidence': 0.78,
                    'reasoning': 'Strategic fit. CEO sees opportunity.',
                    'metrics': {}
                })()
            elif self.name == "CFO":
                return type('msg', (), {
                    'stance': 'neutral',
                    'confidence': 0.65,
                    'reasoning': 'Risk concerns from CFO perspective.',
                    'metrics': {}
                })()
            else:  # HR
                return type('msg', (), {
                    'stance': 'support',
                    'confidence': 0.82,
                    'reasoning': 'Team is ready from HR view.',
                    'metrics': {}
                })()

    agents = {
        "CEO": MockAgent("CEO"),
        "CFO": MockAgent("CFO"),
        "HR": MockAgent("HR")
    }

    learned_weights = {
        "CEO": 0.35,
        "CFO": 0.35,
        "HR": 0.30
    }

    # Run debate
    orchestrator = DebateOrchestrator(max_rounds=3, verbose=True)
    trace = orchestrator.orchestrate_debate(
        scenario=scenario,
        agents_dict=agents,
        learned_weights=learned_weights
    )

    # Analyze
    analytics = DebateAnalytics.analyze_trace(trace)
    print("\n📊 Debate Analytics:")
    print(f"  Messages: {analytics['total_messages']}")
    print(f"  Cross-References: {analytics['cross_references']}")
    print(f"  Stance Changes: {analytics['stance_changes']}")
    print(f"  Debate Quality: {analytics['debate_quality']}")
