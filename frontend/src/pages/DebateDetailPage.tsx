/**
 * Debate detail page — displays a single debate with messages, verdict, and execution.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import DebateView from '../components/DebateView';
import VerdictCard from '../components/VerdictCard';
import ExecutionPanel from '../components/ExecutionPanel';
import { getDebate, executeDebate } from '../services/api';

interface Message {
  id: string;
  debate_id: string;
  round_number: number;
  role: string;
  content: string;
  model_used: string;
  confidence: number;
  created_at: string | null;
}

interface Verdict {
  recommendation: string;
  winner: string;
  confidence: number;
  action_plan: string[];
}

interface Execution {
  id: string;
  debate_id: string;
  status: string;
  code_generated: string;
  execution_result: string | null;
  error_message: string | null;
  created_at: string | null;
  completed_at: string | null;
}

interface Debate {
  id: string;
  topic: string;
  status: string;
  created_at: string | null;
  completed_at: string | null;
  verdict: Verdict | null;
  action_plan: string[] | null;
  messages: Message[];
}

const DebateDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [debate, setDebate] = useState<Debate | null>(null);
  const [execution, setExecution] = useState<Execution | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDebate = useCallback(async () => {
    if (!id) return;
    try {
      const data = await getDebate(id);
      setDebate(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load debate');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchDebate();
  }, [fetchDebate]);

  const handleExecute = async () => {
    if (!debate) return;
    try {
      const result = await executeDebate(debate.id);
      setExecution(result);
      // Poll for execution result
      const pollInterval = setInterval(async () => {
        try {
          const res = await fetch(`/api/executions/${result.id}`);
          const data = await res.json();
          setExecution(data);
          if (data.status === 'success' || data.status === 'failed') {
            clearInterval(pollInterval);
          }
        } catch {
          // ignore poll errors
        }
      }, 2000);
    } catch (err: any) {
      console.error('Execute failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">加载中...</span>
      </div>
    );
  }

  if (error || !debate) {
    return (
      <div className="text-center p-12">
        <p className="text-red-600 mb-4">{error || '辩论不存在'}</p>
        <Link to="/history" className="text-blue-600 hover:underline">
          返回历史记录
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Link to="/history" className="text-sm text-blue-600 hover:underline mb-2 inline-block">
            &larr; 返回历史记录
          </Link>
          <h2 className="text-2xl font-bold text-gray-900">{debate.topic}</h2>
          <p className="text-sm text-gray-500 mt-1">
            创建于 {debate.created_at ? new Date(debate.created_at).toLocaleString('zh-CN') : '—'}
          </p>
        </div>
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

      {/* Messages */}
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">辩论过程</h3>
        <DebateView
          messages={debate.messages || []}
          loading={debate.status === 'running'}
        />
      </div>

      {/* Verdict */}
      {debate.verdict && (
        <VerdictCard
          recommendation={debate.verdict.recommendation}
          winner={debate.verdict.winner}
          confidence={debate.verdict.confidence}
          actionPlan={debate.verdict.action_plan}
          onExecute={debate.status === 'completed' ? handleExecute : undefined}
        />
      )}

      {/* Execution */}
      {execution && (
        <ExecutionPanel
          status={execution.status}
          codeGenerated={execution.code_generated}
          executionResult={execution.execution_result || undefined}
          errorMessage={execution.error_message || undefined}
        />
      )}
    </div>
  );
};

export default DebateDetailPage;
