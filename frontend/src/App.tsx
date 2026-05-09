import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { useState, type ReactNode } from "react";
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
} from "lucide-react";

type AgentStatus = "IDLE" | "ANALYZING" | "WARNING" | "COMPLETED";

type Agent = {
  id: string;
  name: string;
  role: string;
  status: AgentStatus;
  score: number;
  confidence: number;
  color: "cyan" | "emerald" | "amber" | "purple";
  reasoning: string;
};

const initialAgents: Agent[] = [
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

const completedAgents: Agent[] = [
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
    reasoning: "Financial feasibility is positive with acceptable budget exposure.",
  },
  {
    id: "hr",
    name: "HR Agent",
    role: "Workforce Capacity Evaluator",
    status: "WARNING",
    score: 50,
    confidence: 79,
    color: "amber",
    reasoning: "Team readiness is below the recommended execution threshold.",
  },
];

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export default function App() {
  const [agents, setAgents] = useState<Agent[]>(initialAgents);
  const [logs, setLogs] = useState<string[]>([
    "System ready. Awaiting simulation start...",
  ]);
  const [isRunning, setIsRunning] = useState(false);
  const [classifierStatus, setClassifierStatus] = useState<AgentStatus>("IDLE");
  const [aggregatorStatus, setAggregatorStatus] = useState<AgentStatus>("IDLE");
  const [explainStatus, setExplainStatus] = useState<AgentStatus>("IDLE");
  const [finalVisible, setFinalVisible] = useState(false);

  const addLog = async (message: string, delay = 450) => {
    setLogs((prev) => [...prev, message]);
    await wait(delay);
  };

  const updateAgent = (id: string, patch: Partial<Agent>) => {
    setAgents((prev) =>
      prev.map((agent) => (agent.id === id ? { ...agent, ...patch } : agent))
    );
  };

  const runSimulation = async () => {
    if (isRunning) return;

    setIsRunning(true);
    setFinalVisible(false);
    setAgents(initialAgents);
    setClassifierStatus("IDLE");
    setAggregatorStatus("IDLE");
    setExplainStatus("IDLE");
    setLogs([]);

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

    updateAgent("cfo", {
      status: "ANALYZING",
      reasoning: "Evaluating budget exposure and expected return...",
    });
    await addLog("CFO Agent evaluating financial feasibility...");
    updateAgent("cfo", completedAgents[1]);
    await addLog("CFO Agent completed: Score 90 | Confidence 88%");

    updateAgent("hr", {
      status: "ANALYZING",
      reasoning: "Checking team readiness and hiring pressure...",
    });
    await addLog("HR Agent checking workforce capacity...");
    updateAgent("hr", completedAgents[2]);
    await addLog("HR Agent warning: Team readiness insufficient");

    setAggregatorStatus("ANALYZING");
    await addLog("Aggregator applying dynamic weights...");
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

    setFinalVisible(true);
    setIsRunning(false);
  };

  return (
  <main className="scanline cyber-grid min-h-screen bg-[#050816] text-white">
    <div className="flex min-h-screen">
      <Sidebar />

      <div className="flex-1">
        <div className="mx-auto max-w-[1600px] space-y-5 p-5">
          <TopBar isRunning={isRunning} />
        <section className="grid gap-5 xl:grid-cols-[320px_1fr_380px]">
          <ScenarioPanel isRunning={isRunning} onStart={runSimulation} />
          <DecisionCore
            agents={agents}
            classifierStatus={classifierStatus}
            aggregatorStatus={aggregatorStatus}
            explainStatus={explainStatus}
          />
          <LiveFeed logs={logs} />
        </section>

        <section className="grid gap-5 xl:grid-cols-[1fr_430px]">
          <AgentRegistry agents={agents} />
          <FinalDecision visible={finalVisible} isRunning={isRunning} />
        </section>


    <WhatIfLab />
<ExecutiveDecisionReport />

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
              className={`flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left font-mono text-xs transition ${
                item.active
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

function ScenarioPanel({
  isRunning,
  onStart,
}: {
  isRunning: boolean;
  onStart: () => void;
}) {
  const rows = [
    ["Project", "AI Market Expansion Initiative"],
    ["Budget", "$25M"],
    ["Expected ROI", "45%"],
    ["Risk Level", "5/10"],
    ["Team Readiness", "3/10"],
    ["Market Confidence", "7/10"],
    ["Strategic Fit", "8/10"],
    ["Scenario Type", "TEAM EXPANSION"],
  ];

  return (
    <Panel title="Scenario Input" subtitle="Executive decision parameters">
      <div className="space-y-3">
        {rows.map(([label, value]) => (
          <div key={label} className="rounded-xl border border-cyan-400/10 bg-black/40 p-3">
            <p className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
              {label}
            </p>
            <p className="mt-1 text-sm font-semibold text-white">{value}</p>
          </div>
        ))}

        <button
          onClick={onStart}
          disabled={isRunning}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-cyan-400/50 bg-cyan-400/15 px-4 py-3 font-mono text-xs font-bold uppercase text-cyan-300 shadow-[0_0_25px_rgba(34,211,238,0.18)] transition hover:bg-cyan-400 hover:text-slate-950 disabled:cursor-not-allowed disabled:opacity-60"
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
  classifierStatus,
  aggregatorStatus,
  explainStatus,
}: {
  agents: Agent[];
  classifierStatus: AgentStatus;
  aggregatorStatus: AgentStatus;
  explainStatus: AgentStatus;
}) {
  const getStatus = (id: string) => agents.find((agent) => agent.id === id)?.status ?? "IDLE";

  return (
    <Panel title="Decision Core Network" subtitle="Live multi-agent orchestration">
      <div className="relative flex min-h-[520px] items-center justify-center overflow-hidden rounded-2xl border border-cyan-400/10 bg-black/40">
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
            <p className="text-3xl font-black text-white drop-shadow-[0_0_14px_rgba(34,211,238,0.9)]">
              CORE
            </p>
          </div>

          <CoreNode label="CEO" className="-top-14 left-1/2 -translate-x-1/2" color="cyan" status={getStatus("ceo")} />
          <CoreNode label="CFO" className="right-[-92px] top-1/2 -translate-y-1/2" color="emerald" status={getStatus("cfo")} />
          <CoreNode label="HR" className="-bottom-14 left-1/2 -translate-x-1/2" color="amber" status={getStatus("hr")} />
          <CoreNode label="CLASSIFIER" className="left-[-132px] top-1/2 -translate-y-1/2" color="purple" status={classifierStatus} />
          <CoreNode label="AGGREGATOR" className="right-[-110px] bottom-2" color="cyan" status={aggregatorStatus} />
          <CoreNode label="EXPLAIN" className="left-[-96px] bottom-2" color="cyan" status={explainStatus} />
        </motion.div>
      </div>
    </Panel>
  );
}

function LiveFeed({ logs }: { logs: string[] }) {
  return (
    <Panel title="Live Analysis Feed" subtitle="Real-time agent execution stream">
      <div className="space-y-4">
        <div className="h-[340px] overflow-hidden rounded-xl border border-cyan-400/10 bg-black/70 p-4 font-mono text-xs">
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
                  log.toLowerCase().includes("warning") || log.includes("HR weight")
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
          </div>
        </div>

        <AgentContributionChart />
      </div>
    </Panel>
  );
}
const contributionData = [
  { name: "CEO", value: 25, color: "#22d3ee" },
  { name: "CFO", value: 25, color: "#34d399" },
  { name: "HR", value: 50, color: "#fbbf24" },
];

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

function FinalDecision({ visible, isRunning }: { visible: boolean; isRunning: boolean }) {
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
        REVISE
      </h2>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <Metric label="Overall Score" value="68.75 / 100" />
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
  color: "cyan" | "emerald" | "amber" | "purple";
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

function statusBadgeClass(status: AgentStatus) {
  if (status === "WARNING") return "border-amber-400 text-amber-300";
  if (status === "COMPLETED") return "border-emerald-400 text-emerald-300";
  if (status === "ANALYZING") return "border-cyan-400 text-cyan-300";
  return "border-slate-500 text-slate-400";
}

function agentBorderClass(color: Agent["color"], status: AgentStatus) {
  if (status === "IDLE") return "border-slate-700/80";
  if (color === "amber") return "border-amber-400/70 shadow-[0_0_25px_rgba(251,191,36,0.18)]";
  if (color === "emerald") return "border-emerald-400/60 shadow-[0_0_25px_rgba(52,211,153,0.18)]";
  if (color === "purple") return "border-purple-400/60 shadow-[0_0_25px_rgba(168,85,247,0.18)]";
  return "border-cyan-400/60 shadow-[0_0_25px_rgba(34,211,238,0.18)]";
}

function nodeColorClass(color: Agent["color"], status: AgentStatus) {
  if (status === "IDLE") return "border-slate-600 text-slate-400 shadow-slate-500/10";

  if (status === "WARNING") {
    return "border-amber-400 text-amber-300 shadow-amber-400/40";
  }

  if (color === "emerald") return "border-emerald-400 text-emerald-300 shadow-emerald-400/30";
  if (color === "amber") return "border-amber-400 text-amber-300 shadow-amber-400/30";
  if (color === "purple") return "border-purple-400 text-purple-300 shadow-purple-400/30";
  return "border-cyan-400 text-cyan-300 shadow-cyan-400/30";
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

function clamp(value: number) {
  return Math.max(0, Math.min(100, Math.round(value)));
}
function ExecutiveDecisionReport() {
  const agentFindings = [
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

  const nextSteps = [
    "Increase team readiness from 3/10 to at least 6/10.",
    "Create a hiring or onboarding plan before approval.",
    "Keep risk level below 6/10 during execution planning.",
    "Re-run the simulation after workforce capacity improvements.",
  ];

  return (
    <Panel
      title="Executive Decision Report"
      subtitle="AI-generated boardroom summary and explainable recommendation"
    >
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
              {agentFindings.map((item) => (
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
              {nextSteps.map((step, index) => (
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
}
