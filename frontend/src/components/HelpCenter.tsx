import React, { useState } from 'react';
import { 
  Search, 
  HelpCircle, 
  BookOpen, 
  MessageSquare, 
  Github, 
  Download, 
  ArrowRight,
  ChevronDown,
  ChevronUp,
  ExternalLink
} from 'lucide-react';
import { FAQS } from '../data';

export default function HelpCenter() {
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  // Filter FAQs based on query
  const filteredFaqs = FAQS.filter(faq => 
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleFaq = (index: number) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const categories = [
    { title: "Quickstart", desc: "Connect your first LLM node", items: "4 articles" },
    { title: "Dialectics Guide", desc: "Customize multi-agent debate parameters", items: "6 articles" },
    { title: "Reasoning Models", desc: "Deconstruct Chain-of-Thought logs", items: "5 articles" },
    { title: "Security Protocols", desc: "Rotate keys and lock datasets", items: "3 articles" },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h1 className="font-bold text-2xl text-gray-900 tracking-tight font-headline-2">Explore Center & FAQS</h1>
        <p className="text-gray-500 font-body-md mt-1">
          Learn how to customize cognitive layouts, orchestrate multi-agent prompts, and monitor routing pipelines.
        </p>
      </div>

      {/* Large search panel */}
      <div className="bg-gradient-to-tr from-[#23005c] to-indigo-900 rounded-2xl p-8 text-center text-white space-y-4 shadow-md">
        <h2 className="font-bold text-xl tracking-tight leading-none">How can we assist your AI architect team today?</h2>
        <div className="relative max-w-xl mx-auto">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-indigo-300" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search FAQs, documentation, or tutorial blueprints..."
            className="w-full text-sm bg-white/10 hover:bg-white/15 focus:bg-white text-white focus:text-gray-905 border border-white/10 focus:border-transparent rounded-xl pl-12 pr-4 py-3 focus:outline-none transition-all placeholder:text-indigo-200"
          />
        </div>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {categories.map((cat, i) => (
          <div key={i} className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm hover:border-purple-200 hover:shadow-md transition cursor-pointer flex flex-col justify-between">
            <div className="space-y-2">
              <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
                <BookOpen className="w-4 h-4" />
              </div>
              <h4 className="font-bold text-sm text-gray-900">{cat.title}</h4>
              <p className="text-xs text-gray-400 leading-normal">{cat.desc}</p>
            </div>
            <span className="text-[10px] text-primary/80 font-bold uppercase tracking-wider block mt-4">{cat.items}</span>
          </div>
        ))}
      </div>

      {/* FAQs list accordion */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
        <h3 className="font-bold text-base text-gray-900 flex items-center gap-2 pb-2 border-b border-gray-100">
          <HelpCircle className="w-5 h-5 text-purple-600 animate-pulse" />
          Frequently Asked Questions (FAQS)
        </h3>

        <div className="divide-y divide-gray-100">
          {filteredFaqs.map((faq, index) => {
            const isExpanded = expandedIndex === index;
            return (
              <div key={index} className="py-4 first:pt-0 last:pb-0 font-medium">
                <button
                  onClick={() => toggleFaq(index)}
                  className="w-full flex justify-between items-center text-left text-sm font-semibold text-gray-900 hover:text-primary transition"
                >
                  <span>{faq.question}</span>
                  {isExpanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                </button>
                {isExpanded && (
                  <p className="mt-2.5 text-xs text-gray-550 leading-relaxed pl-1">
                    {faq.answer}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Support Resources links panel */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Support links card */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-base text-gray-900">Support Communities</h3>
            <p className="text-xs text-gray-400">Join other AI architects in constructing distributed systems.</p>
          </div>

          <div className="space-y-3 pt-2">
            <a 
              href="https://discord.gg/invite"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-3 bg-gray-50 rounded-xl hover:bg-gray-100/70 border border-gray-100 transition"
            >
              <div className="flex items-center gap-3">
                <MessageSquare className="w-4 h-4 text-blue-500" />
                <span className="text-xs font-semibold text-gray-700">Official Discord Server</span>
              </div>
              <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
            </a>

            <a 
              href="https://github.com/repository" 
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-3 bg-gray-50 rounded-xl hover:bg-gray-100/70 border border-gray-100 transition"
            >
              <div className="flex items-center gap-3">
                <Github className="w-4 h-4 text-gray-900" />
                <span className="text-xs font-semibold text-gray-700">Explore Open-Source Repos</span>
              </div>
              <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
            </a>
          </div>
        </div>

        {/* Featured resource panel */}
        <div className="bg-purple-50/50 border border-purple-100 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-start mb-3">
              <span className="text-3xs font-bold text-purple-700 bg-purple-100 px-2.5 py-0.5 rounded-full tracking-wider uppercase">
                Featured Resource
              </span>
              <Download className="w-4 h-4 text-purple-600 animate-bounce" />
            </div>

            <h4 className="font-bold text-sm text-purple-900 leading-tight">
              AuraSynth Multi-Agent Dialectic Compilers: Benchmark Whitepaper (PDF)
            </h4>

            <p className="text-xs text-purple-700 leading-relaxed mt-2">
              Our comprehensive research paper on cognitive alignment rates, memory routing caches, and token conservation algorithms.
            </p>
          </div>

          <button 
            onClick={() => alert("Downloading the technical specifications whitepaper... (Simulated payload)")}
            className="w-full flex items-center justify-center gap-2 bg-[#23005c] hover:bg-[#340087] text-white font-semibold text-xs py-2.5 px-4 rounded-xl shadow-sm transition"
          >
            Download Whitepaper
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
