import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { useEffect, useMemo, useState, type ReactNode } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle2,
  Copy,
  Cpu,
  Download,
  FileText,
  FlaskConical,
  History,
  LayoutDashboard,
  Loader2,
  PlusCircle,
  Radio,
  RefreshCw,
  Settings,
  ShieldCheck,
  Users,
  Zap,
} from "lucide-react";
import type {
  Agent,
  AgentColor,
  AgentOutputResponse,
  AgentStatus,
  ContributionDatum,
  DebateMessage,
  Scenario,
  ScenarioListResponse,
  SimulationDetailResponse,
} from "./types/decision";

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://localhost:8000";

const AGENT_META: Record<
  string,
  { id: string; role: string; color: AgentColor }
> = {
  CEO: { id: "ceo", role: "Strategic Vision Evaluator", color: "cyan" },
  CFO: { id: "cfo", role: "Financial Feasibility Evaluator", color: "emerald" },
  HR: { id: "hr", role: "Workforce Capacity Evaluator", color: "amber" },
};

const EMPTY_AGENTS: Agent[] = ["CEO", "CFO", "HR"].map((name) => ({
  id: AGENT_META[name].id,
  name: `${name} Agent`,
  role: AGENT_META[name].role,
  status: "IDLE",
  score: 0,
  confidence: 0,
  color: AGENT_META[name].color,
  reasoning: "Waiting for scenario activation.",
}));

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const body = await response.text().catch(() => "");
    throw new Error(
      `HTTP ${response.status} ${response.statusText}${body ? `: ${body}` : ""}`,
    );
  }

  return (await response.json()) as T;
}

function normalizeAgentName(output: AgentOutputResponse) {
  return output.agent_name ?? output.name ?? output.id ?? "Agent";
}

function agentKey(name: string) {
  return name.replace(/\s+Agent$/i, "").toUpperCase();
}

function getSimulationAgents(simulation: SimulationDetailResponse | null) {
  return simulation?.agents ?? simulation?.agent_outputs ?? [];
}

function mapAgents(simulation: SimulationDetailResponse | null): Agent[] {
  const outputs = getSimulationAgents(simulation);

  if (outputs.length === 0) {
    return EMPTY_AGENTS;
  }

  return outputs.map((output) => {
    const name = normalizeAgentName(output);
    const key = agentKey(name);
    const meta = AGENT_META[key] ?? {
      id: key.toLowerCase(),
      role: output.role ?? "Decision Evaluator",
      color: "purple" as AgentColor,
    };
    const confidence = output.confidence ?? Math.min(99, Math.max(55, output.score));

    return {
      id: meta.id,
      name: name.endsWith("Agent") ? name : `${name} Agent`,
      role: output.role ?? meta.role,
      status: output.score >= 50 ? "COMPLETED" : "WARNING",
      score: output.score,
      confidence,
      color: meta.color,
      reasoning: output.rationale ?? output.reasoning ?? "No rationale returned.",
    };
  });
}

function mapDebateMessages(simulation: SimulationDetailResponse | null): DebateMessage[] {
  if (!simulation) return [];

  if (simulation.rounds?.length) {
    return simulation.rounds.flatMap((round) =>
      round.messages.map((message, index) => ({
        id: `${round.round_number}-${message.agent ?? message.agent_name ?? index}`,
        agent: message.agent ?? message.agent_name ?? "Agent",
        stance: message.stance ?? "Analysis",
        confidence: Math.round((message.confidence ?? 0) * 100),
        reasoning: message.reasoning ?? message.rationale ?? "No message returned.",
      })),
    );
  }

  return getSimulationAgents(simulation).map((output, index) => ({
    id: `${normalizeAgentName(output)}-${index}`,
    agent: normalizeAgentName(output),
    stance: output.score >= 70 ? "Approve" : output.score >= 50 ? "Revise" : "Reject",
    confidence: output.confidence ?? Math.min(99, Math.max(55, output.score)),
    reasoning: output.rationale ?? output.reasoning ?? "No rationale returned.",
  }));
}

