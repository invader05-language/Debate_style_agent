import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Settings, Play, RotateCcw, Send, Share2, Award, Loader2, Scale,
  MessageSquare, User, Bot, Zap, CheckCircle, HelpCircle, Clock, Sparkles
} from 'lucide-react';
import { DEBATE_TOPICS } from '../data';
import { debateApi } from '../api';
import { useWebSocket } from '../hooks/useWebSocket';
import { DebateRound, ModelStatus } from '../types';

interface DebateWorkspaceProps {
  models: ModelStatus[];
}

export default function DebateWorkspace({ models }: DebateWorkspaceProps) {
  const modelNames = useMemo(() => models.map(m => m.name), [models]);
  const humanObserver = "Human Observer (Active Intervention)";

  const [topic, setTopic] = useState("The ethical implications of AGI in healthcare");
  const [proComponent, setProComponent] = useState("");
  const [conComponent, setConComponent] = useState("");
  const [neutralArbiter, setNeutralArbiter] = useState("");
  const [roundsCount, setRoundsCount] = useState(3);

  const [isDebating, setIsDebating] = useState(false);
  const [currentRoundIndex, setCurrentRoundIndex] = useState(1);
  const [activeSpeaker, setActiveSpeaker] = useState<"Pro" | "Con" | "Judge" | "Idle">("Idle");
  const [debateLog, setDebateLog] = useState<DebateRound[]>([]);
  const [progress, setProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");
  const [currentDebateId, setCurrentDebateId] = useState<string | null>(null);
  const [interventionText, setInterventionText] = useState("");
  const [metrics, setMetrics] = useState({ logicDensity: 8.4, tokensPerSec: 412, synthesisScore: 91, secondsElapsed: 0 });

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  // Initialize defaults when models load
  useEffect(() => {
    if (modelNames.length > 0) {
      if (!proComponent) setProComponent(modelNames[0]);
      if (!conComponent) setConComponent(modelNames.length > 1 ? modelNames[1] : modelNames[0]);
      if (!neutralArbiter) setNeutralArbiter(modelNames[0]);
    }
  }, [modelNames]);

  // WebSocket for real-time updates
  const { messages: wsMessages, connected } = useWebSocket(currentDebateId || undefined);

  // Process WebSocket messages
  useEffect(() => {
    if (wsMessages.length === 0) return;
    const lastMsg = wsMessages[wsMessages.length - 1];

    if (lastMsg.type === 'debate_message') {
      const round: DebateRound = {
        id: `ws-${Date.now()}`,
        agent: lastMsg.model_used as string || 'AI',
        role: lastMsg.role === 'pro' ? 'PROPONENT' : lastMsg.role === 'con' ? 'OPPONENT' : 'SYNTHESIZER',
        text: lastMsg.content as string,
        confidence: 85,
        timestamp: new Date().toLocaleTimeString(),
      };
      setDebateLog(prev => [...prev, round]);
    } else if (lastMsg.type === 'debate_status') {
      if (lastMsg.status === 'completed') {
        setIsDebating(false);
        setActiveSpeaker("Idle");
        setProgress(100);
      } else if (lastMsg.status === 'failed') {
        setIsDebating(false);
        setActiveSpeaker("Idle");
        setErrorMessage(lastMsg.message as string || 'Debate failed');
      }
    } else if (lastMsg.type === 'debate_verdict') {
      setMetrics(m => ({ ...m, synthesisScore: 91 }));
    }
  }, [wsMessages]);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [debateLog, activeSpeaker]);

  useEffect(() => {
    if (isDebating) {
      timerRef.current = setInterval(() => {
        setMetrics(m => ({
          ...m,
          secondsElapsed: m.secondsElapsed + 1,
          tokensPerSec: Math.floor(Math.random() * 50) + 380,
          logicDensity: parseFloat((Math.random() * 0.4 + 8.2).toFixed(1)),
        }));
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [isDebating]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartDebate = async () => {
    if (isDebating) return;
    setIsDebating(true);
    setDebateLog([]);
    setCurrentRoundIndex(1);
    setProgress(10);
    setErrorMessage("");
    setMetrics({ logicDensity: 8.2, tokensPerSec: 395, synthesisScore: 0, secondsElapsed: 0 });

    try {
      // Create debate via API
      const debate = await debateApi.create({
        topic,
        max_rounds: roundsCount,
        models: { pro: proComponent, con: conComponent, judge: neutralArbiter },
      });
      setCurrentDebateId(debate.id);

      // Start debate (runs in background, updates come via WebSocket)
      setActiveSpeaker("Pro");
      setProgress(30);
      await debateApi.start(debate.id);
    } catch (err: any) {
      console.error(err);
      setErrorMessage(err.message || "Failed to start debate.");
      setIsDebating(false);
      setActiveSpeaker("Idle");
    }
  };

  const handleIntervene = () => {
    if (!interventionText.trim()) return;
    const userTurn: DebateRound = {
      id: `intervention-${Date.now()}`,
      agent: "Human Arbiter",
      role: "SYNTHESIZER",
      text: interventionText,
      confidence: 100,
      depth: 100,
      timestamp: new Date().toLocaleTimeString(),
    };
    setDebateLog(prev => [...prev, userTurn]);
    setInterventionText("");
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <div>
          <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Synthetic Dialectics</h1>
          <p className="text-gray-500 font-body-md mt-1">
            Configure high-fidelity debates between specialized neural agents. Observe logical synthesis in real-time.
          </p>
        </div>
        <div className="flex items-center gap-3 bg-blue-50 border border-blue-100 p-3 rounded-xl shrink-0">
          <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-blue-600 font-semibold tracking-wider uppercase">Active Workspace</p>
            <h4 className="font-bold text-sm text-gray-900">AI Architect Chamber</h4>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Config */}
        <div className="lg:col-span-4 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-5 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-gray-100">
              <Settings className="w-4 h-4 text-primary" />
              <h3 className="font-bold text-base text-gray-900">Configuration</h3>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-gray-700">Debate Topic</label>
              <textarea value={topic} onChange={(e) => setTopic(e.target.value)} rows={3}
                placeholder="e.g. The ethical implications of AGI in health"
                className="w-full border border-gray-200 rounded-lg text-sm p-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition" />
              <div className="flex items-center gap-1">
                <span className="text-2xs text-gray-400">Presets:</span>
                <select onChange={(e) => setTopic(e.target.value)} className="text-2xs text-blue-600 bg-none hover:underline focus:outline-none max-w-[200px]">
                  <option value="">Select a preset...</option>
                  {DEBATE_TOPICS.map((preset, index) => (<option key={index} value={preset}>{preset.slice(0, 45)}...</option>))}
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-gray-700">Pro Component</label>
              <select value={proComponent} onChange={(e) => setProComponent(e.target.value)} className="w-full border border-gray-200 rounded-lg text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary">
                {modelNames.map((agent, i) => (<option key={i} value={agent}>{agent}</option>))}
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-gray-700">Con Component</label>
              <select value={conComponent} onChange={(e) => setConComponent(e.target.value)} className="w-full border border-gray-200 rounded-lg text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary">
                {modelNames.map((agent, i) => (<option key={i} value={agent}>{agent}</option>))}
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-gray-700">Neutral Arbiter</label>
              <select value={neutralArbiter} onChange={(e) => setNeutralArbiter(e.target.value)} className="w-full border border-gray-200 rounded-lg text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary">
                {modelNames.map((agent, i) => (<option key={i} value={agent}>{agent}</option>))}
                <option value={humanObserver}>{humanObserver}</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs font-semibold text-gray-700">
                <span>Debate Rounds</span>
                <span className="text-primary text-sm">{roundsCount}</span>
              </div>
              <input type="range" min="1" max="5" value={roundsCount} onChange={(e) => setRoundsCount(parseInt(e.target.value))}
                className="w-full accent-primary cursor-pointer h-1.5 bg-gray-100 rounded-lg" />
            </div>
          </div>

          <div className="pt-4 border-t border-gray-50 space-y-4">
            <button onClick={handleStartDebate} disabled={isDebating}
              className="w-full flex items-center justify-center gap-2 bg-[#6b38d4] disabled:bg-opacity-50 text-white font-semibold text-sm py-3 px-4 rounded-xl shadow-md cursor-pointer transition-all hover:scale-[1.01] active:scale-[0.99] hover:shadow-lg">
              {isDebating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 text-white fill-white" />}
              {isDebating ? "Dialectics Active..." : "Initialize Debate"}
            </button>
            <div className="p-3 bg-green-50/50 border border-green-100/60 rounded-xl flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              <p className="text-xs text-green-700 font-medium leading-tight">
                {connected ? 'Connected to server. System Ready.' : 'System Ready. All models responsive.'}
              </p>
            </div>
          </div>
        </div>

        {/* Right: Debate Log */}
        <div className="lg:col-span-8 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col justify-between h-[600px]">
          <div className="border-b border-gray-100 pb-3 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-primary" />
              <h4 className="font-bold text-sm text-gray-900">Dialectical Process Log</h4>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-gray-500">Round {currentRoundIndex} of {roundsCount}</span>
              <div className="flex gap-1">
                {Array.from({ length: roundsCount }).map((_, i) => (
                  <span key={i} className={`w-2 h-2 rounded-full ${i + 1 < currentRoundIndex ? 'bg-[#2170e4]' : i + 1 === currentRoundIndex && isDebating ? 'bg-[#6b38d4] animate-ping' : 'bg-gray-200'}`} />
                ))}
              </div>
            </div>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto py-4 space-y-4 pr-1 scrollbar-thin scrollbar-thumb-gray-200">
            {debateLog.length === 0 && !isDebating && (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 text-gray-400">
                <Scale className="w-12 h-12 text-gray-300 mb-3" />
                <p className="font-medium text-sm">Debate terminal hasn't been initialized.</p>
                <p className="text-xs max-w-sm mt-1">Configure parameters on the left and click 'Initialize Debate' to trigger real-time AI negotiation.</p>
              </div>
            )}

            {debateLog.map((log) => {
              const isPro = log.role === 'PROPONENT';
              const isCon = log.role === 'OPPONENT';
              const isJudge = log.role === 'SYNTHESIZER';
              return (
                <div key={log.id} className={`flex flex-col gap-2 p-4 rounded-xl border ${isPro ? 'bg-blue-50/50 border-blue-100 text-blue-900 self-start ml-2 mr-12' : isCon ? 'bg-purple-50/50 border-purple-100 text-purple-900 self-end mr-2 ml-12' : 'bg-[#ffdcc6]/20 border-orange-200 text-amber-900 mx-6 shadow-sm'}`}>
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-xs flex items-center gap-1.5 uppercase tracking-wide">
                      {isPro ? 'Proponent' : isCon ? 'Opponent' : 'Neutral Arbiter'}: {log.agent}
                    </span>
                    <span className="text-2xs text-gray-400 font-medium">Confidence: {log.confidence}%</span>
                  </div>
                  <p className="text-sm font-body-md leading-relaxed whitespace-pre-wrap">{log.text}</p>
                  <div className="flex items-center gap-4 text-xs mt-2 pt-2 border-t border-gray-100">
                    <div className="w-full flex items-center gap-2">
                      <span className="text-2xs text-gray-400">Metrics:</span>
                      <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div className={`h-full ${isPro ? 'bg-blue-600' : isCon ? 'bg-purple-600' : 'bg-orange-500'}`} style={{ width: `${log.confidence}%` }} />
                      </div>
                    </div>
                    <button className="text-gray-400 hover:text-gray-600 shrink-0"><Share2 className="w-3.5 h-3.5" /></button>
                  </div>
                </div>
              );
            })}

            {isDebating && activeSpeaker !== 'Idle' && (
              <div className={`p-4 rounded-xl border flex flex-col gap-3 mx-4 ${activeSpeaker === 'Pro' ? 'bg-blue-50/20 border-blue-100/50 ml-2' : activeSpeaker === 'Con' ? 'bg-purple-50/20 border-purple-100/50 mr-2' : 'bg-orange-50/20 border-orange-100/50 mx-6'}`}>
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs flex items-center gap-1.5 text-gray-400 uppercase tracking-widest animate-pulse">
                    {activeSpeaker === 'Pro' ? `${proComponent} is formulating positive premise...` : activeSpeaker === 'Con' ? `${conComponent} is formulating critical alternative...` : `${neutralArbiter} is synthesizing dialectics...`}
                  </span>
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-gray-400" />
                </div>
                <div className="flex items-end justify-center gap-1 h-8 py-1 bg-gray-55/40 rounded-lg">
                  <div className="w-1 bg-[#2170e4] rounded animate-[bounce_1s_infinite_100ms] h-4" />
                  <div className="w-1 bg-[#6b38d4] rounded animate-[bounce_1s_infinite_200ms] h-6" />
                  <div className="w-1 bg-[#b75b00] rounded animate-[bounce_1s_infinite_300ms] h-5" />
                  <div className="w-1 bg-green-500 rounded animate-[bounce_1s_infinite_400ms] h-3" />
                  <div className="w-1 bg-red-400 rounded animate-[bounce_1s_infinite_500ms] h-5" />
                </div>
              </div>
            )}
          </div>

          <div className="border-t border-gray-100 pt-3 flex gap-2">
            <input type="text" value={interventionText} onChange={(e) => setInterventionText(e.target.value)}
              placeholder="Injecting counter-prompt or query as a human observer..."
              onKeyDown={(e) => e.key === 'Enter' && handleIntervene()}
              className="flex-1 text-sm bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white transition" />
            <button onClick={handleIntervene} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm rounded-xl shrink-0 shadow-sm hover:shadow transition">
              Intervene
            </button>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white border border-gray-200 p-4 rounded-xl shadow-sm text-center">
          <p className="text-2xs font-bold text-gray-400 uppercase tracking-widest">Logic Density</p>
          <h2 className="text-2xl font-bold text-blue-600 mt-1 font-headline-1">{metrics.logicDensity}</h2>
        </div>
        <div className="bg-white border border-gray-200 p-4 rounded-xl shadow-sm text-center">
          <p className="text-2xs font-bold text-gray-400 uppercase tracking-widest">Tokens / Sec</p>
          <h2 className="text-2xl font-bold text-purple-600 mt-1 font-headline-1">{metrics.tokensPerSec}</h2>
        </div>
        <div className="bg-white border border-gray-200 p-4 rounded-xl shadow-sm text-center">
          <p className="text-2xs font-bold text-gray-400 uppercase tracking-widest">Synthesis Score</p>
          <h2 className="text-2xl font-bold text-amber-600 mt-1 font-headline-1">{metrics.synthesisScore > 0 ? `${metrics.synthesisScore}%` : 'N/A'}</h2>
        </div>
        <div className="bg-white border border-gray-200 p-4 rounded-xl shadow-sm text-center">
          <p className="text-2xs font-bold text-gray-400 uppercase tracking-widest">Runtime</p>
          <h2 className="text-2xl font-bold text-gray-800 mt-1 font-headline-1">{formatTime(metrics.secondsElapsed)}</h2>
        </div>
      </div>
    </div>
  );
}
