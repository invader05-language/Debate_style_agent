/**
 * History page component for displaying debate history.
 */

import React, { useState, useEffect } from 'react';
import { listDebates } from '../services/api';
import { Link } from 'react-router-dom';

interface Debate {
  id: string;
  topic: string;
  status: string;
  created_at: string | null;
  completed_at: string | null;
  verdict: any;
}

const HistoryPage: React.FC = () => {
  const [debates, setDebates] = useState<Debate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDebates();
  }, []);

  const loadDebates = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listDebates();
      setDebates(result.debates || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load debates');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-gray-100 text-gray-800';
      case 'running': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'executed': return 'bg-purple-100 text-purple-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'pending': return '等待中';
      case 'running': return '辩论中';
      case 'completed': return '已完成';
      case 'executed': return '已执行';
      case 'failed': return '失败';
      default: return status;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">加载中...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-8">
        <p className="text-red-600">{error}</p>
        <button
          onClick={loadDebates}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          重试
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          历史辩论记录
        </h2>

        {debates.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            暂无辩论记录
          </p>
        ) : (
          <div className="space-y-4">
            {debates.map((debate) => (
              <Link
                key={debate.id}
                to={`/debate/${debate.id}`}
                className="block p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">
                      {debate.topic}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {debate.created_at ? new Date(debate.created_at).toLocaleString() : ''}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(debate.status)}`}>
                    {getStatusLabel(debate.status)}
                  </span>
                </div>
                {debate.verdict && (
                  <p className="text-sm text-gray-600 mt-2">
                    推荐方案: {debate.verdict.recommendation?.substring(0, 100)}...
                  </p>
                )}
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