function mapContributionData(
  simulation: SimulationDetailResponse | null,
): ContributionDatum[] {
  const outputs = getSimulationAgents(simulation);
  const weights = simulation?.agent_weights;

  return outputs.map((output) => {
    const name = normalizeAgentName(output);
    const key = agentKey(name);
    const meta = AGENT_META[key] ?? { color: "purple" as AgentColor };
    const weight = output.weight ?? weights?.[key] ?? weights?.[name] ?? output.score;

    return {
      name,
      value: Number(weight.toFixed ? weight.toFixed(2) : weight),
      color: chartColor(meta.color),
    };
  });
}

function decisionTone(decision?: string) {
  if (decision === "APPROVE") return "emerald";
  if (decision === "REJECT") return "red";
  return "amber";
}

export default function App() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState<number | null>(null);
  const [simulation, setSimulation] = useState<SimulationDetailResponse | null>(null);
  const [isLoadingScenarios, setIsLoadingScenarios] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>(["Connect to the backend to load scenarios."]);

  const selectedScenario =
    scenarios.find((scenario) => scenario.id === selectedScenarioId) ?? null;
  const agents = useMemo(() => mapAgents(simulation), [simulation]);
  const debateMessages = useMemo(() => mapDebateMessages(simulation), [simulation]);
  const contributionData = useMemo(() => mapContributionData(simulation), [simulation]);
  const finalDecision = simulation?.final_decision ?? "WAITING";

  const loadScenarios = async () => {
    setIsLoadingScenarios(true);
    setError(null);

    try {
      const data = await fetchJson<ScenarioListResponse>("/api/v1/scenarios?limit=100&offset=0");
      setScenarios(data.items);
      setSelectedScenarioId((current) => current ?? data.items[0]?.id ?? null);
      setLogs([
        data.items.length
          ? `${data.items.length} scenarios loaded from backend.`
          : "Backend returned no scenarios.",
      ]);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setError(message);
      setLogs([`Scenario load failed: ${message}`]);
    } finally {
      setIsLoadingScenarios(false);
    }
  };

  useEffect(() => {
    void loadScenarios();
  }, []);

  const runSimulation = async () => {
    if (!selectedScenarioId || isRunning) return;

    setIsRunning(true);
    setError(null);
    setSimulation(null);
    setLogs([
      `Scenario selected: ${selectedScenario?.name ?? `#${selectedScenarioId}`}`,
      "POST /api/v1/scenarios/{id}/simulate started.",
    ]);

    try {
      const result = await fetchJson<SimulationDetailResponse>(
        `/api/v1/scenarios/${selectedScenarioId}/simulate`,
        { method: "POST" },
      );
      setSimulation(result);
      setLogs((previous) => [
        ...previous,
        `${getSimulationAgents(result).length} agent outputs received.`,
        `Final decision generated: ${result.final_decision}`,
      ]);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setError(message);
      setLogs((previous) => [...previous, `Simulation failed: ${message}`]);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <main className="scanline cyber-grid min-h-screen bg-[#050816] text-white">
      <div className="flex min-h-screen">
        <Sidebar />

        <div className="flex-1">
          <div className="mx-auto max-w-[1600px] space-y-5 p-5">
            <TopBar isRunning={isRunning} />

            {error ? (
              <div className="rounded-xl border border-red-400/30 bg-red-400/10 p-4 font-mono text-xs text-red-200">
                {error}
              </div>
            ) : null}

            <section className="grid gap-5 xl:grid-cols-[340px_1fr_380px]">
              <ScenarioPanel
                isLoading={isLoadingScenarios}
                isRunning={isRunning}
                scenarios={scenarios}
                selectedScenario={selectedScenario}
                selectedScenarioId={selectedScenarioId}
                onRefresh={loadScenarios}
                onSelect={(id) => {
                  setSelectedScenarioId(id);
                  setSimulation(null);
                }}
                onStart={runSimulation}
              />
              <DecisionCore agents={agents} isRunning={isRunning} simulation={simulation} />
              <LiveFeed logs={logs} />
            </section>

            <section className="grid gap-5 xl:grid-cols-[1fr_420px]">
              <AgentDebateConsole messages={debateMessages} />
              <ContributionPanel data={contributionData} simulation={simulation} />
            </section>

            <section className="grid gap-5 xl:grid-cols-[1fr_430px]">
              <AgentRegistry agents={agents} />
              <FinalDecision
                decision={finalDecision}
                isRunning={isRunning}
                score={simulation?.final_score}
              />
            </section>

            <ExecutiveDecisionReport
              agents={agents}
              scenario={selectedScenario}
              simulation={simulation}
            />
          </div>
        </div>
      </div>
    </main>
  );
}

