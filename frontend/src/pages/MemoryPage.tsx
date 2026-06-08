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

  useEffect(() => { loadMemories(); }, []);

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
    if (!searchQuery.trim()) { loadMemories(); return; }
    setLoading(true);
    setError(null);
    try {
      const result = await searchMemories(searchQuery);
      setMemories(result.memories || []);
    } catch (err: any) {
      setError(err.message || 'Failed to search');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in-up">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl font-bold text-gray-900">Memory Bank</h1>
            <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-600 text-xs font-medium">Pro Plan</span>
          </div>
          <p className="text-sm text-gray-500">Persistent neural insights extracted from cross-model synthesis.</p>
        </div>
        <button className="flex items-center gap-1.5 px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50">
          <span className="material-icons text-base">download</span>
          Export
        </button>
      </div>

      {/* Search */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <span className="material-icons absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg">search</span>
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            placeholder="Search memories..."
            className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button onClick={handleSearch} className="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600">Search</button>
        <button onClick={loadMemories} className="px-4 py-2 border border-gray-200 text-gray-600 rounded-lg text-sm hover:bg-gray-50">Reset</button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <svg className="animate-spin h-6 w-6 text-blue-500" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span className="ml-3 text-sm text-gray-500">Loading memories...</span>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-center py-8">
          <span className="material-icons text-red-400 text-4xl mb-2">error</span>
          <p className="text-sm text-red-600 mb-4">{error}</p>
          <button onClick={loadMemories} className="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600">Retry</button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && memories.length === 0 && (
        <div className="text-center py-16">
          <span className="material-icons text-gray-300 text-5xl mb-4">psychology</span>
          <h3 className="text-lg font-medium text-gray-900 mb-1">No memories yet</h3>
          <p className="text-sm text-gray-500">Complete a debate or thinking session to generate insights</p>
        </div>
      )}

      {/* Memory Cards */}
      {!loading && memories.length > 0 && (
        <div className="space-y-4">
          {memories.map((memory, index) => (
            <div key={memory.id} className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
              {/* Header */}
              <div className="px-5 py-4 border-b border-gray-50">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-base font-semibold text-gray-900">{memory.topic}</h3>
                    <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                      <span>{memory.created_at ? new Date(memory.created_at).toLocaleDateString() : ''}</span>
                      <span>•</span>
                      <span>Confidence: {(memory.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                  <div className="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                      style={{ width: `${memory.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Body */}
              <div className="px-5 py-4 space-y-3">
                <p className="text-sm text-gray-600">{memory.debate_summary}</p>

                {memory.outcome && (
                  <div className="p-3 bg-green-50 rounded-lg border border-green-100">
                    <p className="text-sm text-green-700">{memory.outcome}</p>
                  </div>
                )}

                {/* Tags */}
                {memory.tags && memory.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1.5">
                    {memory.tags.map((tag, i) => (
                      <span key={i} className="px-2 py-0.5 rounded-full bg-gray-100 text-xs text-gray-600">{tag}</span>
                    ))}
                  </div>
                )}

                {/* Lessons Learned */}
                {memory.lessons_learned && memory.lessons_learned.length > 0 && (
                  <div className="pl-4 border-l-2 border-blue-200">
                    <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5 flex items-center gap-1">
                      <span className="material-icons text-sm">lightbulb</span>
                      Lessons Learned
                    </h4>
                    <ul className="space-y-1">
                      {memory.lessons_learned.map((lesson, i) => (
                        <li key={i} className="text-sm text-gray-600">{lesson}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MemoryPage;
