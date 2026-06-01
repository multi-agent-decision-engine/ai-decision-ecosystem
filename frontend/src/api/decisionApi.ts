import type { ApiScenario, ApiSimulationResponse } from "../types/api";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

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

function normalizeScenarioList(data: unknown): ApiScenario[] {
  if (Array.isArray(data)) {
    return data as ApiScenario[];
  }

  if (
    data &&
    typeof data === "object" &&
    "scenarios" in data &&
    Array.isArray((data as { scenarios?: unknown }).scenarios)
  ) {
    return (data as { scenarios: ApiScenario[] }).scenarios;
  }

  if (
    data &&
    typeof data === "object" &&
    "items" in data &&
    Array.isArray((data as { items?: unknown }).items)
  ) {
    return (data as { items: ApiScenario[] }).items;
  }

  return [];
}

export const decisionApi = {
  async getScenarios() {
    const data = await request<unknown>("/api/v1/scenarios");
    return normalizeScenarioList(data);
  },

  simulateScenario(scenarioId: string | number) {
    return request<ApiSimulationResponse>(
      `/api/v1/scenarios/${scenarioId}/simulate`,
      {
        method: "POST",
      }
    );
  },
};