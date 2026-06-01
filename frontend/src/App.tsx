import {
  Cell,
  Pie,
  PieChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle2,
  Cpu,
  Network,
  ShieldCheck,
  Zap,
  Loader2,
  LayoutDashboard,
  FlaskConical,
  FileText,
  History,
  Settings,
  Users,
  Radio,
  PlusCircle,
  Copy,
  Download,
  Check,
} from "lucide-react";
import type {
  Agent,
  AgentColor,
  AgentStatus,
  DebateMessage,
} from "./types/decision";
import {
  agentDebateMessages,
  completedAgents,
  contributionData,
  executiveReportText,
  initialAgents,
  initialLogs,
  reportAgentFindings,
  reportNextSteps,
  scenarioRows,
} from "./data/mockDecision";
import { decisionApi } from "./api/decisionApi";
import type {
  ApiAgentOutput,
  ApiScenario,
  ApiSimulationResponse,
} from "./types/api";


const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export default function App() {
  const [agents, setAgents] = useState<Agent[]>(initialAgents);
  const [logs, setLogs] = useState<string[]>(initialLogs);
const [scenarios, setScenarios] = useState<ApiScenario[]>([]);
const [selectedScenarioId, setSelectedScenarioId] = useState("");
const [scenarioLoading, setScenarioLoading] = useState(true);
const [scenarioError, setScenarioError] = useState<string | null>(null);
const [debateMessages, setDebateMessages] = useState<DebateMessage[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [classifierStatus, setClassifierStatus] = useState<AgentStatus>("IDLE");
  const [aggregatorStatus, setAggregatorStatus] = useState<AgentStatus>("IDLE");
  const [explainStatus, setExplainStatus] = useState<AgentStatus>("IDLE");
  const [finalVisible, setFinalVisible] = useState(false);
const [simulationResult, setSimulationResult] =
  useState<ApiSimulationResponse | null>(null);

const [simulationLoading, setSimulationLoading] = useState(false);
const [simulationError, setSimulationError] = useState<string | null>(null);

  const addLog = async (message: string, delay = 450) => {
    setLogs((prev) => [...prev, message]);
    await wait(delay);
  };
const addDebateMessage = async (message: DebateMessage, delay = 500) => {
  setDebateMessages((prev) => [...prev, message]);
  await wait(delay);
};

  const updateAgent = (id: string, patch: Partial<Agent>) => {
    setAgents((prev) =>
      prev.map((agent) => (agent.id === id ? { ...agent, ...patch } : agent))
    );
  };
useEffect(() => {
  let ignore = false;

  const loadScenarios = async () => {
    try {
      setScenarioLoading(true);
      setScenarioError(null);

      const data = await decisionApi.getScenarios();

      if (ignore) return;

      setScenarios(data);

      if (data.length > 0) {
        setSelectedScenarioId(String(data[0].id));
      }
    } catch (error) {
      if (ignore) return;

      setScenarioError(
        error instanceof Error
          ? error.message
          : "Backend scenario list could not be loaded."
      );
    } finally {
      if (!ignore) {
        setScenarioLoading(false);
      }
    }
  };

  loadScenarios();

  return () => {
    ignore = true;
  };
}, []);

const selectedScenario =
  scenarios.find((scenario) => String(scenario.id) === selectedScenarioId) ??
  null;

  const runSimulation = async () => {
if (isRunning || simulationLoading) return;

  if (!selectedScenarioId) {
    setSimulationError("Please select a scenario before starting simulation.");
    return;
  }

  setIsRunning(true);
  setSimulationLoading(true);
  setSimulationError(null);
  setSimulationResult(null);

  try {
    const result = await decisionApi.simulateScenario(selectedScenarioId);
    setSimulationResult(result);
const backendAgents = result.agent_outputs.map(mapApiAgentToCockpitAgent);

if (backendAgents.length > 0) {
  setAgents(backendAgents);
}

await addLog(
  `Backend simulation completed: ${result.final_decision} | Score ${result.final_score}`
);
    if (isRunning) return;

    setIsRunning(true);
    setFinalVisible(false);
    setAgents(initialAgents);
    setClassifierStatus("IDLE");
    setAggregatorStatus("IDLE");
    setExplainStatus("IDLE");
    setLogs([]);
    setDebateMessages([]);

    await addLog("Scenario received: AI Market Expansion Initiative");
    setClassifierStatus("ANALYZING");
    await addLog("Scenario Classifier initialized...");
    await addLog("Analyzing budget, ROI, risk and team readiness...");
    setClassifierStatus("COMPLETED");
    await addLog("Scenario type detected: TEAM_EXPANSION");

    updateAgent("ceo", {
      status: "ANALYZING",
      reasoning: "Scanning strategic alignment and market opportunity...",
    });
    await addLog("CEO Agent analyzing strategic alignment...");
    updateAgent("ceo", completedAgents[0]);
    await addLog("CEO Agent completed: Score 85 | Confidence 91%");
await addDebateMessage(agentDebateMessages[0]);

    updateAgent("cfo", {
      status: "ANALYZING",
      reasoning: "Evaluating budget exposure and expected return...",
    });
    await addLog("CFO Agent evaluating financial feasibility...");
    updateAgent("cfo", completedAgents[1]);
    await addLog("CFO Agent completed: Score 90 | Confidence 88%");
await addDebateMessage(agentDebateMessages[1]);

    updateAgent("hr", {
      status: "ANALYZING",
      reasoning: "Checking team readiness and hiring pressure...",
    });
    await addLog("HR Agent checking workforce capacity...");
    updateAgent("hr", completedAgents[2]);
    await addLog("HR Agent warning: Team readiness insufficient");
await addDebateMessage(agentDebateMessages[2]);

    setAggregatorStatus("ANALYZING");
    await addLog("Aggregator applying dynamic weights...");
await addDebateMessage(agentDebateMessages[3]);
await addDebateMessage(agentDebateMessages[4]);
await addDebateMessage(agentDebateMessages[5]);
    await addLog("CEO weight: 25%");
    await addLog("CFO weight: 25%");
    await addLog("HR weight: 50%");
    setAggregatorStatus("COMPLETED");
    await addLog("Weighted consensus score calculated: 68.75 / 100");

    setExplainStatus("ANALYZING");
    await addLog("Explanation Engine preparing recommendation...");
    setExplainStatus("COMPLETED");
    await addLog("Primary bottleneck detected: Workforce Capacity");
    await addLog("Final decision generated: REVISE");
await addDebateMessage(agentDebateMessages[6]);

    setFinalVisible(true);
  } catch (error) {
    setSimulationError(
      error instanceof Error
        ? error.message
        : "Simulation request failed."
    );
  } finally {
    setSimulationLoading(false);
    setIsRunning(false);
  }
    setIsRunning(false);
  };

  return (
  <main className="scanline cyber-grid min-h-screen bg-[#050816] text-white">
    <div className="flex min-h-screen">
      <Sidebar />

      <div className="flex-1">
        <div className="mx-auto max-w-[1600px] space-y-5 p-5">
          <div id="mission-control" className="scroll-mt-5">
  <TopBar isRunning={isRunning} />
<ExecutiveKpiStrip finalVisible={finalVisible} isRunning={isRunning} />
</div>
    <MissionTimeline
    agents={agents}
    classifierStatus={classifierStatus}
    aggregatorStatus={aggregatorStatus}
    explainStatus={explainStatus}
    finalVisible={finalVisible}
    />
       <DecisionSignalMatrix />
       <DecisionRadarPanel />
        <section 
        id="new-simulation"
        className="grid scroll-mt-5 gap-5 xl:grid-cols-[320px_1fr_380px]"
         >
         <ScenarioPanel
  isRunning={isRunning}
  onStart={runSimulation}

  scenarios={scenarios}
  selectedScenario={selectedScenario}
  selectedScenarioId={selectedScenarioId}
  onScenarioChange={setSelectedScenarioId}
  scenarioLoading={scenarioLoading}
  scenarioError={scenarioError}
  simulationLoading={simulationLoading}
  simulationError={simulationError}
/>          
 <div id="live-analysis" className="scroll-mt-5">
    <DecisionCore
      agents={agents}
      classifierStatus={classifierStatus}
      aggregatorStatus={aggregatorStatus}
      explainStatus={explainStatus}
    />
  </div>

  <LiveFeed logs={logs} />
</section>

     <section
  id="agent-registry"
  className="grid scroll-mt-5 gap-5 xl:grid-cols-[1fr_430px]"
>
  <AgentRegistry agents={agents} />
<FinalDecision
  visible={finalVisible}
  isRunning={isRunning || simulationLoading}
  simulationResult={simulationResult}
/>
</section>

   <div id="agent-debate" className="scroll-mt-5">
 <AgentDebateConsole
  messages={debateMessages}
  isRunning={isRunning || simulationLoading}
  simulationResult={simulationResult}
/>
</div>

<div id="what-if-lab" className="scroll-mt-5">
  <WhatIfLab />
</div>

<div id="scenario-comparison" className="scroll-mt-5">
  <ScenarioComparisonBoard />
</div>

<div id="action-plan" className="scroll-mt-5">
  <ExecutionActionPlan />
</div>

<div id="reports" className="scroll-mt-5">
  <ExecutiveDecisionReport />
</div>
<div id="history" className="scroll-mt-5">
  <SimulationHistory />
</div>

<div id="system-settings" className="scroll-mt-5">
  <SystemSettingsPanel />
</div>
             </div>
      </div>
    </div>
  </main>
);
}
function Sidebar() {
  const navItems = [
  { label: "Mission Control", icon: LayoutDashboard, target: "mission-control" },
  { label: "New Simulation", icon: PlusCircle, target: "new-simulation" },
  { label: "Agent Registry", icon: Users, target: "agent-registry" },
  { label: "Live Analysis", icon: Radio, target: "live-analysis" },
  { label: "What-if Lab", icon: FlaskConical, target: "what-if-lab" },
  { label: "Reports", icon: FileText, target: "reports" },
  { label: "History", icon: History, target: "history" },
  { label: "System Settings", icon: Settings, target: "system-settings" },
];

const [activeSection, setActiveSection] = useState("mission-control");

const scrollToSection = (target: string) => {
  setActiveSection(target);

  document.getElementById(target)?.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
};
  return (
    <aside className="hidden w-72 shrink-0 border-r border-cyan-400/20 bg-slate-950/90 p-5 shadow-[0_0_35px_rgba(34,211,238,0.10)] backdrop-blur-xl xl:block">
      <div className="mb-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/40 bg-cyan-400/10">
            <Brain className="h-5 w-5 text-cyan-300" />
          </div>

          <div>
            <p className="text-sm font-black tracking-widest text-white">
              DECISION OS
            </p>
            <p className="font-mono text-[10px] text-cyan-300">
              Agentic Command Layer
            </p>
          </div>
        </div>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              onClick={() => scrollToSection(item.target)}
              className={`flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left font-mono text-xs transition ${
                activeSection === item.target
                  ? "border-cyan-400/40 bg-cyan-400/10 text-cyan-300 shadow-[0_0_18px_rgba(34,211,238,0.16)]"
                  : "border-transparent text-slate-400 hover:border-cyan-400/20 hover:bg-cyan-400/5 hover:text-cyan-200"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="mt-8 rounded-2xl border border-cyan-400/20 bg-black/40 p-4">
        <p className="mb-4 font-mono text-[10px] uppercase tracking-widest text-cyan-300">
          System Telemetry
        </p>

        <div className="space-y-3">
          <TelemetryRow label="CPU" value="32%" />
          <TelemetryRow label="Memory" value="47%" />
          <TelemetryRow label="Network" value="Secure" />
          <TelemetryRow label="Data Stream" value="Active" />
        </div>
      </div>

      <div className="mt-5 rounded-xl border border-emerald-400/20 bg-emerald-400/10 p-3">
        <div className="flex items-center gap-2 font-mono text-[10px] text-emerald-300">
          <span className="h-2 w-2 rounded-full bg-emerald-300 shadow-[0_0_12px_rgba(52,211,153,0.9)]" />
          ALL SYSTEMS NOMINAL
        </div>
      </div>
    </aside>
  );
}

function TelemetryRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-b border-white/5 pb-2 last:border-b-0 last:pb-0">
      <span className="font-mono text-[10px] text-slate-500">{label}</span>
      <span className="font-mono text-[10px] font-bold text-white">{value}</span>
    </div>
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
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-400/40 bg-cyan-400/10 shadow-[0_0_25px_rgba(34,211,238,0.35)]">
            <Brain className="h-7 w-7 text-cyan-300" />
          </div>

          <div>
            <h1 className="text-2xl font-black tracking-tight text-white drop-shadow-[0_0_12px_rgba(34,211,238,0.7)]">
              AI Decision Ecosystem Engine
            </h1>
            <p className="font-mono text-xs text-cyan-300">
              Multi-Agent Executive Intelligence Cockpit
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 font-mono text-[11px]">
          <Pill icon={<ShieldCheck size={14} />} text="SYSTEM ONLINE" color="emerald" />
          <Pill icon={<Cpu size={14} />} text="AGENTS ACTIVE: 6/6" color="cyan" />
          <Pill
            icon={isRunning ? <Loader2 size={14} className="animate-spin" /> : <Activity size={14} />}
            text={isRunning ? "SIMULATION RUNNING" : "BOARDROOM SIMULATION"}
            color="purple"
          />
        </div>
      </div>
    </motion.header>
  );
}
function ExecutiveKpiStrip({
  finalVisible,
  isRunning,
}: {
  finalVisible: boolean;
  isRunning: boolean;
}) {
  const kpis = [
    {
      label: "Final Decision",
      value: finalVisible ? "REVISE" : isRunning ? "CALCULATING" : "WAITING",
      detail: finalVisible ? "Revision required" : "Awaiting simulation",
      tone: finalVisible ? "amber" : isRunning ? "cyan" : "slate",
    },
    {
      label: "Overall Score",
      value: finalVisible ? "68.75" : "--",
      detail: "/100 weighted consensus",
      tone: "cyan",
    },
    {
      label: "Primary Bottleneck",
      value: finalVisible ? "Workforce" : "--",
      detail: finalVisible ? "Capacity risk detected" : "Not analyzed yet",
      tone: finalVisible ? "amber" : "slate",
    },
    {
      label: "Confidence",
      value: finalVisible ? "82%" : "--",
      detail: "Explainability confidence",
      tone: "emerald",
    },
  ];

  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {kpis.map((kpi, index) => (
        <motion.div
          key={kpi.label}
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          className={`rounded-2xl border bg-slate-950/80 p-4 shadow-[0_0_25px_rgba(34,211,238,0.08)] backdrop-blur-xl ${kpiCardClass(
            kpi.tone
          )}`}
        >
          <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-slate-500">
            {kpi.label}
          </p>

          <div className="mt-3 flex items-end justify-between gap-3">
            <h3 className={`text-2xl font-black ${kpiValueClass(kpi.tone)}`}>
              {kpi.value}
            </h3>

            <span className={`h-2 w-2 rounded-full ${kpiDotClass(kpi.tone)}`} />
          </div>

          <p className="mt-2 text-xs text-slate-400">{kpi.detail}</p>
        </motion.div>
      ))}
    </section>
  );
}
function MissionTimeline({
  agents,
  classifierStatus,
  aggregatorStatus,
  explainStatus,
  finalVisible,
}: {
  agents: Agent[];
  classifierStatus: AgentStatus;
  aggregatorStatus: AgentStatus;
  explainStatus: AgentStatus;
  finalVisible: boolean;
}) {
  const getAgentStatus = (id: string) =>
    agents.find((agent) => agent.id === id)?.status ?? "IDLE";

  const steps = [
    {
      label: "Scenario",
      status: "COMPLETED" as AgentStatus,
      detail: "Input locked",
    },
    {
      label: "Classifier",
      status: classifierStatus,
      detail: "Type detection",
    },
    {
      label: "CEO",
      status: getAgentStatus("ceo"),
      detail: "Strategy",
    },
    {
      label: "CFO",
      status: getAgentStatus("cfo"),
      detail: "Finance",
    },
    {
      label: "HR",
      status: getAgentStatus("hr"),
      detail: "Workforce",
    },
    {
      label: "Aggregator",
      status: aggregatorStatus,
      detail: "Weighted score",
    },
    {
      label: "Explain",
      status: explainStatus,
      detail: "Recommendation",
    },
    {
      label: "Final",
      status: finalVisible ? ("COMPLETED" as AgentStatus) : ("IDLE" as AgentStatus),
      detail: finalVisible ? "REVISE" : "Awaiting",
    },
  ];

  return (
    <section className="rounded-2xl border border-cyan-400/20 bg-slate-950/80 p-5 shadow-[0_0_30px_rgba(34,211,238,0.12)] backdrop-blur-xl">
      <div className="mb-4 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-sm font-bold text-cyan-300 drop-shadow-[0_0_10px_rgba(34,211,238,0.7)]">
            Mission Timeline
          </h2>
          <p className="mt-1 font-mono text-xs text-slate-500">
            Real-time decision pipeline status
          </p>
        </div>

        <span className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 font-mono text-[10px] text-cyan-300">
          EXECUTIVE PIPELINE
        </span>
      </div>

      <div className="grid gap-3 md:grid-cols-4 xl:grid-cols-8">
        {steps.map((step, index) => (
          <motion.div
            key={step.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.04 }}
            className={`rounded-xl border bg-black/40 p-3 ${timelineStatusClass(
              step.status
            )}`}
          >
            <div className="mb-3 flex items-center justify-between">
              <span className="font-mono text-[10px] text-slate-500">
                {String(index + 1).padStart(2, "0")}
              </span>

              <span
                className={`h-2 w-2 rounded-full ${timelineDotClass(
                  step.status
                )}`}
              />
            </div>

            <p className="text-sm font-bold text-white">{step.label}</p>
            <p className="mt-1 font-mono text-[10px] text-slate-500">
              {step.detail}
            </p>

            <p className={`mt-3 font-mono text-[10px] ${timelineTextClass(step.status)}`}>
              {step.status}
            </p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
function DecisionSignalMatrix() {
  const signals = [
    {
      label: "Strategic Fit",
      value: 85,
      status: "STRONG",
      description: "High alignment with growth and market expansion goals.",
      tone: "cyan",
    },
    {
      label: "Financial Viability",
      value: 90,
      status: "STRONG",
      description: "Expected ROI is attractive and budget exposure is acceptable.",
      tone: "emerald",
    },
    {
      label: "Workforce Capacity",
      value: 50,
      status: "BOTTLENECK",
      description: "Team readiness is below the recommended execution threshold.",
      tone: "amber",
    },
    {
      label: "Risk Exposure",
      value: 62,
      status: "MODERATE",
      description: "Risk is manageable, but execution capacity needs revision.",
      tone: "purple",
    },
  ];

  return (
    <Panel
      title="Decision Signal Matrix"
      subtitle="High-level decision signals behind the final recommendation"
    >
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {signals.map((signal, index) => (
          <motion.div
            key={signal.label}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06 }}
            className={`rounded-2xl border bg-black/40 p-4 ${signalCardClass(
              signal.tone
            )}`}
          >
            <div className="mb-4 flex items-start justify-between gap-3">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-slate-500">
                  Signal
                </p>
                <h3 className="mt-1 text-base font-black text-white">
                  {signal.label}
                </h3>
              </div>

              <span className={`rounded-full border px-2 py-1 font-mono text-[10px] ${signalBadgeClass(signal.tone)}`}>
                {signal.status}
              </span>
            </div>

            <div className="mb-3 flex items-end justify-between">
              <span className="text-3xl font-black text-white">
                {signal.value}
              </span>
              <span className="font-mono text-[10px] text-slate-500">
                /100
              </span>
            </div>

            <div className="h-2 overflow-hidden rounded-full bg-slate-800">
              <div
                className={`h-full rounded-full ${signalBarClass(signal.tone)}`}
                style={{ width: `${signal.value}%` }}
              />
            </div>

            <p className="mt-4 text-xs leading-relaxed text-slate-300">
              {signal.description}
            </p>
          </motion.div>
        ))}
      </div>
    </Panel>
  );
}
function DecisionRadarPanel() {
  const radarData = [
    { metric: "Strategy", value: 85 },
    { metric: "Finance", value: 90 },
    { metric: "Workforce", value: 50 },
    { metric: "Risk Control", value: 62 },
    { metric: "Market", value: 70 },
    { metric: "Execution", value: 58 },
  ];

  return (
    <Panel
      title="Decision Radar"
      subtitle="Radar view of decision strength, risk and execution readiness"
    >
      <div className="grid gap-5 xl:grid-cols-[1fr_380px]">
        <div className="h-[360px] rounded-2xl border border-cyan-400/10 bg-black/40 p-4">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(34,211,238,0.18)" />
              <PolarAngleAxis
                dataKey="metric"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
              />
              <PolarRadiusAxis
                angle={90}
                domain={[0, 100]}
                tick={{ fill: "#64748b", fontSize: 10 }}
              />
              <Radar
                name="Decision Strength"
                dataKey="value"
                stroke="#22d3ee"
                fill="#22d3ee"
                fillOpacity={0.18}
              />
              <Tooltip
                contentStyle={{
                  background: "#020617",
                  border: "1px solid rgba(34,211,238,0.25)",
                  borderRadius: "12px",
                  color: "#fff",
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-2xl border border-amber-400/30 bg-amber-400/10 p-5 shadow-[0_0_35px_rgba(251,191,36,0.12)]">
          <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-amber-300">
            Radar Insight
          </p>

          <h3 className="mt-3 text-2xl font-black text-white">
            Workforce is the weakest signal
          </h3>

          <p className="mt-3 text-sm leading-relaxed text-slate-300">
            Strategy and financial signals are strong, but workforce readiness
            and execution capacity reduce the final decision confidence. This
            explains why the system recommends revision instead of approval.
          </p>

          <div className="mt-5 space-y-3">
            <Metric label="Strongest Signal" value="Finance 90" />
            <Metric label="Weakest Signal" value="Workforce 50" />
            <Metric label="Decision Pressure" value="Execution Risk" />
            <Metric label="Recommended Action" value="Capacity Plan" />
          </div>
        </div>
      </div>
    </Panel>
  );
}
function ScenarioPanel({
  isRunning,
  onStart,
  scenarios,
  selectedScenario,
  selectedScenarioId,
  onScenarioChange,
  scenarioLoading,
  scenarioError,
simulationLoading,
simulationError,
}: {
  isRunning: boolean;
  onStart: () => void;
  scenarios: ApiScenario[];
  selectedScenario: ApiScenario | null;
  selectedScenarioId: string;
  onScenarioChange: (id: string) => void;
  scenarioLoading: boolean;
  scenarioError: string | null;
simulationLoading: boolean;
simulationError: string | null;
}) {
  const rows: [string, string][] = selectedScenario
    ? [
        [
          "Project",
          selectedScenario.title ??
            selectedScenario.name ??
            `Scenario ${selectedScenario.id}`,
        ],
        [
          "Budget",
          selectedScenario.budget !== undefined
            ? `$${selectedScenario.budget}M`
            : "--",
        ],
        [
          "Expected ROI",
          selectedScenario.expected_roi !== undefined
            ? `${selectedScenario.expected_roi}%`
            : "--",
        ],
        [
          "Risk Level",
          selectedScenario.risk_level !== undefined
            ? `${selectedScenario.risk_level}/10`
            : "--",
        ],
        [
          "Team Readiness",
          selectedScenario.team_readiness !== undefined
            ? `${selectedScenario.team_readiness}/10`
            : "--",
        ],
        [
          "Market Confidence",
          selectedScenario.market_confidence !== undefined
            ? `${selectedScenario.market_confidence}/10`
            : "--",
        ],
        [
          "Strategic Fit",
          selectedScenario.strategic_fit !== undefined
            ? `${selectedScenario.strategic_fit}/10`
            : "--",
        ],
        ["Scenario Type", selectedScenario.scenario_type ?? "--"],
      ]
    : scenarioRows;

  return (
    <Panel title="Scenario Input" subtitle="Executive decision parameters">
      <div className="space-y-3">
        <div className="rounded-xl border border-cyan-400/10 bg-black/40 p-3">
          <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
            Scenario Source
          </p>

          {scenarioLoading && (
            <p className="mt-2 text-xs text-cyan-300">
              Loading scenarios from backend...
            </p>
          )}

          {scenarioError && (
            <p className="mt-2 rounded-lg border border-red-400/30 bg-red-400/10 p-2 text-xs text-red-300">
              Backend error: {scenarioError}
            </p>
          )}

          {!scenarioLoading && !scenarioError && scenarios.length === 0 && (
            <p className="mt-2 rounded-lg border border-amber-400/30 bg-amber-400/10 p-2 text-xs text-amber-300">
              No scenarios found. Create a scenario from the backend first.
            </p>
          )}

          {scenarios.length > 0 && (
            <select
              value={selectedScenarioId}
              onChange={(event) => onScenarioChange(event.target.value)}
              className="mt-2 w-full rounded-xl border border-cyan-400/20 bg-slate-950 px-3 py-2 font-mono text-xs text-cyan-200 outline-none transition focus:border-cyan-300"
            >
              {scenarios.map((scenario) => (
                <option key={String(scenario.id)} value={String(scenario.id)}>
                  {scenario.title ?? scenario.name ?? `Scenario ${scenario.id}`}
                </option>
              ))}
            </select>
          )}
        </div>

        {rows.map(([label, value]) => (
          <div
            key={label}
            className="rounded-xl border border-cyan-400/10 bg-black/40 p-3"
          >
            <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
              {label}
            </p>
            <p className="mt-1 text-sm font-semibold text-white">{value}</p>
          </div>
        ))}
{simulationError && (
  <p className="rounded-lg border border-red-400/30 bg-red-400/10 p-2 text-xs text-red-300">
    Simulation error: {simulationError}
  </p>
)}

        <button
          onClick={onStart}
         disabled={isRunning || simulationLoading || scenarioLoading || scenarios.length === 0}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-cyan-400/50 bg-cyan-400/15 px-4 py-3 font-mono text-xs font-bold uppercase text-cyan-300 shadow-[0_0_25px_rgba(34,211,238,0.18)] transition hover:bg-cyan-400 hover:text-slate-950 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isRunning ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <Zap size={16} />
          )}
          {isRunning || simulationLoading ? "Simulation Running" : "Start Simulation"}
        </button>
      </div>
    </Panel>
  );
}
function DecisionCore({
  agents,
  classifierStatus,
  aggregatorStatus,
  explainStatus,
}: {
  agents: Agent[];
  classifierStatus: AgentStatus;
  aggregatorStatus: AgentStatus;
  explainStatus: AgentStatus;
}) {
  const getStatus = (id: string) =>
    agents.find((agent) => agent.id === id)?.status ?? "IDLE";

  return (
    <Panel title="Decision Core Network" subtitle="Live multi-agent orchestration">
      <div className="relative flex min-h-[540px] items-center justify-center overflow-hidden rounded-2xl border border-cyan-400/10 bg-black/40">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.18),transparent_50%)]" />

        <div className="relative flex h-64 w-64 items-center justify-center rounded-full border border-cyan-300/50 bg-cyan-400/10 shadow-[0_0_80px_rgba(34,211,238,0.28)]">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 18, ease: "linear" }}
            className="absolute inset-[-34px] rounded-full border border-dashed border-cyan-300/30"
          />

          <div className="text-center">
            <p className="font-mono text-xs tracking-[0.4em] text-cyan-300">
              DECISION
            </p>
            <p className="text-3xl font-black text-white drop-shadow-[0_0_14px_rgba(34,211,238,0.9)]">
              CORE
            </p>
          </div>
        </div>

        <CoreNode
          label="CEO"
          className="left-1/2 top-8 -translate-x-1/2"
          color="cyan"
          status={getStatus("ceo")}
        />

        <CoreNode
          label="CFO"
          className="right-8 top-1/2 -translate-y-1/2"
          color="emerald"
          status={getStatus("cfo")}
        />

        <CoreNode
          label="HR"
          className="bottom-8 left-1/2 -translate-x-1/2"
          color="amber"
          status={getStatus("hr")}
        />

        <CoreNode
          label="CLASSIFIER"
          className="left-8 top-1/2 -translate-y-1/2"
          color="purple"
          status={classifierStatus}
        />

        <CoreNode
          label="AGGREGATOR"
          className="bottom-20 right-8"
          color="cyan"
          status={aggregatorStatus}
        />

        <CoreNode
          label="EXPLAIN"
          className="bottom-20 left-8"
          color="cyan"
          status={explainStatus}
        />
      </div>
    </Panel>
  );
}
function LiveFeed({ logs }: { logs: string[] }) {
   const logEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [logs]);

  return (
    <Panel title="Live Analysis Feed" subtitle="Real-time agent execution stream">
      <div className="space-y-4">
        <div className="h-[420px] overflow-y-auto rounded-xl border border-cyan-400/10 bg-black/70 p-4 pr-2 font-mono text-xs [scrollbar-color:rgba(34,211,238,0.55)_rgba(15,23,42,0.8)] [scrollbar-width:thin]">
          <div className="mb-3 flex items-center gap-2 text-cyan-300">
            <Network size={16} />
            <span>STREAM ACTIVE</span>
          </div>

          <div className="space-y-2">
            {logs.map((log, index) => (
              <motion.p
                key={`${log}-${index}`}
                initial={{ opacity: 0, x: 12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.02 }}
                className={
                  log.toLowerCase().includes("warning") ||
                  log.includes("HR weight")
                    ? "text-amber-300"
                    : log.toLowerCase().includes("final") ||
                        log.toLowerCase().includes("completed")
                      ? "text-emerald-300"
                      : "text-cyan-200"
                }
              >
                <span className="text-slate-500">
                  [{String(index + 1).padStart(2, "0")}]
                </span>{" "}
                &gt; {log}
              </motion.p>
            ))}

            <div ref={logEndRef} />
          </div>
        </div>

        <AgentContributionChart />
      </div>
    </Panel>
  );
}

function AgentContributionChart() {
  return (
    <div className="rounded-xl border border-cyan-400/10 bg-black/60 p-4">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-cyan-300">
            Agent Contribution
          </h3>
          <p className="font-mono text-[10px] text-slate-500">
            Dynamic scenario weights
          </p>
        </div>

        <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-2 py-1 font-mono text-[10px] text-amber-300">
          HR PRIORITY
        </span>
      </div>

      <div className="grid grid-cols-[150px_1fr] items-center gap-4">
        <div className="h-[150px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={contributionData}
                dataKey="value"
                nameKey="name"
                innerRadius={42}
                outerRadius={68}
                paddingAngle={3}
                stroke="rgba(255,255,255,0.12)"
                strokeWidth={1}
              >
                {contributionData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "#020617",
                  border: "1px solid rgba(34,211,238,0.25)",
                  borderRadius: "12px",
                  color: "#fff",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-3">
          {contributionData.map((item) => (
            <div key={item.name}>
              <div className="mb-1 flex items-center justify-between font-mono text-xs">
                <span className="text-slate-300">{item.name} Agent</span>
                <span className="font-bold text-white">{item.value}%</span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: `${item.value}%`,
                    backgroundColor: item.color,
                    boxShadow: `0 0 14px ${item.color}`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function AgentRegistry({ agents }: { agents: Agent[] }) {
  return (
    <Panel title="Agent Registry" subtitle="Specialized executive intelligence agents">
      <div className="grid gap-4 lg:grid-cols-3">
        {agents.map((agent, index) => (
          <motion.article
            key={agent.id}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.08 }}
            className={`rounded-2xl border bg-black/50 p-4 backdrop-blur ${agentBorderClass(agent.color, agent.status)}`}
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-bold text-white">{agent.name}</h3>
                <p className="mt-1 text-xs text-slate-400">{agent.role}</p>
              </div>

              <StatusBadge status={agent.status} />
            </div>

            <div className="mt-4 grid grid-cols-2 gap-3">
              <Metric label="Score" value={agent.score ? String(agent.score) : "--"} />
              <Metric label="Confidence" value={agent.confidence ? `${agent.confidence}%` : "--"} />
            </div>

            <p className="mt-4 text-xs leading-relaxed text-slate-300">
              {agent.reasoning}
            </p>
          </motion.article>
        ))}
      </div>
    </Panel>
  );
}

function FinalDecision({ visible, isRunning,simulationResult, }: { visible: boolean; isRunning: boolean; simulationResult: ApiSimulationResponse | null; }) {
  if (!visible) {
    return (
      <section className="flex min-h-[330px] items-center justify-center rounded-2xl border border-cyan-400/20 bg-slate-950/80 p-5 text-center shadow-[0_0_30px_rgba(34,211,238,0.12)]">
        <div>
          {isRunning ? (
            <Loader2 className="mx-auto h-10 w-10 animate-spin text-cyan-300" />
          ) : (
            <Zap className="mx-auto h-10 w-10 text-cyan-300" />
          )}
          <p className="mt-4 font-mono text-sm text-cyan-300">
            {isRunning ? "Decision engine calculating..." : "Run simulation to generate final decision."}
          </p>
        </div>
      </section>
    );
  }
  const decision = simulationResult?.final_decision ?? "REVISE";
  const finalScore = simulationResult?.final_score ?? 68.75;
  return (
    <motion.section
      initial={{ opacity: 0, scale: 0.94 }}
      animate={{ opacity: 1, scale: 1 }}
      className="rounded-2xl border border-amber-400/40 bg-amber-400/10 p-5 shadow-[0_0_45px_rgba(251,191,36,0.16)]"
    >
      <p className="font-mono text-xs uppercase tracking-[0.35em] text-amber-300">
        Final Decision
      </p>

      <h2 className="mt-3 text-6xl font-black text-amber-300 drop-shadow-[0_0_20px_rgba(251,191,36,0.45)]">
        {decision}
      </h2>

      <div className="mt-5 grid grid-cols-2 gap-3">
       <Metric label="Overall Score" value={`${finalScore} / 100`} />
        <Metric label="Confidence" value="82%" />
        <Metric label="Scenario Type" value="TEAM EXPANSION" />
        <Metric label="Bottleneck" value="Workforce Capacity" />
      </div>

      <div className="mt-5 rounded-xl border border-amber-400/20 bg-black/40 p-4">
        <p className="font-mono text-[10px] uppercase tracking-widest text-amber-300">
          Recommendation
        </p>
        <p className="mt-2 text-sm leading-relaxed text-white">
          Increase team readiness or hiring capacity before approval.
        </p>
      </div>
    </motion.section>
  );
}
function Panel({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-cyan-400/20 bg-slate-950/80 p-5 shadow-[0_0_30px_rgba(34,211,238,0.12)] backdrop-blur-xl">
      <div className="mb-4">
        <h2 className="text-sm font-bold text-cyan-300 drop-shadow-[0_0_10px_rgba(34,211,238,0.7)]">
          {title}
        </h2>
        {subtitle && <p className="mt-1 font-mono text-xs text-slate-500">{subtitle}</p>}
      </div>
      {children}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-black/40 p-3">
      <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
        {label}
      </p>
      <p className="mt-1 text-sm font-bold text-white">{value}</p>
    </div>
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
    <div className={`absolute z-10 ${className}`}>
      <motion.div
        animate={
          status === "ANALYZING"
            ? { scale: [1, 1.12, 1], opacity: [0.85, 1, 0.85] }
            : { scale: 1, opacity: status === "IDLE" ? 0.55 : 1 }
        }
        transition={{
          repeat: status === "ANALYZING" ? Infinity : 0,
          duration: 1.2,
        }}
        className={`rounded-full border bg-black px-4 py-2 font-mono text-[10px] font-bold shadow-lg ${nodeColorClass(
          color,
          status
        )}`}
      >
        {label}
      </motion.div>
    </div>
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

  if (status === "WARNING") {
    return "border-amber-400 text-amber-300 shadow-amber-400/40";
  }

  if (color === "emerald") return "border-emerald-400 text-emerald-300 shadow-emerald-400/30";
  if (color === "amber") return "border-amber-400 text-amber-300 shadow-amber-400/30";
  if (color === "purple") return "border-purple-400 text-purple-300 shadow-purple-400/30";
  return "border-cyan-400 text-cyan-300 shadow-cyan-400/30";
}

function debateBorderClass(color: AgentColor) {
  if (color === "amber") return "border-amber-400/30";
  if (color === "emerald") return "border-emerald-400/30";
  if (color === "purple") return "border-purple-400/30";
  return "border-cyan-400/30";
}

function debateDotClass(color: AgentColor) {
  if (color === "amber") {
    return "bg-amber-300 shadow-[0_0_12px_rgba(251,191,36,0.9)]";
  }

  if (color === "emerald") {
    return "bg-emerald-300 shadow-[0_0_12px_rgba(52,211,153,0.9)]";
  }

  if (color === "purple") {
    return "bg-purple-300 shadow-[0_0_12px_rgba(168,85,247,0.9)]";
  }

  return "bg-cyan-300 shadow-[0_0_12px_rgba(34,211,238,0.9)]";
}

function debateStanceClass(stance: string)
 {
  if (stance === "Support") {
    return "border-emerald-400/40 bg-emerald-400/10 text-emerald-300";
  }

  if (stance === "Warning") {
    return "border-amber-400/40 bg-amber-400/10 text-amber-300";
  }

  if (stance === "Consensus") {
    return "border-purple-400/40 bg-purple-400/10 text-purple-300";
  }

  return "border-cyan-400/40 bg-cyan-400/10 text-cyan-300";
}
  function AgentDebateConsole({
  messages,
  isRunning,
  simulationResult,
}: {
  messages: DebateMessage[];
  isRunning: boolean;
  simulationResult: ApiSimulationResponse | null;
}) {
  const backendRounds = simulationResult?.rounds ?? [];
  const hasBackendRounds = backendRounds.length > 0;

  const mockRounds = Array.from(
    new Set(messages.map((message) => message.round))
  );

  const getMessageColor = (agent: string): AgentColor => {
    const normalized = agent.toLowerCase();

    if (normalized.includes("cfo")) return "emerald";
    if (normalized.includes("hr")) return "amber";
    if (normalized.includes("aggregator")) return "purple";

    return "cyan";
  };

  const normalizeStance = (
    stance?: string
  ): "Support" | "Warning" | "Revise" | "Consensus" => {
    const normalized = stance?.toLowerCase() ?? "";

    if (normalized.includes("support")) return "Support";
    if (normalized.includes("warning")) return "Warning";
    if (normalized.includes("consensus")) return "Consensus";

    return "Revise";
  };

  return (
    <Panel
      title="Agent Debate Console"
      subtitle="Cross-agent reasoning and boardroom-style deliberation"
    >
      <div className="grid gap-5 xl:grid-cols-[1fr_360px]">
        <div className="space-y-5">
          {!hasBackendRounds && messages.length === 0 && (
            <div className="rounded-2xl border border-cyan-400/10 bg-black/40 p-5 text-center">
              <p className="font-mono text-xs text-cyan-300">
                {isRunning
                  ? "Agent debate is initializing..."
                  : "Run simulation to start cross-agent debate."}
              </p>
            </div>
          )}

          {hasBackendRounds &&
            backendRounds.map((round) => (
              <div
                key={round.round_number}
                className="rounded-2xl border border-cyan-400/10 bg-black/40 p-5"
              >
                <div className="mb-4 flex items-center justify-between">
                  <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
                    ROUND {round.round_number}
                  </p>

                  <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-2 py-1 font-mono text-[10px] text-cyan-300">
                    BACKEND ROUND
                  </span>
                </div>

                <div className="space-y-3">
                  {round.messages.map((message, index) => {
                    const color = getMessageColor(message.agent);
                    const stance = normalizeStance(message.stance);

                    return (
                      <motion.div
                        key={`${round.round_number}-${message.agent}-${index}`}
                        initial={{ opacity: 0, x: -14 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.08 }}
                        className={`rounded-xl border bg-black/50 p-4 ${debateBorderClass(
                          color
                        )}`}
                      >
                        <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <span
                                className={`h-2 w-2 rounded-full ${debateDotClass(
                                  color
                                )}`}
                              />

                              <h3 className="text-sm font-bold text-white">
                                {message.agent}
                              </h3>
                            </div>

                            <p className="mt-2 text-xs leading-relaxed text-slate-300">
                              {message.reasoning ??
                                "No reasoning returned by backend."}
                            </p>

                            <div className="mt-3 flex flex-wrap gap-2 font-mono text-[10px]">
                              <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 text-slate-300">
                                Round {message.round_number ?? round.round_number}
                              </span>

                              <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 text-slate-300">
                                Confidence {message.confidence ?? "--"}%
                              </span>
                            </div>
                          </div>

                          <span
                            className={`shrink-0 rounded-full border px-2 py-1 font-mono text-[10px] ${debateStanceClass(
                              stance
                            )}`}
                          >
                            {message.stance ?? stance}
                          </span>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            ))}

          {!hasBackendRounds &&
            mockRounds.map((round) => (
              <div
                key={round}
                className="rounded-2xl border border-cyan-400/10 bg-black/40 p-5"
              >
                <div className="mb-4 flex items-center justify-between">
                  <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
                    {round}
                  </p>

                  <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-2 py-1 font-mono text-[10px] text-cyan-300">
                    MOCK THREAD
                  </span>
                </div>

                <div className="space-y-3">
                  {messages
                    .filter((message) => message.round === round)
                    .map((message, index) => (
                      <motion.div
                        key={`${message.round}-${message.agent}-${index}`}
                        initial={{ opacity: 0, x: -14 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.08 }}
                        className={`rounded-xl border bg-black/50 p-4 ${debateBorderClass(
                          message.color
                        )}`}
                      >
                        <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <span
                                className={`h-2 w-2 rounded-full ${debateDotClass(
                                  message.color
                                )}`}
                              />

                              <h3 className="text-sm font-bold text-white">
                                {message.agent}
                              </h3>
                            </div>

                            <p className="mt-2 text-xs leading-relaxed text-slate-300">
                              {message.message}
                            </p>
                          </div>

                          <span
                            className={`shrink-0 rounded-full border px-2 py-1 font-mono text-[10px] ${debateStanceClass(
                              message.stance
                            )}`}
                          >
                            {message.stance}
                          </span>
                        </div>
                      </motion.div>
                    ))}
                </div>
              </div>
            ))}
        </div>

        <div className="rounded-2xl border border-purple-400/20 bg-purple-400/10 p-5 shadow-[0_0_35px_rgba(168,85,247,0.12)]">
          <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-purple-300">
            Debate Summary
          </p>

          <h3 className="mt-3 text-2xl font-black text-white">
            Multi-Agent Consensus
          </h3>

          <p className="mt-3 text-sm leading-relaxed text-slate-300">
            CEO, CFO and HR agent messages are displayed by round. When backend
            round data exists, the console switches from frontend mock debate to
            backend-driven debate output.
          </p>

          <div className="mt-5 space-y-3">
            <Metric
              label="Consensus Reached"
              value={simulationResult?.consensus_reached ? "Yes" : "Pending"}
            />
            <Metric
              label="Stability Reached"
              value={simulationResult?.stability_reached ? "Yes" : "Pending"}
            />
            <Metric
              label="Backend Rounds"
              value={String(simulationResult?.rounds?.length ?? 0)}
            />
            <Metric
              label="Boardroom Mode"
              value={hasBackendRounds ? "Backend" : "Frontend Mock"}
            />
          </div>
        </div>
      </div>
    </Panel>
  );
}


function ScenarioComparisonBoard() {
  const scenarios = [
    {
      name: "Current Plan",
      decision: "REVISE",
      score: 68.75,
      risk: "Medium",
      bottleneck: "Workforce Capacity",
      recommendation: "Improve team readiness before approval.",
      tone: "amber",
    },
    {
      name: "Improved Team Plan",
      decision: "APPROVE",
      score: 76.25,
      risk: "Controlled",
      bottleneck: "None critical",
      recommendation: "Proceed with controlled execution.",
      tone: "emerald",
    },
    {
      name: "High Risk Pivot",
      decision: "REJECT",
      score: 44.2,
      risk: "High",
      bottleneck: "Risk Exposure",
      recommendation: "Reduce risk before reconsideration.",
      tone: "red",
    },
  ];

  return (
    <Panel
      title="Scenario Comparison Board"
      subtitle="Compare alternative decision paths before executive approval"
    >
      <div className="grid gap-4 lg:grid-cols-3">
        {scenarios.map((scenario, index) => (
          <motion.div
            key={scenario.name}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06 }}
            className={`rounded-2xl border bg-black/40 p-5 ${scenarioCardClass(
              scenario.tone
            )}`}
          >
            <div className="mb-4 flex items-start justify-between gap-3">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-slate-500">
                  Scenario Variant
                </p>
                <h3 className="mt-1 text-lg font-black text-white">
                  {scenario.name}
                </h3>
              </div>

              <span
                className={`rounded-full border px-2 py-1 font-mono text-[10px] ${scenarioBadgeClass(
                  scenario.tone
                )}`}
              >
                {scenario.decision}
              </span>
            </div>

            <div className="mb-4">
              <div className="flex items-end justify-between">
                <span className="text-4xl font-black text-white">
                  {scenario.score}
                </span>
                <span className="font-mono text-[10px] text-slate-500">
                  /100
                </span>
              </div>

              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className={`h-full rounded-full ${scenarioBarClass(
                    scenario.tone
                  )}`}
                  style={{ width: `${scenario.score}%` }}
                />
              </div>
            </div>

            <div className="grid gap-3">
              <Metric label="Risk" value={scenario.risk} />
              <Metric label="Bottleneck" value={scenario.bottleneck} />
            </div>

            <div className="mt-4 rounded-xl border border-white/10 bg-white/5 p-3">
              <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
                Recommendation
              </p>
              <p className="mt-2 text-xs leading-relaxed text-slate-300">
                {scenario.recommendation}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </Panel>
  );
}
function ExecutionActionPlan() {
  const actions = [
    {
      phase: "01",
      title: "Workforce Readiness Sprint",
      owner: "HR Agent",
      priority: "CRITICAL",
      duration: "2-4 weeks",
      tone: "amber",
      description:
        "Increase team readiness from 3/10 to at least 6/10 with hiring, onboarding and internal capability mapping.",
    },
    {
      phase: "02",
      title: "Budget Guardrail Review",
      owner: "CFO Agent",
      priority: "HIGH",
      duration: "1 week",
      tone: "emerald",
      description:
        "Validate whether additional hiring and onboarding costs keep the expected ROI financially acceptable.",
    },
    {
      phase: "03",
      title: "Strategic Approval Gate",
      owner: "CEO Agent",
      priority: "HIGH",
      duration: "Decision meeting",
      tone: "cyan",
      description:
        "Re-check strategic fit after HR and CFO constraints are updated, then decide whether the scenario can move to approval.",
    },
    {
      phase: "04",
      title: "Re-run Decision Simulation",
      owner: "Decision Aggregator",
      priority: "FINAL",
      duration: "After updates",
      tone: "purple",
      description:
        "Run the decision engine again with improved readiness values and compare the result against the current REVISE outcome.",
    },
  ];

  return (
    <Panel
      title="Execution Action Plan"
      subtitle="Recommended steps to move the scenario from REVISE toward APPROVE"
    >
      <div className="grid gap-4 xl:grid-cols-4">
        {actions.map((action, index) => (
          <motion.div
            key={action.title}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06 }}
            className={`rounded-2xl border bg-black/40 p-5 ${actionCardClass(
              action.tone
            )}`}
          >
            <div className="mb-4 flex items-center justify-between">
              <span className="font-mono text-[10px] text-slate-500">
                PHASE {action.phase}
              </span>

              <span
                className={`rounded-full border px-2 py-1 font-mono text-[10px] ${actionBadgeClass(
                  action.tone
                )}`}
              >
                {action.priority}
              </span>
            </div>

            <h3 className="text-base font-black text-white">{action.title}</h3>

            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              {action.description}
            </p>

            <div className="mt-5 grid gap-3">
              <Metric label="Owner" value={action.owner} />
              <Metric label="Duration" value={action.duration} />
            </div>
          </motion.div>
        ))}
      </div>
    </Panel>
  );
}
function WhatIfLab() {
  const [budget, setBudget] = useState(25);
  const [roi, setRoi] = useState(45);
  const [risk, setRisk] = useState(5);
  const [teamReadiness, setTeamReadiness] = useState(3);
  const [marketConfidence, setMarketConfidence] = useState(7);

  const ceoScore = clamp(
    35 + roi * 0.65 + marketConfidence * 3 - risk * 2
  );

  const cfoScore = clamp(
    55 + roi * 0.55 - budget * 0.7 - risk * 2.5
  );

  const hrScore = clamp(
    20 + teamReadiness * 9 - risk * 1.5
  );

  const finalScore = Number(
    (ceoScore * 0.25 + cfoScore * 0.25 + hrScore * 0.5).toFixed(2)
  );

  const decision =
    finalScore >= 70 ? "APPROVE" : finalScore >= 50 ? "REVISE" : "REJECT";

  const bottleneck =
    hrScore < ceoScore && hrScore < cfoScore
      ? "Workforce Capacity"
      : cfoScore < ceoScore
      ? "Financial Feasibility"
      : "Strategic Alignment";

  const decisionClass =
    decision === "APPROVE"
      ? "text-emerald-300 border-emerald-400/40 bg-emerald-400/10 shadow-[0_0_35px_rgba(52,211,153,0.16)]"
      : decision === "REVISE"
      ? "text-amber-300 border-amber-400/40 bg-amber-400/10 shadow-[0_0_35px_rgba(251,191,36,0.16)]"
      : "text-red-300 border-red-400/40 bg-red-400/10 shadow-[0_0_35px_rgba(248,113,113,0.16)]";

  return (
    <Panel
      title="What-if Simulation Lab"
      subtitle="Change scenario parameters and watch the decision engine react"
    >
      <div className="grid gap-5 xl:grid-cols-[1fr_420px]">
        <div className="grid gap-4 md:grid-cols-2">
          <SliderControl
            label="Budget"
            value={budget}
            min={1}
            max={60}
            suffix="M$"
            onChange={setBudget}
          />

          <SliderControl
            label="Expected ROI"
            value={roi}
            min={0}
            max={80}
            suffix="%"
            onChange={setRoi}
          />

          <SliderControl
            label="Risk Level"
            value={risk}
            min={1}
            max={10}
            suffix="/10"
            onChange={setRisk}
          />

          <SliderControl
            label="Team Readiness"
            value={teamReadiness}
            min={1}
            max={10}
            suffix="/10"
            onChange={setTeamReadiness}
          />

          <SliderControl
            label="Market Confidence"
            value={marketConfidence}
            min={1}
            max={10}
            suffix="/10"
            onChange={setMarketConfidence}
          />
        </div>

        <motion.div
          key={decision + finalScore}
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          className={`rounded-2xl border p-5 ${decisionClass}`}
        >
          <p className="font-mono text-xs uppercase tracking-[0.3em]">
            Simulated Decision
          </p>

          <h3 className="mt-3 text-5xl font-black">{decision}</h3>

          <div className="mt-5 grid grid-cols-2 gap-3">
            <Metric label="Final Score" value={`${finalScore} / 100`} />
            <Metric label="Bottleneck" value={bottleneck} />
            <Metric label="CEO Score" value={String(ceoScore)} />
            <Metric label="CFO Score" value={String(cfoScore)} />
            <Metric label="HR Score" value={String(hrScore)} />
            <Metric label="Scenario Type" value="TEAM EXPANSION" />
          </div>

          <div className="mt-5 rounded-xl border border-white/10 bg-black/40 p-4">
            <p className="font-mono text-[10px] uppercase tracking-widest">
              Recommendation
            </p>
            <p className="mt-2 text-sm leading-relaxed text-white">
              {decision === "APPROVE"
                ? "Scenario is viable. Proceed with controlled execution."
                : decision === "REVISE"
                ? "Improve the weakest parameter before approval. Team readiness is especially important in this scenario."
                : "Scenario is not viable under current constraints. Reduce risk or improve financial and workforce capacity."}
            </p>
          </div>
        </motion.div>
      </div>
    </Panel>
  );
}

function SliderControl({
  label,
  value,
  min,
  max,
  suffix,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  suffix: string;
  onChange: (value: number) => void;
}) {
  return (
    <div className="rounded-xl border border-cyan-400/10 bg-black/40 p-4">
      <div className="mb-3 flex items-center justify-between">
        <p className="font-mono text-xs uppercase tracking-widest text-slate-400">
          {label}
        </p>
        <p className="font-mono text-sm font-bold text-cyan-300">
          {value}
          {suffix}
        </p>
      </div>

      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="h-2 w-full cursor-pointer accent-cyan-300"
      />

      <div className="mt-2 flex justify-between font-mono text-[10px] text-slate-600">
        <span>
          {min}
          {suffix}
        </span>
        <span>
          {max}
          {suffix}
        </span>
      </div>
    </div>
  );
}
function timelineStatusClass(status: AgentStatus) {
  if (status === "COMPLETED") {
    return "border-emerald-400/30 shadow-[0_0_18px_rgba(52,211,153,0.10)]";
  }

  if (status === "ANALYZING") {
    return "border-cyan-400/40 shadow-[0_0_20px_rgba(34,211,238,0.16)]";
  }

  if (status === "WARNING") {
    return "border-amber-400/40 shadow-[0_0_20px_rgba(251,191,36,0.14)]";
  }

  return "border-slate-700/70";
}

function timelineDotClass(status: AgentStatus) {
  if (status === "COMPLETED") {
    return "bg-emerald-300 shadow-[0_0_12px_rgba(52,211,153,0.9)]";
  }

  if (status === "ANALYZING") {
    return "bg-cyan-300 shadow-[0_0_12px_rgba(34,211,238,0.9)] animate-pulse";
  }

  if (status === "WARNING") {
    return "bg-amber-300 shadow-[0_0_12px_rgba(251,191,36,0.9)]";
  }

  return "bg-slate-600";
}

function timelineTextClass(status: AgentStatus) {
  if (status === "COMPLETED") return "text-emerald-300";
  if (status === "ANALYZING") return "text-cyan-300";
  if (status === "WARNING") return "text-amber-300";
  return "text-slate-500";
}
function signalCardClass(tone: string) {
  if (tone === "emerald") {
    return "border-emerald-400/30 shadow-[0_0_22px_rgba(52,211,153,0.10)]";
  }

  if (tone === "amber") {
    return "border-amber-400/40 shadow-[0_0_22px_rgba(251,191,36,0.14)]";
  }

  if (tone === "purple") {
    return "border-purple-400/30 shadow-[0_0_22px_rgba(168,85,247,0.10)]";
  }

  return "border-cyan-400/30 shadow-[0_0_22px_rgba(34,211,238,0.10)]";
}

function signalBadgeClass(tone: string) {
  if (tone === "emerald") {
    return "border-emerald-400/40 bg-emerald-400/10 text-emerald-300";
  }

  if (tone === "amber") {
    return "border-amber-400/40 bg-amber-400/10 text-amber-300";
  }

  if (tone === "purple") {
    return "border-purple-400/40 bg-purple-400/10 text-purple-300";
  }

  return "border-cyan-400/40 bg-cyan-400/10 text-cyan-300";
}

function signalBarClass(tone: string) {
  if (tone === "emerald") return "bg-emerald-300 shadow-[0_0_14px_rgba(52,211,153,0.9)]";
  if (tone === "amber") return "bg-amber-300 shadow-[0_0_14px_rgba(251,191,36,0.9)]";
  if (tone === "purple") return "bg-purple-300 shadow-[0_0_14px_rgba(168,85,247,0.9)]";
  return "bg-cyan-300 shadow-[0_0_14px_rgba(34,211,238,0.9)]";
}
function kpiCardClass(tone: string) {
  if (tone === "amber") {
    return "border-amber-400/40 shadow-[0_0_25px_rgba(251,191,36,0.12)]";
  }

  if (tone === "emerald") {
    return "border-emerald-400/30 shadow-[0_0_25px_rgba(52,211,153,0.10)]";
  }

  if (tone === "cyan") {
    return "border-cyan-400/30 shadow-[0_0_25px_rgba(34,211,238,0.10)]";
  }

  return "border-slate-700/70";
}

function kpiValueClass(tone: string) {
  if (tone === "amber") return "text-amber-300";
  if (tone === "emerald") return "text-emerald-300";
  if (tone === "cyan") return "text-cyan-300";
  return "text-slate-300";
}

function kpiDotClass(tone: string) {
  if (tone === "amber") {
    return "bg-amber-300 shadow-[0_0_12px_rgba(251,191,36,0.9)]";
  }

  if (tone === "emerald") {
    return "bg-emerald-300 shadow-[0_0_12px_rgba(52,211,153,0.9)]";
  }

  if (tone === "cyan") {
    return "bg-cyan-300 shadow-[0_0_12px_rgba(34,211,238,0.9)]";
  }

  return "bg-slate-600";
}
function getAgentIdFromName(name: string) {
  const normalized = name.toLowerCase();

  if (normalized.includes("ceo")) return "ceo";
  if (normalized.includes("cfo")) return "cfo";
  if (normalized.includes("hr")) return "hr";

  return normalized.replace(/\s+/g, "-");
}

function getAgentColorFromId(id: string): AgentColor {
  if (id === "cfo") return "emerald";
  if (id === "hr") return "amber";
  return "cyan";
}

function getAgentRoleFromId(id: string) {
  if (id === "ceo") return "Strategic Vision Evaluator";
  if (id === "cfo") return "Financial Feasibility Evaluator";
  if (id === "hr") return "Workforce Capacity Evaluator";
  return "Decision Agent";
}

function mapApiAgentToCockpitAgent(output: ApiAgentOutput): Agent {
  const id = getAgentIdFromName(output.agent);
  const stance = output.stance?.toLowerCase() ?? "";

  return {
    id,
    name: output.agent,
    role: getAgentRoleFromId(id),
    status:
      stance.includes("revise") ||
      stance.includes("warning") ||
      output.score < 70
        ? "WARNING"
        : "COMPLETED",
    score: Math.round(output.score),
    confidence: output.confidence ?? 80,
    color: getAgentColorFromId(id),
    reasoning: output.reasoning ?? "Backend did not return reasoning.",
  };
}
function clamp(value: number) {
  return Math.max(0, Math.min(100, Math.round(value)));
}
function ExecutiveDecisionReport() {
  const [copied, setCopied] = useState(false);

  const copyReport = async () => {
    await navigator.clipboard.writeText(executiveReportText);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  const downloadReport = () => {
  const blob = new Blob([executiveReportText], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "ai-decision-executive-report.txt";
  link.click();
  URL.revokeObjectURL(url);
};
  

  return (
    <Panel
      title="Executive Decision Report"
      subtitle="AI-generated boardroom summary and explainable recommendation"
    >
<div className="mb-5 flex flex-col gap-3 rounded-2xl border border-cyan-400/10 bg-black/40 p-4 md:flex-row md:items-center md:justify-between">
  <div>
    <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
      Report Actions
    </p>
    <p className="mt-1 text-xs text-slate-400">
      Copy or download the AI-generated executive report.
    </p>
  </div>

  <div className="flex flex-wrap gap-2">
    <button
      onClick={copyReport}
      className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-3 py-2 font-mono text-xs text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
    >
      {copied ? <Check size={14} /> : <Copy size={14} />}
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
      <div className="grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-5">
          <div className="rounded-2xl border border-cyan-400/10 bg-black/40 p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
                  Scenario Summary
                </p>
                <h3 className="mt-2 text-xl font-black text-white">
                  AI Market Expansion Initiative
                </h3>
              </div>

              <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 font-mono text-[10px] text-amber-300">
                NEEDS REVISION
              </span>
            </div>

            <p className="text-sm leading-relaxed text-slate-300">
              The system analyzed a high-impact market expansion scenario using
              three executive AI agents. CEO and CFO perspectives are positive,
              but the HR Agent detected a workforce capacity limitation. Because
              this scenario is classified as <strong>TEAM_EXPANSION</strong>, HR
              receives the highest decision weight.
            </p>

            <div className="mt-5 grid gap-3 md:grid-cols-4">
              <Metric label="Budget" value="$25M" />
              <Metric label="Expected ROI" value="45%" />
              <Metric label="Risk Level" value="5/10" />
              <Metric label="Team Readiness" value="3/10" />
            </div>
          </div>

          <div className="rounded-2xl border border-cyan-400/10 bg-black/40 p-5">
            <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
              Agent Findings
            </p>

            <div className="space-y-3">
              {reportAgentFindings.map((item) => (
                <div
                  key={item.agent}
                  className={`rounded-xl border bg-black/40 p-4 ${
                    item.color === "amber"
                      ? "border-amber-400/30"
                      : item.color === "emerald"
                      ? "border-emerald-400/30"
                      : "border-cyan-400/30"
                  }`}
                >
                  <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                      <h4 className="font-bold text-white">{item.agent}</h4>
                      <p className="mt-1 text-xs leading-relaxed text-slate-400">
                        {item.finding}
                      </p>
                    </div>

                    <div className="flex shrink-0 gap-2">
                      <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 font-mono text-[10px] text-white">
                        Score {item.score}
                      </span>
                      <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 font-mono text-[10px] text-white">
                        Weight {item.weight}
                      </span>
                      <span
                        className={`rounded-full border px-2 py-1 font-mono text-[10px] ${
                          item.stance === "Revise"
                            ? "border-amber-400/40 bg-amber-400/10 text-amber-300"
                            : "border-emerald-400/40 bg-emerald-400/10 text-emerald-300"
                        }`}
                      >
                        {item.stance}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-5">
          <div className="rounded-2xl border border-amber-400/30 bg-amber-400/10 p-5 shadow-[0_0_35px_rgba(251,191,36,0.12)]">
            <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-amber-300">
              Final Score Calculation
            </p>

            <div className="mt-4 space-y-3 font-mono text-xs">
              <CalculationRow label="CEO" formula="85 × 0.25" result="21.25" />
              <CalculationRow label="CFO" formula="90 × 0.25" result="22.50" />
              <CalculationRow label="HR" formula="50 × 0.50" result="25.00" />

              <div className="mt-4 border-t border-amber-400/20 pt-4">
                <div className="flex items-center justify-between">
                  <span className="text-amber-300">Final Score</span>
                  <span className="text-xl font-black text-white">
                    68.75 / 100
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-5 rounded-xl border border-amber-400/20 bg-black/40 p-4">
              <p className="font-mono text-[10px] uppercase tracking-widest text-amber-300">
                Decision Rule
              </p>
              <p className="mt-2 text-xs leading-relaxed text-slate-300">
                70+ = APPROVE, 50–69 = REVISE, below 50 = REJECT. Since the
                final score is 68.75, the recommended decision is{" "}
                <strong className="text-amber-300">REVISE</strong>.
              </p>
            </div>
          </div>

          <div className="rounded-2xl border border-cyan-400/10 bg-black/40 p-5">
            <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-cyan-300">
              Recommended Next Steps
            </p>

            <div className="mt-4 space-y-3">
              {reportNextSteps.map((step, index) => (
                <div
                  key={step}
                  className="flex gap-3 rounded-xl border border-white/10 bg-white/5 p-3"
                >
                  <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-cyan-400/40 bg-cyan-400/10 font-mono text-[10px] text-cyan-300">
                    {index + 1}
                  </div>
                  <p className="text-xs leading-relaxed text-slate-300">
                    {step}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-5">
            <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-emerald-300">
              Improvement Target
            </p>

            <h3 className="mt-3 text-2xl font-black text-emerald-300">
              REVISE → APPROVE
            </h3>

            <p className="mt-3 text-xs leading-relaxed text-slate-300">
              If team readiness is improved from 3/10 to 6/10 while risk remains
              controlled, the HR bottleneck weakens and the scenario can move
              toward approval.
            </p>
          </div>
        </div>
      </div>
    </Panel>
  );

}
function SimulationHistory() {
  const historyItems = [
    {
      title: "AI Market Expansion Initiative",
      decision: "REVISE",
      score: "68.75",
      date: "Latest simulation",
      bottleneck: "Workforce Capacity",
    },
    {
      title: "Cost Optimization Program",
      decision: "APPROVE",
      score: "81.40",
      date: "Demo record",
      bottleneck: "Low risk",
    },
    {
      title: "Strategic Pivot Scenario",
      decision: "REJECT",
      score: "44.20",
      date: "Demo record",
      bottleneck: "High risk exposure",
    },
  ];

  return (
    <Panel
      title="Simulation History"
      subtitle="Previous decision runs and executive outcomes"
    >
      <div className="grid gap-4 lg:grid-cols-3">
        {historyItems.map((item) => (
          <div
            key={item.title}
            className="rounded-2xl border border-cyan-400/10 bg-black/40 p-4"
          >
            <div className="mb-4 flex items-start justify-between gap-3">
              <div>
                <h3 className="text-sm font-bold text-white">{item.title}</h3>
                <p className="mt-1 font-mono text-[10px] text-slate-500">
                  {item.date}
                </p>
              </div>

              <span
                className={`rounded-full border px-2 py-1 font-mono text-[10px] ${
                  item.decision === "APPROVE"
                    ? "border-emerald-400/40 bg-emerald-400/10 text-emerald-300"
                    : item.decision === "REVISE"
                      ? "border-amber-400/40 bg-amber-400/10 text-amber-300"
                      : "border-red-400/40 bg-red-400/10 text-red-300"
                }`}
              >
                {item.decision}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Metric label="Score" value={item.score} />
              <Metric label="Bottleneck" value={item.bottleneck} />
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
}
function SystemSettingsPanel() {
  const settings = [
    ["Simulation Mode", "Frontend Mock"],
    ["Agent Count", "CEO / CFO / HR"],
    ["Debate Mode", "Interactive"],
    ["Report Export", "TXT Enabled"],
    ["Backend Status", "Not connected yet"],
    ["UI Theme", "Decision OS Dark"],
  ];

  return (
    <Panel
      title="System Settings"
      subtitle="Frontend cockpit configuration and prototype status"
    >
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {settings.map(([label, value]) => (
          <div
            key={label}
            className="rounded-xl border border-cyan-400/10 bg-black/40 p-4"
          >
            <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
              {label}
            </p>
            <p className="mt-2 text-sm font-bold text-cyan-300">{value}</p>
          </div>
        ))}
      </div>

      <div className="mt-5 rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4">
        <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-amber-300">
          Prototype Note
        </p>
        <p className="mt-2 text-sm leading-relaxed text-slate-300">
          This cockpit currently uses frontend mock data. The next integration
          step is connecting scenario input, agent outputs, debate messages and
          executive reports to the FastAPI backend.
        </p>
      </div>
    </Panel>
  );
}
function CalculationRow({
  label,
  formula,
  result,
}: {
  label: string;
  formula: string;
  result: string;
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-white/10 bg-black/40 p-3">
      <span className="text-slate-400">{label}</span>
      <span className="text-cyan-300">{formula}</span>
      <span className="font-bold text-white">{result}</span>
    </div>
  );
}function scenarioCardClass(tone: string) {
  if (tone === "emerald") {
    return "border-emerald-400/30 shadow-[0_0_25px_rgba(52,211,153,0.10)]";
  }

  if (tone === "red") {
    return "border-red-400/30 shadow-[0_0_25px_rgba(248,113,113,0.10)]";
  }

  return "border-amber-400/40 shadow-[0_0_25px_rgba(251,191,36,0.12)]";
}

function scenarioBadgeClass(tone: string) {
  if (tone === "emerald") {
    return "border-emerald-400/40 bg-emerald-400/10 text-emerald-300";
  }

  if (tone === "red") {
    return "border-red-400/40 bg-red-400/10 text-red-300";
  }

  return "border-amber-400/40 bg-amber-400/10 text-amber-300";
}

function scenarioBarClass(tone: string) {
  if (tone === "emerald") {
    return "bg-emerald-300 shadow-[0_0_14px_rgba(52,211,153,0.9)]";
  }

  if (tone === "red") {
    return "bg-red-300 shadow-[0_0_14px_rgba(248,113,113,0.9)]";
  }

  return "bg-amber-300 shadow-[0_0_14px_rgba(251,191,36,0.9)]";
}
function actionCardClass(tone: string) {
  if (tone === "emerald") {
    return "border-emerald-400/30 shadow-[0_0_25px_rgba(52,211,153,0.10)]";
  }

  if (tone === "cyan") {
    return "border-cyan-400/30 shadow-[0_0_25px_rgba(34,211,238,0.10)]";
  }

  if (tone === "purple") {
    return "border-purple-400/30 shadow-[0_0_25px_rgba(168,85,247,0.10)]";
  }

  return "border-amber-400/40 shadow-[0_0_25px_rgba(251,191,36,0.12)]";
}

function actionBadgeClass(tone: string) {
  if (tone === "emerald") {
    return "border-emerald-400/40 bg-emerald-400/10 text-emerald-300";
  }

  if (tone === "cyan") {
    return "border-cyan-400/40 bg-cyan-400/10 text-cyan-300";
  }

  if (tone === "purple") {
    return "border-purple-400/40 bg-purple-400/10 text-purple-300";
  }

  return "border-amber-400/40 bg-amber-400/10 text-amber-300";
}