function Sidebar() {
  const navItems = [
    { label: "Mission Control", icon: LayoutDashboard, active: true },
    { label: "New Simulation", icon: PlusCircle },
    { label: "Agent Registry", icon: Users },
    { label: "Live Analysis", icon: Radio },
    { label: "What-if Lab", icon: FlaskConical },
    { label: "Reports", icon: FileText },
    { label: "History", icon: History },
    { label: "System Settings", icon: Settings },
  ];

  return (
    <aside className="hidden w-72 shrink-0 border-r border-cyan-400/20 bg-slate-950/90 p-5 shadow-[0_0_35px_rgba(34,211,238,0.10)] backdrop-blur-xl xl:block">
      <div className="mb-8 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/40 bg-cyan-400/10">
          <Brain className="h-5 w-5 text-cyan-300" />
        </div>
        <div>
          <p className="text-sm font-black tracking-widest text-white">DECISION OS</p>
          <p className="font-mono text-[10px] text-cyan-300">Agentic Command Layer</p>
        </div>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={`flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left font-mono text-xs transition ${
                item.active
                  ? "border-cyan-400/40 bg-cyan-400/10 text-cyan-300"
                  : "border-transparent text-slate-400 hover:border-cyan-400/20 hover:bg-cyan-400/5 hover:text-cyan-200"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

function TopBar({ isRunning }: { isRunning: boolean }) {
  return (
    <motion.header
      initial={{ opacity: 0, y: -18 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-cyan-400/30 bg-slate-950/80 p-5 shadow-[0_0_35px_rgba(34,211,238,0.18)] backdrop-blur-xl"
    >
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-400/40 bg-cyan-400/10">
            <Brain className="h-7 w-7 text-cyan-300" />
          </div>
          <div>
            <h1 className="text-2xl font-black tracking-tight text-white">
              AI Decision Ecosystem Engine
            </h1>
            <p className="font-mono text-xs text-cyan-300">
              Multi-Agent Executive Intelligence Cockpit
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 font-mono text-[11px]">
          <Pill icon={<ShieldCheck size={14} />} text="BACKEND API" color="emerald" />
          <Pill icon={<Cpu size={14} />} text={`${API_BASE_URL}`} color="cyan" />
          <Pill
            icon={isRunning ? <Loader2 size={14} className="animate-spin" /> : <Activity size={14} />}
            text={isRunning ? "SIMULATION RUNNING" : "READY"}
            color="purple"
          />
        </div>
      </div>
    </motion.header>
  );
}

function ScenarioPanel({
  isLoading,
  isRunning,
  scenarios,
  selectedScenario,
  selectedScenarioId,
  onRefresh,
  onSelect,
  onStart,
}: {
  isLoading: boolean;
  isRunning: boolean;
  scenarios: Scenario[];
  selectedScenario: Scenario | null;
  selectedScenarioId: number | null;
  onRefresh: () => void;
  onSelect: (id: number) => void;
  onStart: () => void;
}) {
  const rows = selectedScenario
    ? [
        ["Project", selectedScenario.name],
        ["Budget", `$${selectedScenario.budget_million_usd}M`],
        ["Expected ROI", `${selectedScenario.expected_roi_percent}%`],
        ["Risk Level", `${selectedScenario.risk_level}/10`],
        ["Team Readiness", `${selectedScenario.team_readiness}/10`],
      ]
    : [["Status", isLoading ? "Loading scenarios..." : "No scenario selected"]];

  return (
    <Panel title="Scenario Input" subtitle="Loaded from /api/v1/scenarios">
      <div className="space-y-3">
        <div className="flex gap-2">
          <select
            value={selectedScenarioId ?? ""}
            disabled={isLoading || scenarios.length === 0 || isRunning}
            onChange={(event) => onSelect(Number(event.target.value))}
            className="min-w-0 flex-1 rounded-xl border border-cyan-400/20 bg-black/60 px-3 py-3 font-mono text-xs text-white outline-none focus:border-cyan-300"
          >
            {scenarios.length === 0 ? (
              <option value="">No scenarios</option>
            ) : (
              scenarios.map((scenario) => (
                <option key={scenario.id} value={scenario.id}>
                  #{scenario.id} {scenario.name}
                </option>
              ))
            )}
          </select>
          <button
            type="button"
            onClick={onRefresh}
            disabled={isLoading || isRunning}
            className="flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-400/30 bg-cyan-400/10 text-cyan-300 disabled:opacity-50"
            title="Refresh scenarios"
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
          </button>
        </div>

        {rows.map(([label, value]) => (
          <Metric key={label} label={label} value={value} />
        ))}

        {selectedScenario ? (
          <div className="rounded-xl border border-cyan-400/10 bg-black/40 p-3">
            <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
              Description
            </p>
            <p className="mt-1 text-xs leading-relaxed text-slate-300">
              {selectedScenario.description}
            </p>
          </div>
        ) : null}

        <button
          onClick={onStart}
          disabled={isRunning || !selectedScenarioId}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-cyan-400/50 bg-cyan-400/15 px-4 py-3 font-mono text-xs font-bold uppercase text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isRunning ? <Loader2 size={16} className="animate-spin" /> : <Zap size={16} />}
          {isRunning ? "Simulation Running" : "Start Simulation"}
        </button>
      </div>
    </Panel>
  );
}

function DecisionCore({
  agents,
  isRunning,
  simulation,
}: {
  agents: Agent[];
  isRunning: boolean;
  simulation: SimulationDetailResponse | null;
}) {
  const statusFor = (id: string) =>
    isRunning ? "ANALYZING" : agents.find((agent) => agent.id === id)?.status ?? "IDLE";

  return (
    <Panel title="Decision Core Network" subtitle="Live backend simulation state">
      <div className="relative flex min-h-[470px] items-center justify-center overflow-hidden rounded-2xl border border-cyan-400/10 bg-black/40">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.20),transparent_45%)]" />
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="relative flex h-56 w-56 items-center justify-center rounded-full border border-cyan-300/50 bg-cyan-400/10 shadow-[0_0_80px_rgba(34,211,238,0.3)]"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 18, ease: "linear" }}
            className="absolute inset-[-28px] rounded-full border border-dashed border-cyan-300/30"
          />
          <div className="text-center">
            <p className="font-mono text-xs tracking-[0.4em] text-cyan-300">DECISION</p>
            <p className="text-3xl font-black text-white">CORE</p>
            <p className="mt-2 font-mono text-xs text-slate-400">
              {simulation ? `${simulation.final_score}/100` : "Awaiting run"}
            </p>
          </div>

          <CoreNode label="CEO" className="-top-14 left-1/2 -translate-x-1/2" color="cyan" status={statusFor("ceo")} />
          <CoreNode label="CFO" className="right-[-92px] top-1/2 -translate-y-1/2" color="emerald" status={statusFor("cfo")} />
          <CoreNode label="HR" className="-bottom-14 left-1/2 -translate-x-1/2" color="amber" status={statusFor("hr")} />
          <CoreNode label="API" className="left-[-92px] top-1/2 -translate-y-1/2" color="purple" status={isRunning ? "ANALYZING" : simulation ? "COMPLETED" : "IDLE"} />
        </motion.div>
      </div>
    </Panel>
  );
}

function AgentDebateConsole({ messages }: { messages: DebateMessage[] }) {
  return (
    <Panel title="Agent Debate Console" subtitle="Derived from simulation response">
      {messages.length === 0 ? (
        <EmptyState text="Run a simulation to see real agent rationales." />
      ) : (
        <div className="space-y-3">
          {messages.map((message) => (
            <div key={message.id} className="rounded-xl border border-cyan-400/10 bg-black/40 p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="font-mono text-sm font-bold text-white">{message.agent}</h3>
                <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 font-mono text-[10px] uppercase text-cyan-200">
                  {message.stance} | {message.confidence}%
                </span>
              </div>
              <p className="mt-2 text-sm leading-relaxed text-slate-300">{message.reasoning}</p>
            </div>
          ))}
        </div>
      )}
    </Panel>
  );
}

function LiveFeed({ logs }: { logs: string[] }) {
  return (
    <Panel title="Live Analysis" subtitle="API activity and simulation events">
      <div className="max-h-[420px] space-y-3 overflow-auto pr-1">
        {logs.map((log, index) => (
          <div
            key={`${log}-${index}`}
            className="rounded-xl border border-cyan-400/10 bg-black/40 p-3"
          >
            <p className="font-mono text-[10px] uppercase tracking-widest text-cyan-300">
              Event {String(index + 1).padStart(2, "0")}
            </p>
            <p className="mt-1 text-xs leading-relaxed text-slate-300">{log}</p>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function ContributionPanel({
  data,
  simulation,
}: {
  data: ContributionDatum[];
  simulation: SimulationDetailResponse | null;
}) {
  return (
    <Panel title="Contribution Data" subtitle="Agent weights or returned scores">
      {data.length === 0 ? (
        <EmptyState text="Contribution chart will populate after simulation." />
      ) : (
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={data} dataKey="value" nameKey="name" outerRadius={96} label>
                {data.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "#020617",
                  border: "1px solid rgba(34,211,238,0.3)",
                  borderRadius: 12,
                  color: "#fff",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <Metric label="Consensus" value={boolValue(simulation?.consensus_reached)} />
        <Metric label="Stability" value={boolValue(simulation?.stability_reached)} />
        <Metric label="Scenario Type" value={simulation?.scenario_type ?? "Not returned"} />
        <Metric
          label="Type Confidence"
          value={
            simulation?.scenario_type_confidence == null
              ? "Not returned"
              : `${Math.round(simulation.scenario_type_confidence * 100)}%`
          }
        />
      </div>
    </Panel>
  );
}

function AgentRegistry({ agents }: { agents: Agent[] }) {
  return (
    <Panel title="Agent Registry" subtitle="Scores and rationales from backend">
      <div className="grid gap-4 lg:grid-cols-3">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className={`rounded-2xl border bg-black/40 p-5 ${agentBorderClass(agent.color, agent.status)}`}
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-bold text-white">{agent.name}</h3>
                <p className="mt-1 text-xs text-slate-400">{agent.role}</p>
              </div>
              <StatusBadge status={agent.status} />
            </div>
            <div className="mt-5 grid grid-cols-2 gap-3">
              <Metric label="Score" value={`${agent.score}/100`} />
              <Metric label="Confidence" value={`${agent.confidence}%`} />
            </div>
            <p className="mt-4 text-sm leading-relaxed text-slate-300">{agent.reasoning}</p>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function FinalDecision({
  decision,
  isRunning,
  score,
}: {
  decision: string;
  isRunning: boolean;
  score?: number;
}) {
  const tone = decisionTone(decision);
  const toneClass = {
    emerald: "border-emerald-400/40 bg-emerald-400/10 text-emerald-300",
    amber: "border-amber-400/40 bg-amber-400/10 text-amber-300",
    red: "border-red-400/40 bg-red-400/10 text-red-300",
  }[tone];

  return (
    <Panel title="Final Decision" subtitle="Backend recommendation">
      <motion.div
        key={`${decision}-${score ?? "empty"}`}
        initial={{ opacity: 0, scale: 0.97 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`rounded-2xl border p-5 ${toneClass}`}
      >
        <p className="font-mono text-xs uppercase tracking-[0.3em]">
          {isRunning ? "Calculating" : "Recommendation"}
        </p>
        <h3 className="mt-3 text-5xl font-black">{isRunning ? "RUNNING" : decision}</h3>
        <div className="mt-5 grid grid-cols-2 gap-3">
          <Metric label="Final Score" value={score == null ? "Not ready" : `${score}/100`} />
          <Metric label="Endpoint" value="POST /simulate" />
        </div>
      </motion.div>
    </Panel>
  );
}

function ExecutiveDecisionReport({
  agents,
  scenario,
  simulation,
}: {
  agents: Agent[];
  scenario: Scenario | null;
  simulation: SimulationDetailResponse | null;
}) {
  const [copied, setCopied] = useState(false);
  const reportText = useMemo(() => {
    const lines = [
      "AI Decision Ecosystem Engine - Executive Decision Report",
      "",
      `Scenario: ${scenario?.name ?? "Not selected"}`,
      `Description: ${scenario?.description ?? "Not available"}`,
      "",
      "Inputs:",
      `- Budget: ${scenario ? `$${scenario.budget_million_usd}M` : "Not available"}`,
      `- Expected ROI: ${scenario ? `${scenario.expected_roi_percent}%` : "Not available"}`,
      `- Risk Level: ${scenario ? `${scenario.risk_level}/10` : "Not available"}`,
      `- Team Readiness: ${scenario ? `${scenario.team_readiness}/10` : "Not available"}`,
      "",
      "Agent Findings:",
      ...agents.map(
        (agent) =>
          `- ${agent.name}: Score ${agent.score}/100 | Confidence ${agent.confidence}%\n  ${agent.reasoning}`,
      ),
      "",
      `Final Score: ${simulation?.final_score ?? "Not available"}`,
      `Final Decision: ${simulation?.final_decision ?? "Not available"}`,
    ];

    return lines.join("\n");
  }, [agents, scenario, simulation]);

  const copyReport = async () => {
    await navigator.clipboard.writeText(reportText);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  const downloadReport = () => {
    const blob = new Blob([reportText], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "ai-decision-executive-report.txt";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Panel title="Executive Decision Report" subtitle="Generated from current API state">
      <div className="mb-5 flex flex-col gap-3 rounded-2xl border border-cyan-400/10 bg-black/40 p-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
            Report Actions
          </p>
          <p className="mt-1 text-xs text-slate-400">
            Copy or download the current backend-generated decision summary.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={copyReport}
            className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-3 py-2 font-mono text-xs text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
          >
            <Copy size={14} />
            {copied ? "Copied" : "Copy Report"}
          </button>
          <button
            onClick={downloadReport}
            className="inline-flex items-center gap-2 rounded-xl border border-emerald-400/30 bg-emerald-400/10 px-3 py-2 font-mono text-xs text-emerald-300 transition hover:bg-emerald-400 hover:text-slate-950"
          >
            <Download size={14} />
            Download TXT
          </button>
        </div>
      </div>

      <pre className="max-h-96 overflow-auto whitespace-pre-wrap rounded-2xl border border-white/10 bg-black/40 p-5 text-xs leading-relaxed text-slate-300">
        {reportText}
      </pre>
    </Panel>
  );
}

function Panel({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-cyan-400/20 bg-slate-950/80 p-5 shadow-[0_0_35px_rgba(34,211,238,0.10)] backdrop-blur-xl"
    >
      <div className="mb-5">
        <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
          {title}
        </p>
        <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
      </div>
      {children}
    </motion.section>
  );
}

function CoreNode({
  label,
  className,
  color,
  status,
}: {
  label: string;
  className: string;
  color: AgentColor;
  status: AgentStatus;
}) {
  return (
    <motion.div
      animate={
        status === "ANALYZING"
          ? { scale: [1, 1.12, 1], opacity: [0.85, 1, 0.85] }
          : { scale: 1, opacity: status === "IDLE" ? 0.55 : 1 }
      }
      transition={{ repeat: status === "ANALYZING" ? Infinity : 0, duration: 1.2 }}
      className={`absolute rounded-full border bg-black px-4 py-2 font-mono text-[10px] font-bold shadow-lg ${nodeColorClass(color, status)} ${className}`}
    >
      {label}
    </motion.div>
  );
}

function StatusBadge({ status }: { status: AgentStatus }) {
  const Icon =
    status === "WARNING"
      ? AlertTriangle
      : status === "COMPLETED"
        ? CheckCircle2
        : status === "ANALYZING"
          ? Loader2
          : Activity;

  return (
    <div className={`rounded-full border px-2 py-1 font-mono text-[10px] ${statusBadgeClass(status)}`}>
      <Icon className={`mr-1 inline h-3 w-3 ${status === "ANALYZING" ? "animate-spin" : ""}`} />
      {status}
    </div>
  );
}

function Pill({
  icon,
  text,
  color,
}: {
  icon: ReactNode;
  text: string;
  color: "emerald" | "cyan" | "purple";
}) {
  const colorClass = {
    emerald: "border-emerald-400/40 bg-emerald-400/10 text-emerald-300",
    cyan: "border-cyan-400/40 bg-cyan-400/10 text-cyan-300",
    purple: "border-purple-400/40 bg-purple-400/10 text-purple-300",
  }[color];

  return (
    <span className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 ${colorClass}`}>
      {icon}
      {text}
    </span>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-cyan-400/10 bg-black/40 p-3">
      <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">{label}</p>
      <p className="mt-1 break-words text-sm font-semibold text-white">{value}</p>
    </div>
  );
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="rounded-xl border border-cyan-400/10 bg-black/40 p-4">
      <p className="font-mono text-xs text-slate-400">{text}</p>
    </div>
  );
}

