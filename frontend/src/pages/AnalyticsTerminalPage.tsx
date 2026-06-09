import React, { useState, useEffect } from 'react';

const logEntries = [
  { ts: '00:37:28.26', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:31.22', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:34.60', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:37.88', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:40.03', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:43.30', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:46.31', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:49.33', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:52.31', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
  { ts: '00:37:55.43', model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' },
];

const modelPoints = [
  { name: 'GPT-4o', x: 80, y: 10, color: 'bg-blue-500', shadow: 'shadow-blue-500/50' },
  { name: 'Claude 3.5', x: 40, y: 30, color: 'bg-purple-500', shadow: 'shadow-purple-500/50' },
  { name: 'MIMO-1', x: 15, y: 60, color: 'bg-green-500', shadow: 'shadow-green-500/50' },
  { name: 'DeepSeek', x: 60, y: 50, color: 'bg-yellow-500', shadow: 'shadow-yellow-500/50' },
];

const topics = [
  { name: 'Quantum Ethics', pct: '42.4%', colSpan: 'col-span-4 row-span-2', color: 'bg-blue-50 border-blue-200 text-blue-600', hoverColor: 'hover:bg-blue-100' },
  { name: 'Synthetic Bio', pct: '18.1%', colSpan: 'col-span-2 row-span-1', color: 'bg-purple-50 border-purple-200 text-purple-600', hoverColor: 'hover:bg-purple-100' },
  { name: 'Space Law', pct: '12.2%', colSpan: 'col-span-2 row-span-1', color: 'bg-orange-50 border-orange-200 text-orange-600', hoverColor: 'hover:bg-orange-100' },
  { name: 'AGI Alignment', pct: '15.3%', colSpan: 'col-span-3 row-span-1', color: 'bg-green-50 border-green-200 text-green-600', hoverColor: 'hover:bg-green-100' },
  { name: 'Others', pct: '12.0%', colSpan: 'col-span-3 row-span-1', color: 'bg-gray-100 border-gray-200 text-gray-600', hoverColor: 'hover:bg-gray-200' },
];

export default function AnalyticsTerminalPage() {
  const [logs, setLogs] = useState(logEntries);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const ts = now.toLocaleTimeString('en-GB', { hour12: false }) + '.' + String(Math.floor(Math.random() * 99)).padStart(2, '0');
      setLogs(prev => {
        const next = [...prev, { ts, model: 'MIMO-1', status: '200_OK', msg: 'System heartbeat pulse: synchronization stable.' }];
        return next.length > 10 ? next.slice(-10) : next;
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in-up">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics Terminal</h1>
          <p className="text-sm text-gray-500">Precision-engineered data visualization for the AuraSynth ecosystem.</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-xl">
            <span className="material-icons text-gray-400 text-lg">calendar_month</span>
            <select className="bg-transparent border-none focus:ring-0 text-sm font-medium py-0 pr-6">
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Quarter to Date</option>
            </select>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-xl">
            <span className="material-icons text-gray-400 text-lg">filter_list</span>
            <select className="bg-transparent border-none focus:ring-0 text-sm font-medium py-0 pr-6">
              <option>All Models</option>
              <option>MIMO-1</option>
              <option>DeepSeek-V2</option>
              <option>Claude 3.5</option>
              <option>GPT-4o</option>
            </select>
          </div>
        </div>
      </div>

      {/* Bento Grid */}
      <div className="grid grid-cols-12 gap-4">
        {/* Token Usage Trends */}
        <section className="col-span-12 lg:col-span-8 bg-white border border-gray-100 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-900">Token Usage Trends</h3>
              <p className="text-xs text-gray-500">Real-time throughput analysis across all active synthesis nodes.</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                <span className="text-xs text-gray-500">Prompt</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                <span className="text-xs text-gray-500">Completion</span>
              </div>
            </div>
          </div>
          <div className="h-[280px] w-full relative">
            <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none" viewBox="0 0 800 300">
              <defs>
                <linearGradient id="primary-grad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.15"></stop>
                  <stop offset="100%" stopColor="#3B82F6" stopOpacity="0"></stop>
                </linearGradient>
              </defs>
              <path d="M0,250 Q100,220 200,240 T400,100 T600,150 T800,50" fill="none" stroke="#3B82F6" strokeWidth="3"></path>
              <path d="M0,250 Q100,220 200,240 T400,100 T600,150 T800,50 V300 H0 Z" fill="url(#primary-grad)"></path>
              <path d="M0,280 Q100,260 200,270 T400,180 T600,220 T800,120" fill="none" stroke="#8B5CF6" strokeDasharray="8,4" strokeWidth="3"></path>
            </svg>
            <div className="absolute inset-0 flex flex-col justify-between opacity-10">
              {[0,1,2,3,4].map(i => <div key={i} className="w-full border-b border-gray-400"></div>)}
            </div>
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-400">
            <span>00:00</span><span>04:00</span><span>08:00</span><span>12:00</span><span>16:00</span><span>20:00</span><span>23:59</span>
          </div>
        </section>

        {/* Cost Analysis Metrics */}
        <section className="col-span-12 lg:col-span-4 flex flex-col gap-3">
          <div className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm flex-1 flex flex-col justify-center">
            <div className="flex items-center gap-2 text-blue-600 mb-2">
              <span className="material-icons text-lg">payments</span>
              <span className="text-sm font-medium">Estimated Cost</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">$1,284.42</div>
            <div className="flex items-center gap-1.5 text-green-600 mt-2">
              <span className="material-icons text-sm">trending_down</span>
              <span className="text-xs">-12.4% vs last period</span>
            </div>
          </div>
          <div className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm flex-1 flex flex-col justify-center">
            <div className="flex items-center gap-2 text-purple-600 mb-2">
              <span className="material-icons text-lg">speed</span>
              <span className="text-sm font-medium">Avg. Latency</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">420ms</div>
            <div className="flex items-center gap-1.5 text-red-500 mt-2">
              <span className="material-icons text-sm">trending_up</span>
              <span className="text-xs">+8.1% vs last period</span>
            </div>
          </div>
          <div className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm flex-1 flex flex-col justify-center">
            <div className="flex items-center gap-2 text-blue-600 mb-2">
              <span className="material-icons text-lg">database</span>
              <span className="text-sm font-medium">Token Usage</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">2.8M</div>
            <div className="flex items-center gap-1.5 text-green-600 mt-2">
              <span className="material-icons text-sm">trending_up</span>
              <span className="text-xs">+15.2% vs last period</span>
            </div>
          </div>
          <div className="bg-gray-900 text-white border border-transparent rounded-xl p-4 shadow-md flex-1 flex flex-col justify-center">
            <div className="flex items-center gap-2 mb-2">
              <span className="material-icons text-purple-300 text-lg">bolt</span>
              <span className="text-sm font-medium opacity-80">Efficiency Score</span>
            </div>
            <div className="text-2xl font-bold">98.2</div>
            <div className="w-full bg-white/20 h-1.5 rounded-full mt-2 overflow-hidden">
              <div className="bg-purple-300 h-full" style={{ width: '98.2%' }}></div>
            </div>
          </div>
        </section>

        {/* Model Performance Matrix */}
        <section className="col-span-12 lg:col-span-7 bg-white border border-gray-100 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-900">Model Performance Matrix</h3>
              <p className="text-xs text-gray-500">Efficiency frontier: Accuracy vs. Inference Latency.</p>
            </div>
          </div>
          <div className="relative h-[280px] border-l border-b border-gray-200 ml-8 mb-8">
            <div className="absolute -left-8 top-1/2 -rotate-90 text-xs text-gray-400 whitespace-nowrap">Accuracy (%)</div>
            <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 text-xs text-gray-400">Latency (ms)</div>
            {modelPoints.map(pt => (
              <div key={pt.name} className="absolute flex flex-col items-center group cursor-pointer" style={{ left: `${pt.x}%`, top: `${pt.y}%` }}>
                <div className={`w-4 h-4 ${pt.color} rounded-full shadow-lg ${pt.shadow} group-hover:scale-150 transition-transform`}></div>
                <span className="text-xs font-medium mt-1.5 text-gray-700">{pt.name}</span>
              </div>
            ))}
            <svg className="absolute inset-0 w-full h-full pointer-events-none" preserveAspectRatio="none" viewBox="0 0 100 100">
              <path className="text-gray-300" d="M10,90 Q30,40 90,10" fill="none" stroke="currentColor" strokeDasharray="2,2" strokeWidth="0.5"></path>
            </svg>
          </div>
        </section>

        {/* Topic Distribution */}
        <section className="col-span-12 lg:col-span-5 bg-white border border-gray-100 rounded-xl p-5 shadow-sm">
          <div className="mb-4">
            <h3 className="text-sm font-semibold text-gray-900">Topic Distribution</h3>
            <p className="text-xs text-gray-500">Conceptual heatmapping of multi-agent debate themes.</p>
          </div>
          <div className="grid grid-cols-6 grid-rows-3 gap-2 h-[280px]">
            {topics.map(t => (
              <div key={t.name} className={`${t.colSpan} ${t.color} border rounded-lg p-2 flex flex-col justify-end ${t.hoverColor} transition-all cursor-default`}>
                <span className="text-xs font-medium">{t.name}</span>
                <span className="text-xs opacity-60">{t.pct}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Terminal Output Log */}
        <section className="col-span-12 bg-white border border-gray-100 rounded-xl p-5 shadow-sm overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-400/40"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-400/40"></div>
                <div className="w-3 h-3 rounded-full bg-green-400/40"></div>
              </div>
              <h3 className="text-sm font-semibold text-gray-900">Synthesis Node Output</h3>
            </div>
            <div className="flex items-center gap-2">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              <span className="text-xs text-gray-500">System Live</span>
            </div>
          </div>
          <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm text-gray-300 overflow-x-auto max-h-[300px] overflow-y-auto">
            <div className="flex gap-6 opacity-50 mb-2 border-b border-white/10 pb-2 text-xs">
              <span className="w-24">TIMESTAMP</span>
              <span className="w-20">MODEL</span>
              <span className="w-16">STATUS</span>
              <span>OUTPUT_VECTOR_KEY</span>
            </div>
            {logs.map((log, i) => (
              <div key={i} className={`flex gap-6 py-1 hover:bg-white/5 text-xs ${i === logs.length - 1 ? 'animate-pulse' : ''}`}>
                <span className="w-24 shrink-0 text-purple-400">{log.ts}</span>
                <span className="w-20 shrink-0 text-blue-400">{log.model}</span>
                <span className="w-16 shrink-0 text-green-400">{log.status}</span>
                <span className="truncate italic opacity-60">{log.msg}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
