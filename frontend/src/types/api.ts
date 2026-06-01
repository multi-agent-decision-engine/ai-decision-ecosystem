export type ApiScenario = {
  id: string | number;
  title?: string;
  name?: string;
  description?: string;
  budget?: number;
  expected_roi?: number;
  risk_level?: number;
  team_readiness?: number;
  market_confidence?: number;
  strategic_fit?: number;
  scenario_type?: string;
};

export type ApiAgentOutput = {
  agent: string;
  score: number;
  stance?: string;
  confidence?: number;
  reasoning?: string;
};

export type ApiRoundMessage = {
  agent: string;
  stance?: string;
  confidence?: number;
  reasoning?: string;
  round_number?: number;
};

export type ApiDebateRound = {
  round_number: number;
  messages: ApiRoundMessage[];
};

export type ApiSimulationResponse = {
  scenario_id: string | number;
  final_score: number;
  final_decision: "APPROVE" | "REVISE" | "REJECT" | string;
  agent_outputs: ApiAgentOutput[];
  rounds?: ApiDebateRound[];
  consensus_reached?: boolean;
  stability_reached?: boolean;
};