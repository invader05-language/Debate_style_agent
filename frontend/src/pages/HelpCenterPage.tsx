import React, { useState } from 'react';

const categories = [
  { label: 'Getting Started', desc: 'Essential setup guides for new users', icon: 'rocket_launch', color: 'bg-blue-50 text-blue-600' },
  { label: 'Debate Mode Guide', desc: 'Configuring multi-agent dialectics', icon: 'forum', color: 'bg-purple-50 text-purple-600' },
  { label: 'Model Configuration', desc: 'Fine-tuning AI personalities and limits', icon: 'memory', color: 'bg-yellow-50 text-yellow-600' },
  { label: 'Memory & Insights', desc: 'Understanding persistent knowledge bases', icon: 'psychology', color: 'bg-green-50 text-green-600' },
  { label: 'Execution Engine', desc: 'Running generated code in sandboxed environments', icon: 'terminal', color: 'bg-red-50 text-red-600' },
  { label: 'Billing & Plans', desc: 'Subscription management and usage limits', icon: 'credit_card', color: 'bg-orange-50 text-orange-600' },
];

const faqs = [
  { q: 'How do I switch between different LLM models?', a: 'You can switch models in the Workspace sidebar or through the Model Configuration settings. Each model can be assigned to specific roles (Pro, Con, Judge) independently.' },
  { q: 'Can I export my debate transcripts?', a: 'Yes, navigate to History, select the session you want to export, and click the Export button. Supported formats include JSON, Markdown, and PDF.' },
  { q: 'How does the Memory system work?', a: 'AuraSynth automatically extracts key insights, consensus points, and lessons learned from each debate session. These are stored in your Memory Bank and can be searched or referenced in future sessions.' },
  { q: 'What is the difference between Debate and Think modes?', a: 'Debate mode pits multiple AI models against each other with opposing viewpoints. Think mode uses a single model with recursive self-correction and Chain-of-Thought processing for deep analysis.' },
  { q: 'Is my data secure?', a: 'All data is encrypted at rest and in transit. We use isolated sandboxed environments for code execution, and your API keys are stored with enterprise-grade encryption.' },
];

export default function HelpCenterPage() {
  const [search, setSearch] = useState('');
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in-up">
      {/* System Status Banner */}
      <div className="flex items-center justify-between px-4 py-2 bg-green-50 border border-green-100 rounded-lg">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span className="text-sm font-medium text-green-700">All AI services are operational</span>
        </div>
        <button className="text-xs text-blue-600 hover:underline">View System Status</button>
      </div>

      {/* Hero Search Section */}
      <div className="text-center py-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">How can we help you today?</h1>
        <p className="text-sm text-gray-500 mb-6">Search our documentation, guides, and community support resources.</p>
        <div className="relative max-w-2xl mx-auto">
          <span className="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">search</span>
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search for articles, features, or error codes..."
            className="w-full pl-12 pr-4 py-3.5 bg-white rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm text-sm"
          />
        </div>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {categories.map(cat => (
          <button
            key={cat.label}
            className="group p-5 bg-white border border-gray-100 rounded-xl hover:shadow-md hover:border-blue-200 transition-all flex flex-col items-center text-center"
          >
            <div className={`w-12 h-12 rounded-lg ${cat.color} flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
              <span className="material-icons text-xl">{cat.icon}</span>
            </div>
            <h3 className="text-sm font-semibold text-gray-900 mb-1">{cat.label}</h3>
            <p className="text-xs text-gray-500">{cat.desc}</p>
          </button>
        ))}
      </div>

      {/* FAQs */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <span className="material-icons text-blue-500">live_help</span>
          <h2 className="text-lg font-semibold text-gray-900">Top Frequently Asked Questions</h2>
        </div>
        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className={`bg-white border rounded-xl overflow-hidden transition-all duration-300 ${
                openFaq === i ? 'border-blue-200 shadow-md' : 'border-gray-100'
              }`}
            >
              <button
                onClick={() => setOpenFaq(openFaq === i ? null : i)}
                className="w-full flex items-center justify-between p-4 text-left"
              >
                <span className={`text-sm font-medium ${openFaq === i ? 'text-blue-600' : 'text-gray-900'}`}>
                  {faq.q}
                </span>
                <span className={`material-icons text-gray-400 transition-transform ${openFaq === i ? 'rotate-180' : ''}`}>
                  expand_more
                </span>
              </button>
              {openFaq === i && (
                <div className="px-4 pb-4 pt-0 text-sm text-gray-600 border-t border-gray-50">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Featured Resource */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center bg-gray-900 text-white rounded-2xl overflow-hidden">
        <div className="md:col-span-5 p-8">
          <span className="inline-block px-3 py-1 bg-blue-500 text-white text-xs font-medium rounded-full mb-3">Featured Resource</span>
          <h2 className="text-xl font-bold mb-2">Master the Art of Multi-Agent Interaction</h2>
          <p className="text-sm text-gray-400 mb-4">Download our comprehensive whitepaper on orchestrating hierarchical AI debates for complex problem-solving.</p>
          <button className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-300 hover:underline">
            Get the Guide <span className="material-icons text-sm">arrow_forward</span>
          </button>
        </div>
        <div className="md:col-span-7 h-48 md:h-72 relative bg-gradient-to-br from-blue-500/20 to-purple-500/20">
          <div className="absolute inset-0 bg-gradient-to-r from-gray-900 via-transparent to-transparent"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="material-icons text-white/10" style={{ fontSize: '120px' }}>auto_awesome</span>
          </div>
        </div>
      </div>

      {/* Footer Links */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 py-6 border-t border-gray-100">
        <div className="text-center md:text-left">
          <h3 className="text-sm font-semibold text-gray-900">AuraSynth</h3>
          <p className="text-xs text-gray-500">&copy; 2024 AuraSynth Technologies. All rights reserved.</p>
        </div>
        <div className="flex gap-4">
          <button className="text-xs text-gray-500 hover:text-blue-500">Privacy Policy</button>
          <button className="text-xs text-gray-500 hover:text-blue-500">Terms of Service</button>
          <button className="text-xs text-gray-500 hover:text-blue-500">SLA</button>
        </div>
      </div>
    </div>
  );
}
