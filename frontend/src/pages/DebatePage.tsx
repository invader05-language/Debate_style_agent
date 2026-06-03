/**
 * Debate page component.
 */

import React, { useState } from 'react';
import { useDebate } from '../hooks/useDebate';
import DebateView from '../components/DebateView';
import VerdictCard from '../components/VerdictCard';
import ExecutionPanel from '../components/ExecutionPanel';
import { executeDebate } from '../services/api';

const DebatePage: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [executionStatus, setExecutionStatus] = useState<string | null>(null);
  const {
    debate,
    loading,
    error,
    wsConnected,
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
    disconnectWebSocket();
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          开始新辩论
        </h2>
        <div className="flex space-x-4">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="输入辩论主题..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={handleStartDebate}
            disabled={loading || !topic.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '创建中...' : '开始辩论'}
          </button>
        </div>
        {error && (
          <p className="mt-2 text-red-600 text-sm">{error}</p>
        )}
      </div>

      {/* WebSocket Status */}
      {debate && (
        <div className="flex items-center space-x-2 text-sm">
          <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-gray-600">
            {wsConnected ? '实时连接已建立' : '未连接'}
          </span>
        </div>
      )}

      {/* Debate View */}
      {debate && (
        <div className="bg-white rounded-lg shadow-lg p-6 border">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">
              辩论过程
            </h2>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              debate.status === 'pending' ? 'bg-gray-100 text-gray-800' :
              debate.status === 'running' ? 'bg-blue-100 text-blue-800' :
              debate.status === 'completed' ? 'bg-green-100 text-green-800' :
              'bg-red-100 text-red-800'
            }`}>
              {debate.status === 'pending' && '等待开始'}
              {debate.status === 'running' && '辩论中'}
              {debate.status === 'completed' && '已完成'}
              {debate.status === 'failed' && '失败'}
            </span>
          </div>
          <DebateView
            messages={debate.messages || []}
            loading={debate.status === 'running'}
          />
        </div>
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