function boolValue(value?: boolean) {
  if (value == null) return "Not returned";
  return value ? "Reached" : "Not reached";
}

function chartColor(color: AgentColor) {
  if (color === "emerald") return "#34d399";
  if (color === "amber") return "#fbbf24";
  if (color === "purple") return "#a855f7";
  return "#22d3ee";
}

function statusBadgeClass(status: AgentStatus) {
  if (status === "WARNING") return "border-amber-400 text-amber-300";
  if (status === "COMPLETED") return "border-emerald-400 text-emerald-300";
  if (status === "ANALYZING") return "border-cyan-400 text-cyan-300";
  return "border-slate-500 text-slate-400";
}

function agentBorderClass(color: AgentColor, status: AgentStatus) {
  if (status === "IDLE") return "border-slate-700/80";
  if (color === "amber") return "border-amber-400/70 shadow-[0_0_25px_rgba(251,191,36,0.18)]";
  if (color === "emerald") return "border-emerald-400/60 shadow-[0_0_25px_rgba(52,211,153,0.18)]";
  if (color === "purple") return "border-purple-400/60 shadow-[0_0_25px_rgba(168,85,247,0.18)]";
  return "border-cyan-400/60 shadow-[0_0_25px_rgba(34,211,238,0.18)]";
}

function nodeColorClass(color: AgentColor, status: AgentStatus) {
  if (status === "IDLE") return "border-slate-600 text-slate-400 shadow-slate-500/10";
  if (status === "WARNING") return "border-amber-400 text-amber-300 shadow-amber-400/40";
  if (color === "emerald") return "border-emerald-400 text-emerald-300 shadow-emerald-400/30";
  if (color === "amber") return "border-amber-400 text-amber-300 shadow-amber-400/30";
  if (color === "purple") return "border-purple-400 text-purple-300 shadow-purple-400/30";
  return "border-cyan-400 text-cyan-300 shadow-cyan-400/30";
}
