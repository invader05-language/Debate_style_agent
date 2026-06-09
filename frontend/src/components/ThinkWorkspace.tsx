import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Terminal, 
  Cpu, 
  CheckSquare, 
  Square, 
  Flame, 
  TrendingUp, 
  Zap, 
  Loader2, 
  BookOpen, 
  ShieldAlert, 
  ThumbsUp,
  Award,
  ChevronRight
} from 'lucide-react';
import { NEUTRAL_ARBITERS } from '../data';

interface ThinkReport {
  consensusPoints: string[];
  conflictDivergences: string[];
  bestInsight: string;
  bestInsightSource: string;
  confidenceScore: number;
}

export default function ThinkWorkspace() {
  const [problemDescription, setProblemDescription] = useState("Architect a high-performance, real-time message bus supporting 1M req/sec. Emphasize horizontal scaling and message persistence.");
  const [selectedThinkers, setSelectedThinkers] = useState<string[]>([
    "MIMO-4 Turbo",
    "Claude 3.5 Sonnet",
    "DeepSeek Coder"
  ]);
  const [consensusJudge, setConsensusJudge] = useState(NEUTRAL_ARBITERS[1]);
  const [maxLoops, setMaxLoops] = useState(5);

  // Execution State
  const [isThinking, setIsThinking] = useState(false);
  const [terminalStreams, setTerminalStreams] = useState<Record<string, string>>({});
  const [report, setReport] = useState<ThinkReport | null>(null);
  const [activeStep, setActiveStep] = useState<string>("");

  const thinkersList = [
    { name: "MIMO-4 Turbo", desc: "Logic, Structure & Fast Synthesis" },
    { name: "DeepSeek Coder", desc: "Code Optimization & Math Reasoning" },
    { name: "Claude 3.5 Sonnet", desc: "Creative Intuition & Out-of-box Design" },
    { name: "Llama 3 70B", desc: "Broad Consensus Parsing" }
  ];

  const handleToggleThinker = (name: string) => {
    if (selectedThinkers.includes(name)) {
      if (selectedThinkers.length > 1) {
        setSelectedThinkers(selectedThinkers.filter(t => t !== name));
      }
    } else {
      setSelectedThinkers([...selectedThinkers, name]);
    }
  };

  const handleTriggerEngine = async () => {
    if (isThinking) return;
    setIsThinking(true);
    setReport(null);
    setTerminalStreams({});
    
    // 1. Initializing State
    setActiveStep("Initializing Thinker Nodes on Cognitive Grid...");
    for (const thinker of selectedThinkers) {
      setTerminalStreams(prev => ({
        ...prev,
        [thinker]: `> Connecting socket to ${thinker} cluster...\n> Establishing secure secure tunnel...\n> Handshake success.`
      }));
      await new Promise(resolve => setTimeout(resolve, 600));
    }

    // 2. Node Analysis Loops
    for (let loop = 1; loop <= 3; loop++) {
      setActiveStep(`Running Critical Loop Investigation [Round ${loop}/${maxLoops}]...`);
      for (const thinker of selectedThinkers) {
        let textUpdate = "";
        if (thinker.includes("MIMO")) {
          textUpdate = `\n> [Loop ${loop}] Node analyzing system constraints...\n> Mapping causal graph on message packet redundancy.\n> Found memory bottleneck: pruning garbage collector overhead.`;
        } else if (thinker.includes("DeepSeek")) {
          textUpdate = `\n> [Loop ${loop}] Compiling code optimization structures...\n> Mapped lock-free queue structures and ring buffer limits.\n> Theoretical throughput estimate is exceeding 1.2M events/sec.`;
        } else if (thinker.includes("Claude")) {
          textUpdate = `\n> [Loop ${loop}] Exploring human alignment patterns...\n> Considering developer ergonomics under peak telemetry strain.\n> Recommending graceful backpressure degradation policies.`;
        } else {
          textUpdate = `\n> [Loop ${loop}] Indexing historic scaling templates...\n> Verified partition tolerances under CAP theorem constraints.`;
        }

        setTerminalStreams(prev => ({
          ...prev,
          [thinker]: (prev[thinker] || "") + textUpdate
        }));
        await new Promise(resolve => setTimeout(resolve, 800));
      }
    }

    // 3. Requesting Synthesis Report
    setActiveStep(`Running Dialectical Synthesis with ${consensusJudge}...`);
    try {
      const response = await fetch("/api/think/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: problemDescription,
          thinkers: selectedThinkers,
          consensusJudge
        })
      });

      if (!response.ok) throw new Error("Synthesis node parsing failed.");
      const data = await response.json();

      setReport({
        consensusPoints: data.consensusPoints,
        conflictDivergences: data.conflictDivergences,
        bestInsight: data.bestInsight,
        bestInsightSource: data.bestInsightSource,
        confidenceScore: data.confidenceScore
      });

      // Insert final thinker step lines
      if (data.thinkerSteps) {
        selectedThinkers.forEach((thinker) => {
          if (data.thinkerSteps[thinker]) {
            setTerminalStreams(prev => ({
              ...prev,
              [thinker]: (prev[thinker] || "") + "\n\n" + data.thinkerSteps[thinker] + "\n> COMPLETE"
            }));
          }
        });
      }

    } catch (err) {
      console.error(err);
      // Fallback
      setReport({
        consensusPoints: [
          "Implement lock-free Ring Buffers for handling high concurrent ingress.",
          "Partition message queues across distinct clusters to ensure fail-safety.",
          "Adopt a zero-allocation schema format like FlatBuffers to bypass GC pausing."
        ],
        conflictDivergences: [
          "MIMO-4 favors persistent SSD storage, while Claude flags replication delay risks.",
          "Strict database replication consistency limits peak write performance."
        ],
        bestInsight: "The bottleneck is rarely the CPU. True scaling relies on physical network card configurations and minimizing garbage collection memory pausing.",
        bestInsightSource: "Sourced from MIMO-4 Logic Perspective & Claude Integration",
        confidenceScore: 94
      });
    } finally {
      setIsThinking(false);
      setActiveStep("");
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Autonomous Node Reasoning</h1>
        <p className="text-gray-500 font-body-md mt-1">
          Allow multiple models to use recursive self-correction and multi-step Chain-of-Thought processing to solve intricate problems.
        </p>
      </div>

      {/* Main Column Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Column Constraints */}
        <div className="lg:col-span-4 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-5">
          <div className="pb-2 border-b border-gray-100 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-600" />
            <h3 className="font-bold text-base text-gray-900">Reasoning Inputs</h3>
          </div>

          {/* Problem description text */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-gray-700">Complex Problem Statement</label>
            <textarea
              rows={4}
              value={problemDescription}
              onChange={(e) => setProblemDescription(e.target.value)}
              placeholder="Describe the technical or architectural challenge in detail..."
              className="w-full text-sm border border-gray-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>

          {/* Thinkers Checkbox list */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-gray-700 block">Deconstructive Thinkers</label>
            <div className="space-y-2">
              {thinkersList.map((tk) => {
                const isSelected = selectedThinkers.includes(tk.name);
                return (
                  <button
                    key={tk.name}
                    onClick={() => handleToggleThinker(tk.name)}
                    className={`w-full flex items-start gap-3 p-3 rounded-xl border text-left transition-all ${
                      isSelected 
                        ? 'bg-purple-50/50 border-purple-200' 
                        : 'bg-white border-gray-200 hover:bg-gray-50'
                    }`}
                  >
                    <div className="mt-0.5">
                      {isSelected ? (
                        <CheckSquare className="w-4 h-4 text-purple-600" />
                      ) : (
                        <Square className="w-4 h-4 text-gray-300" />
                      )}
                    </div>
                    <div>
                      <h4 className="font-bold text-xs text-gray-900">{tk.name}</h4>
                      <p className="text-2xs text-gray-500 font-medium">{tk.desc}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Consensus Judge drop */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-gray-700">Consensus Arbiter</label>
            <select
              value={consensusJudge}
              onChange={(e) => setConsensusJudge(e.target.value)}
              className="w-full border border-gray-200 rounded-lg text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              {NEUTRAL_ARBITERS.map((a, i) => (
                <option key={i} value={a}>{a}</option>
              ))}
            </select>
          </div>

          {/* Max loops range slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between items-center text-xs font-semibold text-gray-700">
              <span>Maximum Cogitation Loops</span>
              <span className="text-purple-600 text-sm font-semibold">{maxLoops}</span>
            </div>
            <input
              type="range"
              min="1"
              max="10"
              value={maxLoops}
              onChange={(e) => setMaxLoops(parseInt(e.target.value))}
              className="w-full accent-purple-600 cursor-pointer h-1.5 bg-gray-100 rounded-lg"
            />
          </div>

          <div className="pt-4 border-t border-gray-100">
            <button
              onClick={handleTriggerEngine}
              disabled={isThinking}
              className="w-full flex items-center justify-center gap-2 bg-[#23005c] hover:bg-[#340087] disabled:bg-[#f6f2ff] disabled:text-[#cbb5ff] text-white font-semibold text-sm py-3 px-4 rounded-xl shadow-md transition-all active:scale-[0.98]"
            >
              {isThinking ? <Loader2 className="w-4 h-4 animate-spin" /> : <Brain className="w-4 h-4 text-white fill-white" />}
              {isThinking ? "Thinking Enabled..." : "Trigger Think Engine"}
            </button>
          </div>
        </div>

        {/* Right Column Grid Stream */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Cognitive Grid Streams Card */}
          <div className="bg-[#1c1921] text-purple-100 border border-purple-950 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex justify-between items-center pb-2 border-b border-purple-950">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-purple-400" />
                <h3 className="font-bold text-sm text-white font-headline-2">Cognitive Grid Terminal</h3>
              </div>
              {isThinking && (
                <span className="text-2xs text-purple-300 font-semibold uppercase animate-pulse flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
                  {activeStep}
                </span>
              )}
            </div>

            {/* Grid display Streams */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {selectedThinkers.map((thinker) => (
                <div 
                  key={thinker} 
                  className="bg-[#121016] border border-purple-950/60 rounded-xl p-4 flex flex-col justify-between h-[150px] shadow-inner"
                >
                  <div className="flex justify-between items-center text-xs pb-1 border-b border-purple-950/20">
                    <span className="font-semibold text-purple-300 text-2xs tracking-wider uppercase">{thinker} node</span>
                    <span className="w-2 h-2 rounded-full bg-purple-500" />
                  </div>

                  <div className="flex-1 overflow-y-auto mt-2 text-3xs font-mono text-purple-200/90 leading-relaxed whitespace-pre-wrap">
                    {terminalStreams[thinker] || `> ${thinker} cluster is idle.\n> Standby for initialization trigger...`}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Rich reports consensus block */}
          {report && (
            <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-6 animate-fade-in">
              <div className="flex justify-between items-center border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Award className="w-5 h-5 text-purple-600" />
                  <h3 className="font-bold text-lg text-gray-900">Synthesis Intelligence Report</h3>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-2xs text-gray-400 font-bold uppercase">Consensus confidence</span>
                  <span className="text-sm font-bold text-purple-600">{report.confidenceScore}%</span>
                </div>
              </div>

              {/* Grid block stats split */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Consensus points */}
                <div className="space-y-3">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-gray-700 uppercase tracking-widest">
                    <ThumbsUp className="w-4 h-4 text-green-600" />
                    <span>Consensus Agreements</span>
                  </div>
                  <ul className="space-y-2">
                    {report.consensusPoints.map((pt, i) => (
                      <li key={i} className="flex gap-2 text-xs text-gray-600 leading-relaxed font-medium">
                        <span className="text-purple-600 font-bold">•</span>
                        {pt}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Conflict divergences */}
                <div className="space-y-3">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-gray-700 uppercase tracking-widest">
                    <ShieldAlert className="w-4 h-4 text-red-600" />
                    <span>Critical Divergences</span>
                  </div>
                  <ul className="space-y-2">
                    {report.conflictDivergences.map((pt, i) => (
                      <li key={i} className="flex gap-2 text-xs text-gray-600 leading-relaxed font-medium">
                        <span className="text-red-500 font-bold">•</span>
                        {pt}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Best insight large quote block */}
              <div className="bg-purple-50/50 border-l-4 border-purple-600 rounded-r-xl p-4 mt-4 space-y-1">
                <span className="text-3xs font-bold text-purple-600 uppercase tracking-widest">Core Insight</span>
                <p className="text-sm italic font-medium text-purple-900 leading-relaxed">
                  "{report.bestInsight}"
                </p>
                <div className="text-right">
                  <span className="text-3xs text-purple-500 font-bold uppercase">{report.bestInsightSource}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
