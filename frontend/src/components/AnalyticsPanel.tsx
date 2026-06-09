import React from 'react';
import { 
  TrendingUp, 
  Cpu, 
  Clock, 
  BarChart3, 
  Award,
  Zap,
  Activity,
  AlertCircle
} from 'lucide-react';

export default function AnalyticsPanel() {
  const stats = [
    { name: "Global Logical Consistency", value: "94.2%", suffix: "+2.4% vs yesterday" },
    { name: "Autonomous Token Savings", value: "41.8%", suffix: "Cached compiler active" },
    { name: "Average Response Latency", value: "134ms", suffix: "Healthy optimization" },
    { name: "Active Pipeline Shards", value: "12 / 12", suffix: "100% operational throughput" },
  ];

  const trends = [
    { date: "09:00", activeTokens: 14200, hitRate: 88, latency: 125 },
    { date: "10:00", activeTokens: 25400, hitRate: 91, latency: 130 },
    { date: "11:00", activeTokens: 38900, hitRate: 94, latency: 124 },
    { date: "12:00", activeTokens: 42100, hitRate: 90, latency: 145 },
    { date: "13:00", activeTokens: 31200, hitRate: 92, latency: 132 },
    { date: "14:00", activeTokens: 18500, hitRate: 95, latency: 121 },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Analysis Terminal</h1>
        <p className="text-gray-500 font-body-md mt-1">
          Monitor multi-agent compiler workloads, routing latency metrics, and cache execution quotas in real-time.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <div key={i} className="bg-white border border-gray-200 rounded-2xl p-4.5 shadow-sm space-y-1 hover:border-blue-100 transition">
            <p className="text-3xs font-bold text-gray-400 uppercase tracking-widest">{stat.name}</p>
            <h2 className="text-2xl font-bold text-gray-900 font-headline-1">{stat.value}</h2>
            <p className="text-4xs text-green-600 font-semibold uppercase tracking-wider">{stat.suffix}</p>
          </div>
        ))}
      </div>

      {/* Grid: Trends Table & Metrics info */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Trends table */}
        <div className="lg:col-span-8 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex justify-between items-center pb-2 border-b border-gray-50">
            <h3 className="font-bold text-sm text-gray-900">Throughput Time-Series</h3>
            <span className="text-3xs font-bold text-gray-400 uppercase">Live streaming</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="px-4 py-3 font-semibold text-gray-500 uppercase tracking-wider">Timestamp</th>
                  <th className="px-4 py-3 font-semibold text-gray-500 uppercase tracking-wider">Active token rate (T/S)</th>
                  <th className="px-4 py-3 font-semibold text-gray-500 uppercase tracking-wider">Synthesized Hit Rate</th>
                  <th className="px-4 py-3 font-semibold text-gray-500 uppercase tracking-wider">Avg latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 font-medium">
                {trends.map((t, index) => (
                  <tr key={index} className="hover:bg-gray-50/50 transition">
                    <td className="px-4 py-3 font-semibold text-gray-850 font-mono">{t.date}</td>
                    <td className="px-4 py-3 text-blue-600 font-mono">{t.activeTokens} tokens</td>
                    <td className="px-4 py-3 text-green-600 font-mono">{t.hitRate}%</td>
                    <td className="px-4 py-3 text-indigo-600 font-mono">{t.latency}ms</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Cognitive capacity gauge */}
        <div className="lg:col-span-4 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center gap-1.5 pb-2 border-b border-gray-50">
              <Activity className="w-4 h-4 text-primary" />
              <h3 className="font-bold text-sm text-gray-900">Cognitive Capacity</h3>
            </div>

            <p className="text-2xs text-gray-400 leading-normal">
              Representing hardware resource utilisation during multi-model parallel synthesis operations today.
            </p>

            <div className="space-y-3.5">
              {/* RAM */}
              <div className="space-y-1">
                <div className="flex justify-between text-2xs font-semibold">
                  <span>Logic Thread Allocation</span>
                  <span>78%</span>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-600 rounded-full" style={{ width: '78%' }} />
                </div>
              </div>

              {/* Cache */}
              <div className="space-y-1">
                <div className="flex justify-between text-2xs font-semibold">
                  <span>Cache Hit Ratio</span>
                  <span>92%</span>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 rounded-full" style={{ width: '92%' }} />
                </div>
              </div>
            </div>
          </div>

          <div className="p-3 bg-indigo-50/50 border border-indigo-100/50 rounded-xl flex gap-2">
            <AlertCircle className="w-4 text-indigo-600 shrink-0 mt-0.5" />
            <span className="text-3xs text-indigo-700 leading-normal font-semibold">
              Automatic node balancing is running on cluster Shard-A4, preventing request throttling.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
