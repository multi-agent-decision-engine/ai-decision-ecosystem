export type AgentStatus = "IDLE" | "ANALYZING" | "WARNING" | "COMPLETED";

export type AgentColor = "cyan" | "emerald" | "amber" | "purple";

export type DecisionResult = "APPROVE" | "REVISE" | "REJECT";

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

export type ScenarioRow = [label: string, value: string];

export type ContributionItem = {
  name: string;
  value: number;
  color: string;
};

export type AgentFinding = {
  agent: string;
  score: number;
  weight: string;
  stance: "Support" | "Revise" | "Reject";
  color: AgentColor;
  finding: string;
};
export type DebateMessage = {
  round: string;
  agent: string;
  stance: "Support" | "Warning" | "Revise" | "Consensus";
  message: string;
  color: AgentColor;
};
