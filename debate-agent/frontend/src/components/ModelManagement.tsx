import React, { useState } from 'react';
import {
  Plus, Cpu, RefreshCw, Zap, AlertCircle, Activity, Bot, Play, Share2
} from 'lucide-react';
import { ModelStatus } from '../types';
import { modelsApi } from '../api';

interface ModelManagementProps {
  models: ModelStatus[];
  onToggleModel: (id: string) => void;
  onAddNewModel: (model: any) => void;
}

export default function ModelManagement({ models, onToggleModel, onAddNewModel }: ModelManagementProps) {
  const [testingModelId, setTestingModelId] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<Record<string, { status: string; latency: string }>>({});

  const handleTestConnection = async (id: string) => {
    setTestingModelId(id);
    try {
      const result = await modelsApi.test(id);
      setTestResults(prev => ({
        ...prev,
        [id]: {
          status: result.status === 'success' ? 'Online' : 'Failed',
          latency: result.latency_ms ? `${Math.round(result.latency_ms)}ms` : 'N/A',
        }
      }));
    } catch {
      setTestResults(prev => ({
        ...prev,
        [id]: { status: 'Failed', latency: 'N/A' }
      }));
    } finally {
      setTestingModelId(null);
    }
  };

  const distributionData = [
    { name: "MIMO-4 Turbo", percentage: 44, color: "bg-blue-600", colorLight: "bg-blue-100" },
    { name: "Claude 3.5 Sonnet", percentage: 28, color: "bg-indigo-600", colorLight: "bg-indigo-100" },
    { name: "GPT-4o Agent", percentage: 18, color: "bg-green-600", colorLight: "bg-green-100" },
    { name: "DeepSeek Coder", percentage: 10, color: "bg-amber-500", colorLight: "bg-amber-100" },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Model Integration Chamber</h1>
          <p className="text-gray-500 font-body-md mt-1">
            Configure register, toggle, and benchmark connected models across multiple providers.
          </p>
        </div>
        <button
          onClick={() => {
            const name = prompt("Enter new Model name:");
            if (name) {
              onAddNewModel({
                id: `model-${Date.now()}`,
                name,
                provider: prompt("Enter model provider:") || "Standard API",
                contextWindow: "128k Tokens",
                apiFormat: "REST / JSON",
                status: "Healthy",
                toggle: true,
                latency: "150ms"
              });
            }
          }}
          className="flex items-center gap-2 bg-[#2170e4] hover:bg-opacity-95 text-white font-semibold text-sm py-2.5 px-4 rounded-xl shadow-sm transition"
        >
          <Plus className="w-4 h-4" />
          Register Model
        </button>
      </div>

      {/* Model Registry Table */}
      <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
        <div className="p-5 border-b border-gray-100">
          <h3 className="font-bold text-base text-gray-900">Active Model Registry</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider w-16">Active</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Model Name</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Provider</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Context Size</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">API Schema</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Avg Latency</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {models.map((model) => {
                const testResult = testResults[model.id];
                const isTesting = testingModelId === model.id;
                return (
                  <tr key={model.id} className="hover:bg-gray-50/50 transition-colors">
                    <td className="px-6 py-4.5">
                      <button onClick={() => onToggleModel(model.id)}
                        className={`w-9 h-5 rounded-full p-0.5 transition-colors focus:outline-none cursor-pointer ${model.toggle ? 'bg-green-500' : 'bg-gray-200'}`}>
                        <div className={`w-4 h-4 rounded-full bg-white shadow transition-transform ${model.toggle ? 'translate-x-4' : 'translate-x-0'}`} />
                      </button>
                    </td>
                    <td className="px-6 py-4.5 font-semibold text-sm text-gray-900">
                      <div className="flex items-center gap-2">
                        <Cpu className={`w-4 h-4 ${model.toggle ? 'text-blue-500' : 'text-gray-400'}`} />
                        {model.name}
                      </div>
                    </td>
                    <td className="px-6 py-4.5 text-xs text-gray-600 font-medium">{model.provider}</td>
                    <td className="px-6 py-4.5">
                      <span className="text-2xs font-semibold px-2 py-0.5 bg-gray-100 text-gray-600 rounded-md">{model.contextWindow}</span>
                    </td>
                    <td className="px-6 py-4.5 text-xs text-gray-500 font-mono">{model.apiFormat}</td>
                    <td className="px-6 py-4.5 text-xs text-gray-700 font-semibold font-mono">
                      {testResult ? testResult.latency : model.latency || "N/A"}
                    </td>
                    <td className="px-6 py-4.5">
                      <span className={`text-2xs font-semibold px-2 py-0.5 rounded-full ${model.toggle ? 'bg-green-50 text-green-700 border border-green-100' : 'bg-gray-50 text-gray-500 border border-gray-100'}`}>
                        {model.toggle ? (testResult ? testResult.status : "Online") : "Inactive"}
                      </span>
                    </td>
                    <td className="px-6 py-4.5 text-right">
                      <button onClick={() => handleTestConnection(model.id)}
                        disabled={!model.toggle || isTesting}
                        className="text-primary hover:text-opacity-80 text-xs font-semibold disabled:text-gray-300 disabled:cursor-not-allowed flex items-center gap-1 ml-auto">
                        {isTesting ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Activity className="w-3.5 h-3.5" />}
                        {isTesting ? "Testing..." : "Test Connection"}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5 bg-gradient-to-br from-[#23005c] to-[#40128a] text-white rounded-2xl p-6 shadow-md flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-start mb-4">
              <span className="text-3xs font-bold px-2 py-1 bg-white/20 text-indigo-100 rounded-full tracking-wider uppercase">Pro Plan Advantage</span>
              <Zap className="w-6 h-6 text-warning" />
            </div>
            <h3 className="font-bold text-lg leading-tight mb-2">
              Save up to 40% Token Quotas with Multi-Agent local Cache Optimization.
            </h3>
            <p className="text-purple-200 text-xs leading-relaxed">
              Our local semantic compilation compiler intercepts redundant prompt tokens and dynamically routes contextual memories. Benefit from sub-millisecond latencies on repeated validation tasks.
            </p>
          </div>
          <div className="mt-8 flex gap-3 text-2xs font-bold uppercase tracking-wider border-t border-purple-900 pt-4">
            <span className="text-purple-300">Cache Hits Today: <span className="text-green-400 font-mono">14,249</span></span>
            <span className="text-purple-300">•</span>
            <span className="text-purple-300">Tokens Saved: <span className="text-green-400 font-mono">2.4M</span></span>
          </div>
        </div>

        <div className="lg:col-span-7 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
          <div>
            <h3 className="font-bold text-base text-gray-900">Inference Distribution</h3>
            <p className="text-xs text-gray-400">Volume of reasoning requests channeled across active thinker nodes today.</p>
          </div>
          <div className="space-y-4">
            {distributionData.map((node) => (
              <div key={node.name} className="space-y-1">
                <div className="flex justify-between text-xs font-semibold">
                  <span className="text-gray-700">{node.name}</span>
                  <span className="text-gray-900">{node.percentage}%</span>
                </div>
                <div className="w-full h-3.5 bg-gray-100 rounded-full overflow-hidden flex">
                  <div className={`h-full ${node.color} rounded-full transition-all duration-1000`} style={{ width: `${node.percentage}%` }} />
                </div>
              </div>
            ))}
          </div>
          <div className="pt-3 border-t border-gray-100 flex items-center gap-2 p-2 bg-blue-50/20 border border-blue-100/30 rounded-xl">
            <AlertCircle className="w-4 h-4 text-blue-600 shrink-0" />
            <p className="text-3xs text-blue-700 font-semibold leading-tight">
              Routing algorithm is currently balancing load automatically between AuraLabs and Anthropic endpoints.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
