import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Play, Square, Loader, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function TerminalPanel() {
  const [logs, setLogs] = useState<string[]>([
    "System log terminal boot sequence initiated.",
    "[Auth Node] Multi-tenant gateway handshakes completed successfully.",
    "[Shard Host] Connected port 3000 mapping: container ingress active.",
    "[Compile Node] Active model registry load complete: MIMO-4, Claude-3.5, DeepSeek, GPT-4o online."
  ]);
  const [isRunning, setIsRunning] = useState(true);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!isRunning) return;

    const phrases = [
      () => `[Routing Engine] Dynamically balancing request load to Shard-A4 cluster (latency: ${Math.floor(Math.random() * 30) + 120}ms)`,
      () => `[Memory cache] Semantic prompt redundancy intercepted! Saved ${Math.floor(Math.random() * 100) + 200} tokens from local pipeline.`,
      () => `[Gateway Shard] Quota limit verified: client JD token balance remaining: ${Math.floor(Math.random() * 1000) + 123000} tokens.`,
      () => `[Validator Node] Logical coherence index calibrated to standard standard bounds: 94.2% stability index.`,
      () => `[Socket Agent] Broadcast ping thread safe. Heartbeat signal dispatched to localhost:3000.`
    ];

    const timer = setInterval(() => {
      const phrase = phrases[Math.floor(Math.random() * phrases.length)]();
      setLogs(prev => {
        const next = [...prev, phrase];
        if (next.length > 50) next.shift(); // keep it clean
        return next;
      });
    }, 2500);

    return () => clearInterval(timer);
  }, [isRunning]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Active Node Audit Terminal</h1>
          <p className="text-gray-500 font-body-md mt-1">
            Observe real-time console telemetry logs streamed from our active orchestration layers.
          </p>
        </div>

        {/* Start / Stop triggers */}
        <div className="flex gap-2">
          <button
            onClick={() => setIsRunning(!isRunning)}
            className={`flex items-center gap-2 text-xs font-semibold px-4 py-2 rounded-xl border transition shadow-sm ${
              isRunning 
                ? 'bg-red-50 hover:bg-red-100 text-red-650 border-red-100' 
                : 'bg-green-50 hover:bg-green-100 text-green-750 border-green-100'
            }`}
          >
            {isRunning ? <Square className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            {isRunning ? "Freeze Stream" : "Resume Stream"}
          </button>
        </div>
      </div>

      {/* Console Shell Component */}
      <div className="bg-[#0f0d13] text-purple-200 border border-purple-950 rounded-2xl p-5 shadow-xl space-y-4">
        <div className="flex justify-between items-center border-b border-purple-950 pb-3">
          <div className="flex items-center gap-2">
            <Terminal className="w-4.5 h-4.5 text-purple-400" />
            <span className="text-sm font-bold text-white font-mono">telemetry@aurasynth-node: ~</span>
          </div>

          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse" />
            <span className="text-2xs font-bold text-purple-300 font-mono">CONNECTION STABLE</span>
          </div>
        </div>

        {/* Lines logs display */}
        <div 
          ref={scrollRef}
          className="h-[380px] overflow-y-auto font-mono text-3xs p-4 bg-[#050407] rounded-xl border border-purple-950/20 space-y-2 pr-1 scrollbar-thin scrollbar-thumb-purple-900"
        >
          {logs.map((log, index) => {
            const isRedundancy = log.includes("redundancy");
            const isError = log.includes("Error") || log.includes("throttling");
            return (
              <p 
                key={index} 
                className={`${
                  isRedundancy 
                    ? 'text-amber-400 font-semibold' 
                    : isError 
                    ? 'text-red-400 font-bold' 
                    : 'text-purple-200/90'
                }`}
              >
                <span className="text-purple-500 font-bold font-mono">aurasynth_core_host $</span> {log}
              </p>
            );
          })}
        </div>

        {/* Summary grid details */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 text-[11px] font-semibold">
          <div className="flex items-center gap-2 bg-[#17141d] p-3 rounded-xl">
            <ShieldCheck className="w-4.5 h-4.5 text-green-500 shrink-0" />
            <p>TLS Certificates verified: Security active.</p>
          </div>
          <div className="flex items-center gap-2 bg-[#17141d] p-3 rounded-xl">
            <Loader className="w-4.5 h-4.5 text-blue-400 animate-spin shrink-0" />
            <p>Port routing latency holds: 132ms average.</p>
          </div>
          <div className="flex items-center gap-2 bg-[#17141d] p-3 rounded-xl">
            <AlertTriangle className="w-4.5 h-4.5 text-emerald-400 shrink-0" />
            <p>Zero exceptions registered last 24h.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
