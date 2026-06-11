import React from 'react';
import { 
  MessageSquare, 
  Brain, 
  ChevronRight, 
  AlertCircle, 
  ArrowRight,
  TrendingUp,
  Cpu,
  Clock,
  Zap
} from 'lucide-react';
import { ActivityItem, ModelStatus } from '../types';

interface HomeDashboardProps {
  activities: ActivityItem[];
  models: ModelStatus[];
  onSelectDebate: () => void;
  onSelectThink: () => void;
  onViewAllHistory: () => void;
  onViewModelStatus: () => void;
}

export default function HomeDashboard({
  activities,
  models,
  onSelectDebate,
  onSelectThink,
  onViewAllHistory,
  onViewModelStatus
}: HomeDashboardProps) {
  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="relative overflow-hidden bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
        <div className="absolute top-0 right-0 w-80 h-full bg-gradient-to-l from-indigo-50/50 to-transparent pointer-events-none rounded-r-2xl" />
        <div className="absolute top-1/2 right-12 -translate-y-1/2 w-48 h-48 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
        
        <div className="max-w-2xl relative z-10">
          <h1 className="font-bold text-2xl text-gray-900 tracking-tight mb-2">
            Hello, let's start your AI collaboration
          </h1>
          <p className="text-gray-500 font-body-lg">
            Select a mode to begin exploring multi-agent intelligence and autonomous reasoning.
          </p>
        </div>
      </div>

      {/* Mode Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Debate Mode Card */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between group hover:border-indigo-200 transition-all">
          <div>
            <div className="flex justify-between items-start mb-4">
              <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <MessageSquare className="w-6 h-6" />
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 bg-blue-50 text-blue-600 rounded-full tracking-wide">
                Multi-Agent
              </span>
            </div>
            <h3 className="font-bold text-lg text-gray-900 mb-2">AI Debate Mode</h3>
            <p className="text-gray-500 text-sm leading-relaxed mb-6">
              Pitting models against each other to discover truth, find edge cases, or refine complex arguments through dialectical synthesis.
            </p>
          </div>
          <button 
            onClick={onSelectDebate}
            className="w-full flex items-center justify-center gap-2 bg-[#6b38d4] hover:bg-opacity-90 text-white font-medium text-sm py-3 px-4 rounded-xl shadow-sm transition-all group-hover:shadow group-hover:scale-[1.01]"
          >
            Start Session
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Think Mode Card */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between group hover:border-[#b75b00]/30 transition-all">
          <div>
            <div className="flex justify-between items-start mb-4">
              <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
                <Brain className="w-6 h-6" />
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 bg-purple-50 text-purple-600 rounded-full tracking-wide">
                Deep Reasoning
              </span>
            </div>
            <h3 className="font-bold text-lg text-gray-900 mb-2">Independent Think Mode</h3>
            <p className="text-gray-500 text-sm leading-relaxed mb-6">
              Allow a single model to use recursive self-correction and multi-step Chain-of-Thought processing for complex problem-solving.
            </p>
          </div>
          <button 
            onClick={onSelectThink}
            className="w-full flex items-center justify-center gap-2 bg-white hover:bg-gray-50 text-primary border border-gray-200 font-medium text-sm py-3 px-4 rounded-xl shadow-sm transition-all group-hover:border-primary group-hover:scale-[1.01]"
          >
            Start Task
            <Zap className="w-4 h-4 text-warning" />
          </button>
        </div>
      </div>

      {/* Activities and Status Section */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        {/* Recent Activity List */}
        <div className="xl:col-span-7 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold text-lg text-gray-900">Recent Activity</h3>
            <button 
              onClick={onViewAllHistory}
              className="text-primary text-sm font-semibold hover:underline flex items-center gap-1"
            >
              View All
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="divide-y divide-gray-100">
            {activities.map((act) => (
              <div key={act.id} className="py-4 first:pt-0 last:pb-0 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                    act.type === 'Debate' 
                      ? 'bg-blue-50 text-blue-600' 
                      : 'bg-purple-50 text-purple-600'
                  }`}>
                    {act.type === 'Debate' ? <MessageSquare className="w-5 h-5" /> : <Brain className="w-5 h-5" />}
                  </div>
                  <div>
                    <h5 className="font-semibold text-sm text-gray-900">{act.title}</h5>
                    <p className="text-xs text-gray-500 font-medium">
                      {act.type} • {act.agentsCount ? `${act.agentsCount} agents` : act.agentName} • {act.timeAgo}
                    </p>
                  </div>
                </div>

                <div className="flex items-center">
                  <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                    act.status === 'Completed' 
                      ? 'bg-green-50 text-green-700 border border-green-100' 
                      : act.status === 'In Progress' 
                      ? 'bg-blue-50 text-blue-700 border border-blue-100' 
                      : 'bg-red-50 text-red-700 border border-red-100'
                  }`}>
                    {act.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Model Status column */}
        <div className="xl:col-span-5 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-lg text-gray-900">Model Status</h3>
              <button 
                onClick={onViewModelStatus}
                className="text-gray-500 hover:text-gray-900 text-xs font-semibold flex items-center gap-1"
              >
                Manage Models
                <ChevronRight className="w-4" />
              </button>
            </div>

            <div className="space-y-3">
              {models.map((model) => (
                <div 
                  key={model.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-200 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center text-blue-700">
                      <Cpu className="w-4 h-4" />
                    </div>
                    <div>
                      <h6 className="font-semibold text-sm text-gray-900">{model.name}</h6>
                      <p className="text-xs text-gray-400">{model.provider}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <div className={`w-2 h-2 rounded-full ${
                      model.status === 'Online' || model.status === 'Healthy' 
                        ? 'bg-green-500 animate-pulse' 
                        : 'bg-gray-300'
                    }`} />
                    <span className="text-xs font-medium text-gray-600">
                      {model.status === 'Online' || model.status === 'Healthy' ? 'Online' : 'Offline'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Alert maintenance banner */}
          <div className="mt-6 flex items-start gap-2.5 p-3.5 bg-blue-50/50 border border-blue-100 text-blue-800 rounded-xl">
            <AlertCircle className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
            <p className="text-xs leading-relaxed font-medium">
              Scheduled maintenance for Claude clusters in 4 hours. No significant impact expected.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
