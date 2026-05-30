from app.domain.agents.base import Agent
from app.domain.models import AgentMessage, ScenarioInput, get_agent_metrics, get_agent_stance


def _to_hr_inputs(scenario: ScenarioInput) -> dict:
    """
    Convert ScenarioInput to standardized HR inputs.
    """
    budget_factor = scenario.budget_million_usd / 5.0
    risk_factor = scenario.risk_level / 5.0
    hiring_needed = int(budget_factor + risk_factor)

    if hiring_needed <= 2:
        time_to_hire = 1.5
        training = 1.0
    elif hiring_needed <= 5:
        time_to_hire = 2.5
        training = 1.5
    else:
        time_to_hire = 3.5
        training = 2.0

    if scenario.team_readiness >= 8:
        training = max(0.5, training - 0.5)

    return {
        "hiring_needed": max(0, hiring_needed),
        "time_to_hire_months": time_to_hire,
        "training_months": training,
        "team_readiness": scenario.team_readiness,
    }


class HRAgent(Agent):
    """
    HR Agent: human resources impact evaluation.

    Metrics produced:
        - talent_availability (0-10): available talent/hiring feasibility
        - team_impact (0-10): impact on existing team
        - workload_score (0-10): workload sustainability assessment
    """

    def _build_reasoning_prompt(self, scenario_inputs: ScenarioInput) -> str:
        return (
            "[HR Metni / HR Analysis]: Ekip kapasitesi / team capacity and workload review "
            f"(readiness: {scenario_inputs.team_readiness}/10)"
        )

    def analyze(
        self,
        scenario_inputs: ScenarioInput,
        previous_messages: list[AgentMessage] | None = None,
    ) -> AgentMessage:
        hr_inputs = _to_hr_inputs(scenario_inputs)

        team_readiness = hr_inputs["team_readiness"]
        hiring_needed = hr_inputs["hiring_needed"]
        time_to_hire_months = hr_inputs["time_to_hire_months"]
        training_months = hr_inputs["training_months"]
        total_readiness_months = time_to_hire_months + training_months

        talent_availability = max(0, 10 - hiring_needed * 0.8)
        team_impact = team_readiness * (1 - hiring_needed / 15.0)
        workload_score = max(0, 10 - total_readiness_months * 1.5)

        current_round = 1
        if previous_messages:
            current_round = max(m.round_number for m in previous_messages) + 1

        reasoning_notes: list[str] = []

        if current_round > 1 and previous_messages:
            cfo_metrics = get_agent_metrics(previous_messages, "CFO")
            if cfo_metrics:
                cfo_risk = cfo_metrics.get("risk_score", 0)
                cfo_roi = cfo_metrics.get("roi_estimate", 0)

                if cfo_risk > 7:
                    talent_availability -= 1.5
                    reasoning_notes.append(
                        "CFO's high financial risk warning may make hiring harder."
                    )

                if cfo_roi > 30 and cfo_risk < 5:
                    talent_availability += 1.0
                    reasoning_notes.append(
                        "CFO's strong ROI view may improve candidate attraction."
                    )

            ceo_metrics = get_agent_metrics(previous_messages, "CEO")
            if ceo_metrics:
                market_alignment = ceo_metrics.get("market_alignment", 0)
                growth_potential = ceo_metrics.get("growth_potential", 0)

                if market_alignment < 4:
                    team_impact -= 1.0
                    reasoning_notes.append(
                        "CEO's market uncertainty signal may reduce team motivation."
                    )

                if growth_potential >= 8:
                    workload_score += 0.8
                    reasoning_notes.append(
                        "CEO's growth vision increases workload tolerance."
                    )

        talent_availability = round(max(0, min(10, talent_availability)), 1)
        team_impact = round(max(0, min(10, team_impact)), 1)
        workload_score = round(max(0, min(10, workload_score)), 1)

        composite = (talent_availability + team_impact + workload_score) / 30.0

        if composite >= 0.6:
            stance = "support"
            confidence = min(1.0, 0.5 + composite * 0.5)
        elif composite >= 0.35:
            stance = "neutral"
            confidence = 0.5 + abs(composite - 0.475) * 0.8
        else:
            stance = "oppose"
            confidence = min(1.0, 0.5 + (0.35 - composite) * 1.5)

        if current_round > 1 and previous_messages:
            cfo_metrics = get_agent_metrics(previous_messages, "CFO")
            if cfo_metrics:
                if cfo_metrics.get("risk_score", 0) > 7:
                    confidence -= 0.08
                if cfo_metrics.get("roi_estimate", 0) > 30 and cfo_metrics.get("risk_score", 0) < 5:
                    confidence += 0.05

            ceo_stance = get_agent_stance(previous_messages, "CEO")
            cfo_stance = get_agent_stance(previous_messages, "CFO")

            if ceo_stance and cfo_stance:
                ceo_s, _ = ceo_stance
                cfo_s, _ = cfo_stance

                if stance == "oppose" and ceo_s == "support" and cfo_s == "support":
                    if composite > 0.25:
                        stance = "neutral"
                        confidence = 0.45
                        reasoning_notes.append(
                            "CEO and CFO both support the scenario, so HR softens the objection to neutral."
                        )
                elif stance == "support" and ceo_s == "oppose" and cfo_s == "oppose":
                    stance = "neutral"
                    confidence = 0.5
                    reasoning_notes.append(
                        "CEO and CFO both oppose the scenario, so HR withdraws support."
                    )
                elif ceo_s == "support" and cfo_s == "oppose":
                    confidence -= 0.05
                    reasoning_notes.append(
                        "CEO and CFO disagree, increasing people-execution uncertainty."
                    )

                if not reasoning_notes:
                    reasoning_notes.append(
                        f"CEO's {ceo_s} stance and CFO's {cfo_s} stance were reviewed; "
                        "HR keeps its position based on capacity and workload constraints."
                    )
            elif not reasoning_notes:
                reasoning_notes.append(
                    "Previous agent messages were reviewed; HR reassessed capacity and workload before keeping its position."
                )

        confidence = max(0.3, min(1.0, confidence))

        base_reasoning = (
            f"{self._build_reasoning_prompt(scenario_inputs)} | "
            f"Team readiness is {team_readiness}/10. Hiring need is {hiring_needed} people "
            f"with {total_readiness_months} months to productivity. "
            f"Talent: {talent_availability}/10, team impact: {team_impact}/10, "
            f"workload: {workload_score}/10."
        )

        if reasoning_notes:
            final_reasoning = (
                f"{base_reasoning} Cross-analysis: {' '.join(reasoning_notes)} "
                f"Result: {stance} ({int(confidence * 100)}%)."
            )
        else:
            final_reasoning = f"{base_reasoning} Result: {stance} ({int(confidence * 100)}%)."

        return AgentMessage(
            agent="HR",
            stance=stance,
            confidence=round(confidence, 2),
            reasoning=final_reasoning,
            metrics={
                "talent_availability": talent_availability,
                "team_impact": team_impact,
                "workload_score": workload_score,
            },
            round_number=current_round,
        )
