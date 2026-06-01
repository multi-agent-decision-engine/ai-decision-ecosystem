import type {
  ApiAgentOutput,
  ApiDebateRound,
  ApiRoundMessage,
  ApiScenario,
  ApiSimulationResponse,
} from "../types/api";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type UnknownRecord = Record<string, unknown>;

function isRecord(value: unknown): value is UnknownRecord {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function asString(value: unknown, fallback = "") {
  if (typeof value === "string") return value;
  if (typeof value === "number") return String(value);
  return fallback;
}

function asNumber(value: unknown, fallback = 0) {
  if (typeof value === "number") return value;

  if (typeof value === "string") {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  return fallback;
}

function asBoolean(value: unknown, fallback = false) {
  if (typeof value === "boolean") return value;

  if (typeof value === "string") {
    const normalized = value.toLowerCase();
    if (normalized === "true" || normalized === "yes") return true;
    if (normalized === "false" || normalized === "no") return false;
  }

  return fallback;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function unwrapData(value: unknown): unknown {
  if (!isRecord(value)) return value;

  return (
    value.data ??
    value.result ??
    value.simulation ??
    value.payload ??
    value
  );
}

function normalizeScenario(raw: unknown): ApiScenario {
  const item = isRecord(raw) ? raw : {};

  return {
    id: asString(
      item.id ?? item.scenario_id ?? item.scenarioId,
      crypto.randomUUID()
    ),
    title: asString(
      item.title ??
        item.name ??
        item.scenario_name ??
        item.scenarioName ??
        item.project
    ),
    name: asString(item.name ?? item.title),
    description: asString(item.description),
    budget:
      item.budget !== undefined
        ? asNumber(item.budget)
        : item.budget_million_usd !== undefined
          ? asNumber(item.budget_million_usd)
        : item.budget_million !== undefined
          ? asNumber(item.budget_million)
          : undefined,
    expected_roi:
      item.expected_roi !== undefined
        ? asNumber(item.expected_roi)
        : item.expected_roi_percent !== undefined
          ? asNumber(item.expected_roi_percent)
        : item.expectedRoi !== undefined
          ? asNumber(item.expectedRoi)
          : item.roi !== undefined
            ? asNumber(item.roi)
            : undefined,
    risk_level:
      item.risk_level !== undefined
        ? asNumber(item.risk_level)
        : item.riskLevel !== undefined
          ? asNumber(item.riskLevel)
          : item.risk !== undefined
            ? asNumber(item.risk)
            : undefined,
    team_readiness:
      item.team_readiness !== undefined
        ? asNumber(item.team_readiness)
        : item.teamReadiness !== undefined
          ? asNumber(item.teamReadiness)
          : undefined,
    market_confidence:
      item.market_confidence !== undefined
        ? asNumber(item.market_confidence)
        : item.marketConfidence !== undefined
          ? asNumber(item.marketConfidence)
          : undefined,
    strategic_fit:
      item.strategic_fit !== undefined
        ? asNumber(item.strategic_fit)
        : item.strategicFit !== undefined
          ? asNumber(item.strategicFit)
          : undefined,
    scenario_type: asString(
      item.scenario_type ?? item.scenarioType ?? item.type
    ),
  };
}

function normalizeScenarioList(data: unknown): ApiScenario[] {
  const unwrapped = unwrapData(data);

  if (Array.isArray(unwrapped)) {
    return unwrapped.map(normalizeScenario);
  }

  if (isRecord(unwrapped)) {
    const possibleList =
      unwrapped.scenarios ??
      unwrapped.items ??
      unwrapped.results ??
      unwrapped.data;

    if (Array.isArray(possibleList)) {
      return possibleList.map(normalizeScenario);
    }
  }

  return [];
}

function normalizeAgentOutput(raw: unknown): ApiAgentOutput {
  const item = isRecord(raw) ? raw : {};

  return {
    agent: asString(
      item.agent ??
        item.agent_name ??
        item.agentName ??
        item.name ??
        item.role,
      "Unknown Agent"
    ),
    score: asNumber(item.score ?? item.final_score ?? item.finalScore, 0),
    stance: asString(item.stance ?? item.decision ?? item.recommendation),
    confidence:
      item.confidence !== undefined ? asNumber(item.confidence) : undefined,
    reasoning: asString(
      item.reasoning ??
        item.message ??
        item.explanation ??
        item.rationale ??
        item.summary
    ),
  };
}

function normalizeRoundMessage(
  raw: unknown,
  fallbackRoundNumber: number
): ApiRoundMessage {
  const item = isRecord(raw) ? raw : {};

  return {
    agent: asString(
      item.agent ??
        item.agent_name ??
        item.agentName ??
        item.name ??
        item.role,
      "Unknown Agent"
    ),
    stance: asString(item.stance ?? item.decision ?? item.recommendation),
    confidence:
      item.confidence !== undefined ? asNumber(item.confidence) : undefined,
    reasoning: asString(
      item.reasoning ??
        item.message ??
        item.content ??
        item.explanation ??
        item.rationale
    ),
    round_number: asNumber(
      item.round_number ?? item.roundNumber,
      fallbackRoundNumber
    ),
  };
}

function normalizeRound(raw: unknown, index: number): ApiDebateRound {
  const item = isRecord(raw) ? raw : {};
  const roundNumber = asNumber(
    item.round_number ?? item.roundNumber ?? item.id,
    index + 1
  );

  const messagesRaw =
    item.messages ??
    item.agent_messages ??
    item.agentMessages ??
    item.outputs ??
    [];

  const messages = Array.isArray(messagesRaw)
    ? messagesRaw.map((message) => normalizeRoundMessage(message, roundNumber))
    : [];

  return {
    round_number: roundNumber,
    messages,
  };
}

function normalizeSimulationResponse(data: unknown): ApiSimulationResponse {
  const unwrapped = unwrapData(data);
  const item = isRecord(unwrapped) ? unwrapped : {};

  const rawAgentOutputs =
    item.agent_outputs ??
    item.agentOutputs ??
    item.agents ??
    item.outputs ??
    [];

  const rawRounds =
    item.rounds ??
    item.debate_rounds ??
    item.debateRounds ??
    item.discussion_rounds ??
    [];

  return {
    scenario_id: asString(
      item.scenario_id ?? item.scenarioId ?? item.id ?? item.scenario,
      "unknown"
    ),
    final_score: asNumber(
      item.final_score ??
        item.finalScore ??
        item.score ??
        item.overall_score ??
        item.overallScore,
      0
    ),
    final_decision: asString(
      item.final_decision ??
        item.finalDecision ??
        item.decision ??
        item.recommendation,
      "UNKNOWN"
    ),
    agent_outputs: Array.isArray(rawAgentOutputs)
      ? rawAgentOutputs.map(normalizeAgentOutput)
      : [],
    rounds: Array.isArray(rawRounds)
      ? rawRounds.map((round, index) => normalizeRound(round, index))
      : [],
    total_rounds:
      item.total_rounds !== undefined
        ? asNumber(item.total_rounds)
        : item.totalRounds !== undefined
          ? asNumber(item.totalRounds)
          : undefined,
    consensus_reached: asBoolean(
      item.consensus_reached ?? item.consensusReached,
      false
    ),
    stability_reached: asBoolean(
      item.stability_reached ?? item.stabilityReached,
      false
    ),
    scenario_type: asString(item.scenario_type ?? item.scenarioType),
    scenario_type_confidence:
      item.scenario_type_confidence !== undefined
        ? asNumber(item.scenario_type_confidence)
        : item.scenarioTypeConfidence !== undefined
          ? asNumber(item.scenarioTypeConfidence)
          : undefined,
    agent_weights: isRecord(item.agent_weights)
      ? Object.fromEntries(
          Object.entries(item.agent_weights).map(([key, value]) => [
            key,
            asNumber(value),
          ])
        )
      : undefined,
  };
}

export const decisionApi = {
  async getScenarios() {
    const data = await request<unknown>("/api/v1/scenarios");
    return normalizeScenarioList(data);
  },

  async simulateScenario(scenarioId: string | number) {
    const data = await request<unknown>(
      `/api/v1/scenarios/${scenarioId}/simulate`,
      {
        method: "POST",
      }
    );

    return normalizeSimulationResponse(data);
  },
};
