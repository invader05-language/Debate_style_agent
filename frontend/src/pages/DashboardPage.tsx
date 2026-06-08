import React from 'react';
import { Link } from 'react-router-dom';

const modeCards = [
  {
    icon: 'forum',
    title: 'Multi-Agent Debate',
    desc: 'Pitting models against each other to discover truth, find edge cases, or refine complex arguments through dialectical synthesis.',
    link: '/debate/new',
    gradient: 'from-blue-500 to-cyan-400',
  },
  {
    icon: 'psychology',
    title: 'Single Agent Thinking',
    desc: 'Allow a single model to use recursive self-correction and multi-step Chain-of-Thought processing for complex problem-solving.',
    link: '/think/new',
    gradient: 'from-purple-500 to-pink-400',
  },
];

const modelStatus = [
  { name: 'MIMO', icon: 'cloud_done', status: 'Online', color: 'text-green-500' },
  { name: 'DeepSeek', icon: 'memory', status: 'Online', color: 'text-green-500' },
  { name: 'Claude 3.5', icon: 'psychology', status: 'Online', color: 'text-green-500' },
  { name: 'GPT-4o', icon: 'api', status: 'Offline', color: 'text-gray-400' },
];

export default function DashboardPage() {
  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in-up">
      {/* Hero */}
      <div className="text-center py-4">
        <div className="inline-block px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-medium mb-4">
          Pro Plan Activated
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Select a mode to begin exploring multi-agent intelligence
        </h1>
        <p className="text-sm text-gray-500">
          and autonomous reasoning.
        </p>
      </div>

      {/* Mode Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {modeCards.map((card) => (
          <Link
            key={card.title}
            to={card.link}
            className="group bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer"
          >
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center mb-4`}>
              <span className="material-icons text-white text-xl">{card.icon}</span>
            </div>
            <h2 className="text-lg font-semibold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
              {card.title}
            </h2>
            <p className="text-sm text-gray-500 leading-relaxed mb-4">
              {card.desc}
            </p>
            <span className="text-sm font-medium text-blue-600 group-hover:text-blue-700 flex items-center gap-1">
              Get Started
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </span>
          </Link>
        ))}
      </div>

      {/* Model Status */}
      <div>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Agent Status</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {modelStatus.map((model) => (
            <div key={model.name} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center">
                  <span className="material-icons text-gray-600">{model.icon}</span>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">{model.name}</p>
                  <div className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${model.status === 'Online' ? 'bg-green-500' : 'bg-gray-300'}`} />
                    <span className={`text-xs ${model.color}`}>{model.status}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Notice */}
      <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-xl border border-blue-100">
        <span className="material-icons text-blue-500 text-lg mt-0.5">info</span>
        <p className="text-sm text-blue-700">
          Scheduled maintenance for Claude clusters in 4 hours.
        </p>
      </div>
    </div>
  );
}
