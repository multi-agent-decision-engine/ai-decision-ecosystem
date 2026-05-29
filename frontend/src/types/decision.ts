export type AgentStatus = "IDLE" | "ANALYZING" | "WARNING" | "COMPLETED";

export type AgentColor = "cyan" | "emerald" | "amber" | "purple";

export type Agent = {
  id: string;
  name: string;
  role: string;
  status: AgentStatus;
  score: number;
  confidence: number;
  color: AgentColor;
  reasoning: string;
};

export type Scenario = {
  id: number;
  name: string;
  description: string;
  budget_million_usd: number;
  expected_roi_percent: number;
  risk_level: number;
  team_readiness: number;
  created_at: string;
};

export type ScenarioListResponse = {
  items: Scenario[];
  limit: number;
  offset: number;
};

export type AgentOutputResponse = {
  agent_name?: string;
  name?: string;
  id?: string;
  role?: string;
  score: number;
  rationale?: string;
  reasoning?: string;
  confidence?: number;
  weight?: number;
};

export type AgentMessageResponse = {
  agent?: string;
  agent_name?: string;
  stance?: string;
  confidence?: number;
  reasoning?: string;
  rationale?: string;
  round_number?: number;
};

export type RoundResponse = {
  round_number: number;
  messages: AgentMessageResponse[];
};

export type SimulationDetailResponse = {
  scenario_id?: number;
  scenario?: Scenario;
  agents?: AgentOutputResponse[];
  agent_outputs?: AgentOutputResponse[];
  rounds?: RoundResponse[];
  final_score: number;
  final_decision: string;
  consensus_reached?: boolean;
  stability_reached?: boolean;
  scenario_type?: string | null;
  scenario_type_confidence?: number | null;
  agent_weights?: Record<string, number> | null;
};

export type DebateMessage = {
  id: string;
  agent: string;
  stance: string;
  confidence: number;
  reasoning: string;
};

export type ContributionDatum = {
  name: string;
  value: number;
  color: string;
};
