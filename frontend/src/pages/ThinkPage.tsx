import React, { useState } from 'react';

const availableModels = [
  { id: 'mimo', name: 'MIMO v2.5 Pro', role: 'Logical Specialist', checked: true },
  { id: 'deepseek', name: 'DeepSeek V4', role: 'Analytical Engine', checked: false },
  { id: 'claude', name: 'Claude 3.5 Sonnet', role: 'Creative Strategist', checked: true },
  { id: 'gpt4o', name: 'GPT-4o', role: 'General Reasoner', checked: false },
];

export default function ThinkPage() {
  const [taskDesc, setTaskDesc] = useState('');
  const [models, setModels] = useState(availableModels);
  const [phase, setPhase] = useState<'config' | 'running' | 'done'>('config');

  const toggleModel = (id: string) => {
    setModels(prev => prev.map(m => m.id === id ? { ...m, checked: !m.checked } : m));
  };

  const selectedCount = models.filter(m => m.checked).length;

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in-up">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Single Agent Thinking</h1>
        <p className="text-sm text-gray-500 mt-1">Allow a single model to use recursive self-correction and multi-step Chain-of-Thought processing.</p>
      </div>

      {phase === 'config' && (
        <>
          {/* Task Description */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Task Description</h2>
            <textarea
              value={taskDesc}
              onChange={e => setTaskDesc(e.target.value)}
              placeholder="Describe the problem you want the AI to think deeply about..."
              className="w-full px-4 py-3 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[120px] resize-none"
            />
          </div>

          {/* Model Selection */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Select Thinkers</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {models.map(model => (
                <label
                  key={model.id}
                  className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-all ${
                    model.checked ? 'border-blue-200 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={model.checked}
                    onChange={() => toggleModel(model.id)}
                    className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{model.name}</p>
                    <p className="text-xs text-gray-500">{model.role}</p>
                  </div>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-400 mt-3">{selectedCount} model{selectedCount !== 1 ? 's' : ''} selected</p>
          </div>

          {/* Start Button */}
          <button
            onClick={() => setPhase('running')}
            disabled={!taskDesc.trim() || selectedCount < 1}
            className="w-full py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span className="material-icons text-lg">psychology</span>
            Start Thinking
          </button>
        </>
      )}

      {phase === 'running' && (
        <>
          {/* Status Bar */}
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg text-xs">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
              <span className="text-gray-600">Phase 1/2: Independent Thinking</span>
            </div>
            <span className="text-gray-400">2/3 models completed</span>
          </div>

          {/* Thinker Progress */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {models.filter(m => m.checked).map(model => (
              <div key={model.id} className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                    <span className="material-icons text-white text-sm">psychology</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{model.name}</p>
                    <p className="text-xs text-gray-500">{model.role}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-xs text-blue-600">
                  <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Thinking...
                </div>
              </div>
            ))}
          </div>

          {/* Synthesis Card */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <div className="bg-gradient-to-r from-purple-500 to-blue-500 px-6 py-4">
              <h2 className="text-lg font-semibold text-white">Synthesis Analysis</h2>
              <p className="text-sm text-white/80">Generated by AuraSynth-Omega Judge</p>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="material-icons text-green-500 text-lg">check_circle</span>
                  <h3 className="text-sm font-semibold text-gray-900">Consensus Points</h3>
                </div>
                <ul className="space-y-1 pl-7">
                  <li className="text-sm text-gray-600 list-disc">All agents agree on microservices architecture</li>
                  <li className="text-sm text-gray-600 list-disc">MVP-first approach is unanimously recommended</li>
                </ul>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="material-icons text-yellow-500 text-lg">rule</span>
                  <h3 className="text-sm font-semibold text-gray-900">Key Divergences</h3>
                </div>
                <ul className="space-y-1 pl-7">
                  <li className="text-sm text-gray-600 list-disc">GPT-4o favors aggressive scaling; Claude warns of brand erosion</li>
                  <li className="text-sm text-gray-600 list-disc">Differing views on the necessity of local LLM integration</li>
                </ul>
              </div>
              <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-100">
                <div className="flex items-center gap-2 mb-1">
                  <span className="material-icons text-yellow-600 text-base">star</span>
                  <span className="text-xs font-semibold text-yellow-700 uppercase tracking-wide">Best Insight</span>
                </div>
                <p className="text-sm text-yellow-800 italic">"Prioritize horizontal scaling before vertical optimization — latency is the user retention killer."</p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4 border-t border-gray-100">
                <button onClick={() => setPhase('done')} className="flex-1 py-2.5 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg text-sm transition-colors">
                  Confirm & Execute
                </button>
                <button onClick={() => setPhase('config')} className="flex-1 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg text-sm transition-colors">
                  Rethink
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {phase === 'done' && (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8 text-center">
          <span className="material-icons text-green-500 text-5xl mb-4">check_circle</span>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Thinking Complete</h2>
          <p className="text-sm text-gray-500 mb-6">The synthesis has been saved to your memory bank.</p>
          <button onClick={() => { setPhase('config'); setTaskDesc(''); }} className="px-6 py-2.5 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg text-sm transition-colors">
            Start New Think
          </button>
        </div>
      )}
    </div>
  );
}
