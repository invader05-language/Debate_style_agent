/**
 * Memory page component for displaying and searching memories.
 */

import React, { useState, useEffect } from 'react';
import { listMemories, searchMemories } from '../services/api';

interface Memory {
  id: string;
  topic: string;
  debate_summary: string;
  outcome: string | null;
  confidence: number;
  tags: string[];
  lessons_learned: string[];
  created_at: string | null;
}

const MemoryPage: React.FC = () => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadMemories();
  }, []);

  const loadMemories = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listMemories();
      setMemories(result.memories || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load memories');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadMemories();
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await searchMemories(searchQuery);
      setMemories(result.memories || []);
    } catch (err: any) {
      setError(err.message || 'Failed to search memories');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
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
          onClick={loadMemories}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          重试
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search Section */}
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          记忆库
        </h2>
        <div className="flex space-x-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="搜索记忆..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearch}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            搜索
          </button>
          <button
            onClick={loadMemories}
            className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            重置
          </button>
        </div>
      </div>

      {/* Memory List */}
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          记忆列表
        </h3>

        {memories.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            暂无记忆记录
          </p>
        ) : (
          <div className="space-y-4">
            {memories.map((memory) => (
              <div
                key={memory.id}
                className="p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="text-lg font-medium text-gray-900">
                      {memory.topic}
                    </h4>
                    <p className="text-sm text-gray-600 mt-2">
                      {memory.debate_summary}
                    </p>
                    {memory.outcome && (
                      <p className="text-sm text-green-600 mt-2">
                        结果: {memory.outcome}
                      </p>
                    )}
                  </div>
                  <div className="ml-4 flex flex-col items-end">
                    <span className="text-sm text-gray-500">
                      信心度: {(memory.confidence * 100).toFixed(0)}%
                    </span>
                    {memory.tags && memory.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {memory.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                {memory.lessons_learned && memory.lessons_learned.length > 0 && (
                  <div className="mt-3">
                    <h5 className="text-sm font-medium text-gray-700">经验教训:</h5>
                    <ul className="list-disc list-inside text-sm text-gray-600 mt-1">
                      {memory.lessons_learned.map((lesson, index) => (
                        <li key={index}>{lesson}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {memory.created_at && (
                  <p className="text-xs text-gray-400 mt-3">
                    创建时间: {new Date(memory.created_at).toLocaleString()}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MemoryPage;
