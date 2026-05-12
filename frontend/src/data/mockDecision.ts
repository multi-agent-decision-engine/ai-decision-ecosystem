import type {
  Agent,
  AgentFinding,
  ContributionItem,
  DebateMessage,
  ScenarioRow,
} from "../types/decision";

export const initialAgents: Agent[] = [
  {
    id: "ceo",
    name: "CEO Agent",
    role: "Strategic Vision Evaluator",
    status: "IDLE",
    score: 0,
    confidence: 0,
    color: "cyan",
    reasoning: "Waiting for scenario activation.",
  },
  {
    id: "cfo",
    name: "CFO Agent",
    role: "Financial Feasibility Evaluator",
    status: "IDLE",
    score: 0,
    confidence: 0,
    color: "emerald",
    reasoning: "Waiting for financial analysis request.",
  },
  {
    id: "hr",
    name: "HR Agent",
    role: "Workforce Capacity Evaluator",
    status: "IDLE",
    score: 0,
    confidence: 0,
    color: "amber",
    reasoning: "Waiting for workforce capacity scan.",
  },
];

export const completedAgents: Agent[] = [
  {
    id: "ceo",
    name: "CEO Agent",
    role: "Strategic Vision Evaluator",
    status: "COMPLETED",
    score: 85,
    confidence: 91,
    color: "cyan",
    reasoning: "Strong strategic alignment and high ROI detected.",
  },
  {
    id: "cfo",
    name: "CFO Agent",
    role: "Financial Feasibility Evaluator",
    status: "COMPLETED",
    score: 90,
    confidence: 88,
    color: "emerald",
    reasoning:
      "Financial feasibility is positive with acceptable budget exposure.",
  },
  {
    id: "hr",
    name: "HR Agent",
    role: "Workforce Capacity Evaluator",
    status: "WARNING",
    score: 50,
    confidence: 79,
    color: "amber",
    reasoning:
      "Team readiness is below the recommended execution threshold.",
  },
];

export const initialLogs = ["System ready. Awaiting simulation start..."];

export const scenarioRows: ScenarioRow[] = [
  ["Project", "AI Market Expansion Initiative"],
  ["Budget", "$25M"],
  ["Expected ROI", "45%"],
  ["Risk Level", "5/10"],
  ["Team Readiness", "3/10"],
  ["Market Confidence", "7/10"],
  ["Strategic Fit", "8/10"],
  ["Scenario Type", "TEAM EXPANSION"],
];

export const contributionData: ContributionItem[] = [
  { name: "CEO", value: 25, color: "#22d3ee" },
  { name: "CFO", value: 25, color: "#34d399" },
  { name: "HR", value: 50, color: "#fbbf24" },
];

export const reportAgentFindings: AgentFinding[] = [
  {
    agent: "CEO Agent",
    score: 85,
    weight: "25%",
    stance: "Support",
    color: "cyan",
    finding:
      "The initiative has strong strategic alignment and supports long-term market expansion.",
  },
  {
    agent: "CFO Agent",
    score: 90,
    weight: "25%",
    stance: "Support",
    color: "emerald",
    finding:
      "The expected ROI is financially attractive and the budget exposure is acceptable.",
  },
  {
    agent: "HR Agent",
    score: 50,
    weight: "50%",
    stance: "Revise",
    color: "amber",
    finding:
      "Team readiness is below the required execution threshold, creating a workforce capacity bottleneck.",
  },
];

export const reportNextSteps: string[] = [
  "Increase team readiness from 3/10 to at least 6/10.",
  "Create a hiring or onboarding plan before approval.",
  "Keep risk level below 6/10 during execution planning.",
  "Re-run the simulation after workforce capacity improvements.",
];

export const executiveReportText = `AI Decision Ecosystem Engine - Executive Decision Report

Scenario:
AI Market Expansion Initiative

Inputs:
- Budget: $25M
- Expected ROI: 45%
- Risk Level: 5/10
- Team Readiness: 3/10
- Scenario Type: TEAM_EXPANSION

Agent Findings:
- CEO Agent: Score 85 | Weight 25% | Stance: Support
  Strong strategic alignment and long-term market expansion potential detected.

- CFO Agent: Score 90 | Weight 25% | Stance: Support
  Expected ROI is financially attractive and budget exposure is acceptable.

- HR Agent: Score 50 | Weight 50% | Stance: Revise
  Team readiness is below execution threshold, creating a workforce capacity bottleneck.

Final Score Calculation:
CEO: 85 × 0.25 = 21.25
CFO: 90 × 0.25 = 22.50
HR : 50 × 0.50 = 25.00

Final Score: 68.75 / 100
Final Decision: REVISE
Primary Bottleneck: Workforce Capacity

Recommended Next Steps:
1. Increase team readiness from 3/10 to at least 6/10.
2. Create a hiring or onboarding plan before approval.
3. Keep risk level below 6/10 during execution planning.
4. Re-run the simulation after workforce capacity improvements.
`;
export const agentDebateMessages: DebateMessage[] = [
  {
    round: "ROUND 1 — Independent Analysis",
    agent: "CEO Agent",
    stance: "Support",
    color: "cyan",
    message:
      "Strategic upside is strong. ROI and market confidence support expansion.",
  },
  {
    round: "ROUND 1 — Independent Analysis",
    agent: "CFO Agent",
    stance: "Support",
    color: "emerald",
    message:
      "Financial feasibility is positive. Budget exposure is acceptable under controlled execution.",
  },
  {
    round: "ROUND 1 — Independent Analysis",
    agent: "HR Agent",
    stance: "Warning",
    color: "amber",
    message:
      "Execution risk is high because team readiness is only 3/10.",
  },
  {
    round: "ROUND 2 — Cross-Agent Deliberation",
    agent: "CEO Agent",
    stance: "Revise",
    color: "cyan",
    message:
      "I accept HR's workforce concern. Approval should depend on hiring readiness.",
  },
  {
    round: "ROUND 2 — Cross-Agent Deliberation",
    agent: "CFO Agent",
    stance: "Revise",
    color: "emerald",
    message:
      "If additional hiring cost is planned, financial risk remains manageable.",
  },
  {
    round: "ROUND 2 — Cross-Agent Deliberation",
    agent: "HR Agent",
    stance: "Revise",
    color: "amber",
    message:
      "Recommendation: revise the plan with a hiring and onboarding capacity plan.",
  },
  {
    round: "CONSENSUS — Aggregator Decision",
    agent: "Decision Aggregator",
    stance: "Consensus",
    color: "purple",
    message:
      "Consensus decision: REVISE. Main bottleneck is Workforce Capacity.",
  },
];
