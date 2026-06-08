/**
 * Debate page component — redesigned with AuraSynth style.
 */

import React, { useState } from 'react';
import { useDebate } from '../hooks/useDebate';
import DebateView from '../components/DebateView';
import VerdictCard from '../components/VerdictCard';
import ExecutionPanel from '../components/ExecutionPanel';
import RoundProgress from '../components/RoundProgress';
import { executeDebate } from '../services/api';

const modelOptions = [
  { id: 'mimo', name: 'MIMO v2.5 Pro' },
  { id: 'deepseek', name: 'DeepSeek V4' },
  { id: 'claude', name: 'Claude Sonnet 4' },
  { id: 'gpt4o', name: 'GPT-4o' },
];

const DebatePage: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [proModel, setProModel] = useState('mimo');
  const [conModel, setConModel] = useState('deepseek');
  const [judgeModel, setJudgeModel] = useState('claude');
  const [rounds, setRounds] = useState(3);
  const [executionStatus, setExecutionStatus] = useState<string | null>(null);
  const [showGuide, setShowGuide] = useState(false);
  const [guideText, setGuideText] = useState('');
  const {
    debate,
    loading,
    error,
    wsConnected,
    currentRound,
    maxRounds,
    createNewDebate,
    startDebateById,
    connectWebSocket,
    disconnectWebSocket
  } = useDebate();

  const handleStartDebate = async () => {
    if (!topic.trim()) return;
    try {
      const debateId = await createNewDebate(topic);
      connectWebSocket(debateId);
      await startDebateById(debateId);
    } catch (err) {
      console.error('Failed to start debate:', err);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !loading && topic.trim()) {
      handleStartDebate();
    }
  };

  const handleExecute = async () => {
    if (!debate) return;
    try {
      setExecutionStatus('running');
      await executeDebate(debate.id);
      setExecutionStatus('success');
    } catch (err) {
      setExecutionStatus('failed');
      console.error('Failed to execute:', err);
    }
  };

  const handleRedebate = () => {
    setTopic('');
    setExecutionStatus(null);
    disconnectWebSocket();
  };

  const statusConfig: Record<string, { label: string; color: string; dot: string }> = {
    pending: { label: 'Pending', color: 'bg-gray-100 text-gray-700', dot: 'bg-gray-400' },
    running: { label: 'Debate in Progress', color: 'bg-blue-100 text-blue-700', dot: 'bg-blue-500' },
    completed: { label: 'Completed', color: 'bg-green-100 text-green-700', dot: 'bg-green-500' },
    failed: { label: 'Failed', color: 'bg-red-100 text-red-700', dot: 'bg-red-500' }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in-up">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configure high-fidelity debates</h1>
        <p className="text-sm text-gray-500 mt-1">between specialized neural agents. Observe logical synthesis and cross-model reasoning in real-time.</p>
      </div>

      {/* Configuration Panel */}
      {!debate && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center gap-2 mb-4">
            <span className="material-icons text-gray-400 text-lg">tune</span>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Configuration</h2>
          </div>

          {/* Topic Input */}
          <div className="mb-5">
            <label className="block text-sm font-medium text-gray-700 mb-2">Debate Topic</label>
            <textarea
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Enter the topic for debate, e.g. Should we adopt microservices architecture?"
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-sm min-h-[80px] resize-none"
              disabled={loading}
            />
          </div>

          {/* Model Selection */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-5">
            <div>
              <label className="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
                <span className="inline-flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-green-500" /> Pro Agent
                </span>
              </label>
              <select
                value={proModel}
                onChange={e => setProModel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {modelOptions.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
                <span className="inline-flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-red-500" /> Con Agent
                </span>
              </label>
              <select
                value={conModel}
                onChange={e => setConModel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {modelOptions.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
                <span className="inline-flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-yellow-500" /> Judge Agent
                </span>
              </label>
              <select
                value={judgeModel}
                onChange={e => setJudgeModel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {modelOptions.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
              </select>
            </div>
          </div>

          {/* Rounds Slider */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Rounds: <span className="text-blue-600 font-semibold">{rounds}</span>
            </label>
            <input
              type="range"
              min={1}
              max={10}
              value={rounds}
              onChange={e => setRounds(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>1</span><span>10</span>
            </div>
          </div>

          {/* Start Button */}
          <button
            onClick={handleStartDebate}
            disabled={loading || !topic.trim()}
            className="w-full py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Creating...
              </>
            ) : (
              <>
                <span className="material-icons text-lg">forum</span>
                Start Debate
              </>
            )}
          </button>

          {error && (
            <div className="mt-3 flex items-center gap-2 text-red-600 text-sm bg-red-50 px-4 py-2 rounded-lg">
              <span className="material-icons text-base">error</span>
              {error}
            </div>
          )}
        </div>
      )}

      {/* Processing Stream */}
      {debate && (
        <>
          {/* Status Bar */}
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg text-xs">
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
              <span className="text-gray-600">{wsConnected ? 'Connected' : 'Reconnecting...'}</span>
            </div>
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${statusConfig[debate.status]?.color || statusConfig.pending.color}`}>
              <span className={`w-1.5 h-1.5 rounded-full ${statusConfig[debate.status]?.dot || statusConfig.pending.dot} ${debate.status === 'running' ? 'animate-pulse' : ''}`} />
              {statusConfig[debate.status]?.label || debate.status}
            </span>
          </div>

          {/* Round Progress */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 px-6 py-4">
            <div className="flex items-center gap-2 mb-3">
              <span className="material-icons text-gray-400 text-lg">auto_awesome_motion</span>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Processing Stream</h2>
            </div>
            <RoundProgress currentRound={currentRound} maxRounds={maxRounds} status={debate.status} />
          </div>

          {/* Debate Messages */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <DebateView messages={debate.messages || []} loading={debate.status === 'running'} />
          </div>

          {/* User Guide Input */}
          {debate.status === 'running' && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <button
                onClick={() => setShowGuide(!showGuide)}
                className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700"
              >
                <span className="material-icons text-base">{showGuide ? 'expand_less' : 'expand_more'}</span>
                User Guidance (Optional)
              </button>
              {showGuide && (
                <div className="mt-3 flex gap-2">
                  <input
                    type="text"
                    value={guideText}
                    onChange={e => setGuideText(e.target.value)}
                    placeholder="Send a hint to influence the debate direction..."
                    className="flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium">Send</button>
                </div>
              )}
            </div>
          )}
        </>
      )}

      {/* Verdict */}
      {debate?.verdict && (
        <VerdictCard
          recommendation={debate.verdict.recommendation}
          winner={debate.verdict.winner}
          confidence={debate.verdict.confidence}
          actionPlan={debate.verdict.action_plan}
          onExecute={handleExecute}
          onRedebate={handleRedebate}
        />
      )}

      {/* Execution Panel */}
      {executionStatus && (
        <ExecutionPanel
          status={executionStatus}
          codeGenerated={debate?.action_plan?.join('\n')}
        />
      )}
    </div>
  );
};

export default DebatePage;
