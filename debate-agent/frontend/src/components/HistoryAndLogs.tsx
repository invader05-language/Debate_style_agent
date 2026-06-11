import React, { useState } from 'react';
import { 
  Search, 
  Filter, 
  ChevronRight, 
  Clock, 
  MessageSquare, 
  Brain, 
  Scale, 
  X,
  FileText,
  Trash2,
  ListFilter
} from 'lucide-react';
import { HistoryItem } from '../types';

interface HistoryAndLogsProps {
  history: HistoryItem[];
  onDeleteSession: (id: string) => void;
}

export default function HistoryAndLogs({ history, onDeleteSession }: HistoryAndLogsProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [selectedSession, setSelectedSession] = useState<HistoryItem | null>(null);

  // Filter history items
  const filteredHistory = history.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          item.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === "ALL" || item.type === typeFilter;
    const matchesStatus = statusFilter === "ALL" || item.status === statusFilter;
    return matchesSearch && matchesType && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Session History Audit</h1>
        <p className="text-gray-500 font-body-md mt-1">
          Review, restore, and analyze previously generated multi-agent debate sessions and recursive think trails.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row gap-4 items-center justify-between">
        {/* Search */}
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search past sessions by keyword..."
            className="w-full text-sm bg-gray-50 border border-gray-200 rounded-xl pl-10 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white transition"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3 w-full md:w-auto items-center">
          <div className="flex items-center gap-1.5 text-xs font-bold text-gray-400 uppercase tracking-wider">
            <ListFilter className="w-4 h-4 text-gray-400" />
            <span>Filters:</span>
          </div>

          {/* Type Select */}
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="border border-gray-200 rounded-lg text-xs font-semibold text-gray-600 px-3 py-2 bg-none focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
          >
            <option value="ALL">All Types</option>
            <option value="DEBATE">Debate</option>
            <option value="THINK">Think</option>
            <option value="SYNTHESIS">Synthesis</option>
          </select>

          {/* Status Select */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-200 rounded-lg text-xs font-semibold text-gray-600 px-3 py-2 bg-none focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
          >
            <option value="ALL">All Statuses</option>
            <option value="COMPLETED">Completed</option>
            <option value="IN PROGRESS">In Progress</option>
            <option value="FAILED">Failed</option>
          </select>
        </div>
      </div>

      {/* Session Audit Table List */}
      <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Session Topic</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Configuration</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Engine Nodes</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Created</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3.5 text-xs font-bold text-gray-400 uppercase tracking-wider text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredHistory.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-400 text-sm">
                    No session logs found matching your filters.
                  </td>
                </tr>
              ) : (
                filteredHistory.map((item) => {
                  const iconMap = {
                    "DEBATE": <MessageSquare className="w-4 h-4 text-blue-600" />,
                    "THINK": <Brain className="w-4 h-4 text-purple-600" />,
                    "SYNTHESIS": <Scale className="w-4 h-4 text-amber-600" />
                  };

                  return (
                    <tr 
                      key={item.id} 
                      className="hover:bg-gray-50/40 transition-colors group cursor-pointer"
                      onClick={() => setSelectedSession(item)}
                    >
                      {/* Name */}
                      <td className="px-6 py-4.5">
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                            item.type === 'DEBATE' 
                              ? 'bg-blue-50' 
                              : item.type === 'THINK' 
                              ? 'bg-purple-50' 
                              : 'bg-amber-50'
                          }`}>
                            {iconMap[item.type]}
                          </div>
                          <div>
                            <h5 className="font-bold text-sm text-gray-900 group-hover:text-primary transition-colors">
                              {item.title}
                            </h5>
                            <p className="text-2xs text-gray-400 font-medium">Session ID: {item.id}</p>
                          </div>
                        </div>
                      </td>

                      {/* Type */}
                      <td className="px-6 py-4.5 font-bold text-xs uppercase tracking-wide text-gray-600">
                        {item.type}
                      </td>

                      {/* Engine Nodes */}
                      <td className="px-6 py-4.5 font-medium text-xs text-gray-500">
                        {item.agents.join(", ")}
                      </td>

                      {/* Timestamp */}
                      <td className="px-6 py-4.5 text-xs text-gray-500">
                        {item.timestamp}
                      </td>

                      {/* Status */}
                      <td className="px-6 py-4.5">
                        <span className={`text-2xs font-semibold px-2 py-0.5 rounded-full ${
                          item.status === 'COMPLETED' 
                            ? 'bg-green-50 text-green-700 border border-green-100' 
                            : item.status === 'IN PROGRESS' 
                            ? 'bg-blue-50 text-blue-700 border border-blue-100' 
                            : 'bg-red-50 text-red-700 border border-red-100'
                        }`}>
                          {item.status}
                        </span>
                      </td>

                      {/* Actions */}
                      <td className="px-6 py-4.5 text-right" onClick={(e) => e.stopPropagation()}>
                        <div className="flex justify-end gap-3.5 items-center">
                          <button 
                            onClick={() => setSelectedSession(item)}
                            className="text-primary hover:underline text-xs font-semibold flex items-center gap-1 cursor-pointer"
                          >
                            Inspect Log
                            <ChevronRight className="w-4 h-4" />
                          </button>
                          <button 
                            onClick={() => onDeleteSession(item.id)}
                            className="text-gray-400 hover:text-red-600 p-1 rounded transition"
                            title="Delete Log"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Popup for Inspection */}
      {selectedSession && (
        <div className="fixed inset-0 bg-black/65 flex items-center justify-center p-4 z-50 animate-fade-in backdrop-blur-xs">
          <div className="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl animate-scale-up">
            {/* Header */}
            <div className={`p-6 text-white flex justify-between items-start ${
              selectedSession.type === 'DEBATE' 
                ? 'bg-blue-700' 
                : selectedSession.type === 'THINK' 
                ? 'bg-purple-900' 
                : 'bg-amber-700'
            }`}>
              <div>
                <span className="text-2xs font-bold bg-white/20 px-2 py-0.5 rounded uppercase tracking-wider">
                  {selectedSession.type} Log Summary
                </span>
                <h3 className="font-bold text-lg mt-1 tracking-tight">{selectedSession.title}</h3>
              </div>
              <button 
                onClick={() => setSelectedSession(null)}
                className="p-1 rounded-lg bg-white/10 hover:bg-white/20 text-white transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Body Info */}
            <div className="p-6 space-y-6 max-h-[450px] overflow-y-auto">
              {/* Params */}
              <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl text-xs">
                <div>
                  <p className="text-2xs font-semibold text-gray-400 uppercase tracking-widest">Selected Nodes</p>
                  <p className="font-semibold text-gray-800 mt-1">{selectedSession.agents.join(", ")}</p>
                </div>
                <div>
                  <p className="text-2xs font-semibold text-gray-400 uppercase tracking-widest">Executed Timestamp</p>
                  <p className="font-semibold text-gray-800 mt-1">{selectedSession.timestamp}</p>
                </div>
              </div>

              {/* Description */}
              <div className="space-y-2">
                <h4 className="font-bold text-xs text-gray-500 uppercase tracking-widest">Premise Context Description</h4>
                <p className="text-sm text-gray-700 font-body-md leading-relaxed bg-gray-50 border border-gray-100 p-3.5 rounded-xl">
                  {selectedSession.description}
                </p>
              </div>

              {/* Complete transcript logs simulations */}
              <div className="space-y-2.5">
                <h4 className="font-bold text-xs text-gray-500 uppercase tracking-widest">Cognitive Core Trail Transcript</h4>
                
                <div className="h-40 overflow-y-auto bg-gray-900 text-green-400 text-3xs font-mono p-4 rounded-xl space-y-2">
                  <p className="text-gray-500 font-bold">&gt; Initializing virtual execution environment...</p>
                  <p className="text-gray-500">&gt; Booting hyper-parameter registers...</p>
                  <p className="text-white font-semibold">&gt; Core active node: {selectedSession.agents[0] || 'AuraSynth-Omega'}</p>
                  <p className="leading-relaxed">
                    &gt; Triggered prompt: "Refine architectural model based on state isolation. Output constraints."
                  </p>
                  <p className="text-amber-300">&gt; Validation compiler outputs complete agreement with 98% confidence.</p>
                  <p className="text-gray-500">&gt; Termination sequence complete. Session finalized successfully.</p>
                </div>
              </div>
            </div>

            {/* Footer buttons */}
            <div className="p-4 border-t border-gray-100 bg-gray-50 flex justify-end gap-3.5">
              <button 
                onClick={() => setSelectedSession(null)}
                className="px-4 py-2 border border-gray-200 bg-white hover:bg-gray-150 text-gray-700 font-semibold text-xs rounded-xl transition cursor-pointer"
              >
                Close Summary
              </button>
              <button 
                onClick={() => {
                  alert("Restoring debate session parameter nodes to active workspace...");
                  setSelectedSession(null);
                }}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-xl transition cursor-pointer"
              >
                Restore Session State
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
