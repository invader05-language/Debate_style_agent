import React, { useState } from 'react';
import { 
  Plus, 
  Brain, 
  Check, 
  Trash2, 
  Filter, 
  Image,
  Award,
  BookOpen
} from 'lucide-react';
import { MemoryInsight } from '../types';

interface MemoryBankProps {
  memories: MemoryInsight[];
  onAddMemory: (newItem: MemoryInsight) => void;
  onDeleteMemory: (id: string) => void;
}

export default function MemoryBank({ memories, onAddMemory, onDeleteMemory }: MemoryBankProps) {
  const [activeTag, setActiveTag] = useState("ALL");
  const [showAddForm, setShowAddForm] = useState(false);

  // Form State
  const [newTitle, setNewTitle] = useState("");
  const [newSource, setNewSource] = useState<"DEBATE" | "THINK" | "SYNTHESIS">("SYNTHESIS");
  const [newConfidence, setNewConfidence] = useState(90);
  const [newLessonsText, setNewLessonsText] = useState("");
  const [newTagsText, setNewTagsText] = useState("");

  const tags = ["ALL", "Auth", "Security", "AI", "Search", "Cryptography", "Frontend", "Styling"];

  const handleCreateMemory = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    const lessons = newLessonsText
      .split("\n")
      .map(l => l.trim())
      .filter(l => l.length > 0);
    
    const parsedTags = newTagsText
      .split(",")
      .map(t => t.trim())
      .filter(t => t.length > 0);

    const newItem: MemoryInsight = {
      id: `mem-${Date.now()}`,
      title: newTitle,
      sourceType: newSource,
      date: new Date().toLocaleDateString() + " • Live Commit",
      confidence: newConfidence,
      lessons: lessons.length > 0 ? lessons : ["Verify alignment on target endpoints."],
      tags: parsedTags.length > 0 ? parsedTags : ["Manual"]
    };

    onAddMemory(newItem);
    setNewTitle("");
    setNewLessonsText("");
    setNewTagsText("");
    setShowAddForm(false);
  };

  // Filter list
  const filteredMemories = memories.filter((mem) => {
    if (activeTag === "ALL") return true;
    return mem.tags.some(t => t.toLowerCase() === activeTag.toLowerCase());
  });

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="font-bold text-2xl text-gray-900 tracking-tight">Synthesized Memory Bank</h1>
          <p className="text-gray-500 font-body-md mt-1">
            Aggregated insights, rules, and best-practice blueprints distilled from multi-model dialectics and independent thinking.
          </p>
        </div>

        <button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center gap-2 bg-[#2170e4] hover:bg-opacity-95 text-white font-semibold text-sm py-2.5 px-4 rounded-xl shadow-sm transition"
        >
          <Plus className="w-4 h-4" />
          {showAddForm ? "Close Form" : "Commit Lesson"}
        </button>
      </div>

      {/* Add Custom Lesson Form panel */}
      {showAddForm && (
        <form 
          onSubmit={handleCreateMemory} 
          className="bg-white border border-purple-100 rounded-2xl p-6 shadow-md space-y-4 animate-fade-in"
        >
          <h3 className="font-bold text-sm text-gray-900 uppercase tracking-wide">Manual Insight Commit</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Title */}
            <div className="space-y-1.5 animate-pulse-once">
              <label className="text-xs font-semibold text-gray-700">Insight Topic / Title</label>
              <input
                type="text"
                required
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="e.g. Session Token Revocation Scheme"
                className="w-full text-sm border border-gray-200 rounded-xl px-3.5 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            {/* Source Type & Confidence */}
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-gray-700">Source Type</label>
                <select
                  value={newSource}
                  onChange={(e) => setNewSource(e.target.value as any)}
                  className="w-full border border-gray-200 rounded-xl text-sm px-3 py-2 focus:outline-none"
                >
                  <option value="DEBATE">Debate</option>
                  <option value="THINK">Think</option>
                  <option value="SYNTHESIS">Synthesis</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-gray-700">Confidence (%)</label>
                <input
                  type="number"
                  min="50"
                  max="100"
                  value={newConfidence}
                  onChange={(e) => setNewConfidence(parseInt(e.target.value))}
                  className="w-full text-sm border border-gray-200 rounded-xl px-3 py-2 focus:outline-none"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Lessons Bullet points */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-gray-700">Lessons Learned (One per line)</label>
              <textarea
                rows={3}
                value={newLessonsText}
                onChange={(e) => setNewLessonsText(e.target.value)}
                placeholder="Rule 1: Never trust user client context.&#10;Rule 2: Restrict database transaction rate limits."
                className="w-full text-sm border border-gray-200 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            {/* Tags comma sep */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-gray-700">Tags (Comma separated)</label>
              <input
                type="text"
                value={newTagsText}
                onChange={(e) => setNewTagsText(e.target.value)}
                placeholder="Security, Auth, Architecture"
                className="w-full text-sm border border-gray-200 rounded-xl px-3.5 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <button
            type="submit"
            className="px-5 py-2 bg-purple-700 hover:bg-purple-800 text-white font-semibold text-xs rounded-xl shadow-sm transition"
          >
            Commit Lesson
          </button>
        </form>
      )}

      {/* Filter Category Tabs row */}
      <div className="flex flex-wrap gap-2 pb-2 border-b border-gray-100">
        {tags.map((tag) => (
          <button
            key={tag}
            onClick={() => setActiveTag(tag)}
            className={`text-xs font-semibold px-3 py-1.5 rounded-lg border transition ${
              activeTag === tag 
                ? 'bg-[#23005c] hover:bg-[#340087] text-white border-transparent shadow' 
                : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
            }`}
          >
            {tag}
          </button>
        ))}
      </div>

      {/* Memories Grid list */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredMemories.map((mem) => (
          <div 
            key={mem.id} 
            className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between"
          >
            <div className="space-y-3">
              {/* Top Row meta */}
              <div className="flex justify-between items-center text-xs pb-2.5 border-b border-gray-50">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
                  <span className="font-bold text-gray-500 font-headline-2 text-2xs uppercase tracking-wider">
                    {mem.sourceType} • {mem.date}
                  </span>
                </div>

                <span className="font-semibold text-[#6b38d4] text-xs">
                  Confidence: {mem.confidence}%
                </span>
              </div>

              {/* Title heading */}
              <h3 className="font-bold text-sm text-gray-900 tracking-tight">
                {mem.title}
              </h3>

              {/* Bullet notes */}
              <ul className="space-y-2">
                {mem.lessons.map((lesson, index) => (
                  <li key={index} className="flex gap-2 text-xs text-gray-650 font-medium leading-relaxed">
                    <Check className="w-4 h-4 text-green-500 shrink-0 mt-0.5" />
                    <span>{lesson}</span>
                  </li>
                ))}
              </ul>

              {/* Dynamic Diagram Image hotlink if present */}
              {mem.imageUrl && (
                <div className="mt-4 border border-gray-100 rounded-xl overflow-hidden shadow-inner bg-slate-50">
                  <img
                    src={mem.imageUrl}
                    alt={`${mem.title} Schematic Diagram`}
                    referrerPolicy="no-referrer"
                    className="w-full h-auto object-contain max-h-[160px] opacity-95 hover:opacity-100 transition-opacity"
                  />
                  <div className="px-3 py-1.5 bg-gray-50 text-[10px] text-gray-400 font-mono text-center border-t border-gray-100">
                    Schematic: hotlinked SVG diagram node
                  </div>
                </div>
              )}
            </div>

            {/* Bottom tag list & actions */}
            <div className="flex justify-between items-center pt-3.5 border-t border-gray-50">
              <div className="flex gap-1">
                {mem.tags.map((t) => (
                  <span 
                    key={t}
                    className="text-[10px] font-bold px-2 py-0.5 bg-blue-50 text-blue-700 rounded-md tracking-wider uppercase"
                  >
                    #{t}
                  </span>
                ))}
              </div>

              <button
                onClick={() => onDeleteMemory(mem.id)}
                className="text-gray-400 hover:text-red-600 transition p-1"
                title="Prune Memory insight"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
