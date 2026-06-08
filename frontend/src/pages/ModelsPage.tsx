import React, { useState } from 'react';

interface ModelConfig {
  id: string;
  name: string;
  provider: string;
  apiFormat: string;
  enabled: boolean;
  status: 'connected' | 'disconnected' | 'testing';
}

const initialModels: ModelConfig[] = [
  { id: '1', name: 'MIMO v2.5 Pro', provider: 'MIMO', apiFormat: 'OpenAI Schema', enabled: true, status: 'connected' },
  { id: '2', name: 'DeepSeek V4', provider: 'DeepSeek AI', apiFormat: 'OpenAI Schema', enabled: true, status: 'connected' },
  { id: '3', name: 'Claude Sonnet 4', provider: 'Anthropic', apiFormat: 'Anthropic SDK', enabled: false, status: 'disconnected' },
  { id: '4', name: 'GPT-4o', provider: 'OpenAI', apiFormat: 'OpenAI Schema', enabled: false, status: 'disconnected' },
];

export default function ModelsPage() {
  const [models, setModels] = useState<ModelConfig[]>(initialModels);
  const [search, setSearch] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [testingId, setTestingId] = useState<string | null>(null);

  const filteredModels = models.filter(m =>
    m.name.toLowerCase().includes(search.toLowerCase()) ||
    m.provider.toLowerCase().includes(search.toLowerCase())
  );

  const toggleModel = (id: string) => {
    setModels(prev => prev.map(m => m.id === id ? { ...m, enabled: !m.enabled } : m));
  };

  const testConnection = (id: string) => {
    setTestingId(id);
    setTimeout(() => {
      setModels(prev => prev.map(m => m.id === id ? { ...m, status: 'connected' } : m));
      setTestingId(null);
    }, 2000);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in-up">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Model Management</h1>
        <p className="text-sm text-gray-500 mt-1">Manage API endpoints and performance presets.</p>
      </div>

      {/* Toolbar */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-1">
          <div className="relative flex-1 max-w-md">
            <span className="material-icons absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg">search</span>
            <input
              type="text"
              placeholder="Search models..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="flex items-center gap-1.5 px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50">
            <span className="material-icons text-base">filter_list</span>
            Provider
          </button>
          <button className="flex items-center gap-1.5 px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50">
            <span className="material-icons text-base">settings</span>
            Schema
          </button>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-1.5 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors"
        >
          <span className="material-icons text-base">add</span>
          Add Model
        </button>
      </div>

      {/* Model Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredModels.map(model => (
          <div key={model.id} className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <span className="material-icons text-white text-lg">smart_toy</span>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-gray-900">{model.name}</h3>
                  <p className="text-xs text-gray-500">{model.provider}</p>
                </div>
              </div>
              <button
                onClick={() => toggleModel(model.id)}
                className={`relative w-10 h-6 rounded-full transition-colors ${model.enabled ? 'bg-green-500' : 'bg-gray-300'}`}
              >
                <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${model.enabled ? 'left-[18px]' : 'left-0.5'}`} />
              </button>
            </div>

            <div className="mb-4">
              <span className="inline-block px-2 py-0.5 rounded bg-gray-100 text-xs text-gray-600">
                {model.apiFormat}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => testConnection(model.id)}
                disabled={testingId === model.id}
                className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition-colors disabled:opacity-50"
              >
                {testingId === model.id ? (
                  <>
                    <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Testing...
                  </>
                ) : (
                  <>
                    <span className="material-icons text-base">cable</span>
                    Test Connection
                  </>
                )}
              </button>
              <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg">
                <span className="material-icons text-base">more_vert</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Performance Presets */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Performance Presets</h2>
        <p className="text-sm text-gray-500 mb-4">Enable hardware-accelerated quantization and local caching for all your connected models with one click.</p>
        <div className="flex items-center gap-4">
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors">
            <span className="material-icons text-base">speed</span>
            Enable Fast Mode
          </button>
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
            <span className="material-icons text-base">memory</span>
            Local Cache
          </button>
        </div>
      </div>

      {/* Add Model Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center" onClick={() => setShowAddModal(false)}>
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full mx-4" onClick={e => e.stopPropagation()}>
            <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Add AI Model</h2>
              <button onClick={() => setShowAddModal(false)} className="p-1 hover:bg-gray-100 rounded-lg">
                <span className="material-icons text-gray-400">close</span>
              </button>
            </div>
            <div className="px-6 py-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Model Name *</label>
                <input type="text" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="e.g. My Custom Model" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Provider *</label>
                <input type="text" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="e.g. OpenAI" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">API Endpoint *</label>
                <input type="text" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="https://api.example.com/v1" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">API Key *</label>
                <input type="password" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="sk-..." />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">API Format</label>
                <div className="flex gap-4">
                  {['OpenAI', 'Anthropic', 'Gemini'].map(fmt => (
                    <label key={fmt} className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
                      <input type="radio" name="apiFormat" value={fmt} defaultChecked={fmt === 'OpenAI'} className="text-blue-600" />
                      {fmt}
                    </label>
                  ))}
                </div>
              </div>
            </div>
            <div className="px-6 py-4 border-t border-gray-100 flex justify-end gap-3">
              <button onClick={() => setShowAddModal(false)} className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">Cancel</button>
              <button onClick={() => setShowAddModal(false)} className="px-4 py-2 text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 rounded-lg">Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
