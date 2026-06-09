import React, { useState } from 'react';
import AnalyticsTerminalPage from './AnalyticsTerminalPage';
import HelpCenterPage from './HelpCenterPage';

const stats = [
  { label: 'Debates', value: '47', icon: 'forum', color: 'from-blue-500 to-blue-600' },
  { label: 'Win Rate', value: '78%', icon: 'emoji_events', color: 'from-green-500 to-green-600' },
  { label: 'Memories', value: '126', icon: 'psychology', color: 'from-purple-500 to-purple-600' },
  { label: 'Models Used', value: '4', icon: 'smart_toy', color: 'from-orange-500 to-orange-600' },
];

const recentActivity = [
  { id: 1, type: 'debate', title: 'Microservices vs Monolith', time: '2 hours ago', status: 'completed', icon: 'forum' },
  { id: 2, type: 'think', title: 'API Gateway Design Pattern', time: '5 hours ago', status: 'completed', icon: 'psychology' },
  { id: 3, type: 'memory', title: 'Extracted: Scaling Strategies', time: '1 day ago', status: 'saved', icon: 'lightbulb' },
  { id: 4, type: 'debate', title: 'React vs Vue for Enterprise', time: '2 days ago', status: 'executed', icon: 'forum' },
  { id: 5, type: 'think', title: 'Database Sharding Analysis', time: '3 days ago', status: 'completed', icon: 'psychology' },
];

const settingsGroups = [
  {
    title: 'Account',
    items: [
      { label: 'Edit Profile', icon: 'person', desc: 'Update your name, avatar, and bio' },
      { label: 'API Keys', icon: 'key', desc: 'Manage your model API keys' },
      { label: 'Billing', icon: 'credit_card', desc: 'Pro Plan - Active until Dec 2026' },
    ],
  },
  {
    title: 'Preferences',
    items: [
      { label: 'Default Models', icon: 'tune', desc: 'Set preferred models for debate and thinking' },
      { label: 'Notifications', icon: 'notifications', desc: 'Configure email and push notifications' },
      { label: 'Theme', icon: 'palette', desc: 'Light mode - Dark mode coming soon' },
    ],
  },
  {
    title: 'Data',
    items: [
      { label: 'Export All Data', icon: 'download', desc: 'Download all debates, memories, and settings' },
      { label: 'Clear History', icon: 'delete_sweep', desc: 'Remove all session history' },
    ],
  },
];

type SubPage = 'profile' | 'analytics' | 'help';

const subNavItems: { key: SubPage; label: string; icon: string }[] = [
  { key: 'profile', label: 'Profile', icon: 'person' },
  { key: 'analytics', label: 'Analytics', icon: 'insights' },
  { key: 'help', label: 'Help Center', icon: 'help_outline' },
];

function ProfileContent() {
  const [activeTab, setActiveTab] = useState<'overview' | 'settings'>('overview');

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="h-32 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 relative">
          <div className="absolute inset-0 bg-black/10" />
        </div>
        <div className="px-6 pb-6">
          <div className="flex flex-col sm:flex-row items-center sm:items-end gap-4 -mt-12">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-3xl font-bold border-4 border-white shadow-lg flex-shrink-0">
              U
            </div>
            <div className="flex-1 text-center sm:text-left pb-1">
              <h1 className="text-xl font-bold text-gray-900">User</h1>
              <p className="text-sm text-gray-500">Pro Plan Member since Jan 2026</p>
              <div className="flex items-center justify-center sm:justify-start gap-3 mt-2">
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-blue-50 text-blue-600 text-xs font-medium">
                  <span className="material-icons text-sm">verified</span>
                  Verified
                </span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-purple-50 text-purple-600 text-xs font-medium">
                  <span className="material-icons text-sm">workspace_premium</span>
                  Pro
                </span>
              </div>
            </div>
            <button className="px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 flex items-center gap-1.5">
              <span className="material-icons text-base">edit</span>
              Edit Profile
            </button>
          </div>
        </div>
      </div>

      {/* Circular Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 text-center">
            <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${stat.color} flex items-center justify-center mx-auto mb-3`}>
              <span className="material-icons text-white text-xl">{stat.icon}</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            <p className="text-xs text-gray-500 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center gap-2 border-b border-gray-100 pb-0">
        {(['overview', 'settings'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2.5 text-sm font-medium transition-colors border-b-2 -mb-px ${
              activeTab === tab
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab === 'overview' ? 'Overview' : 'Settings'}
          </button>
        ))}
      </div>

      {activeTab === 'overview' && (
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
            <div className="px-5 py-4 border-b border-gray-50">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide flex items-center gap-2">
                <span className="material-icons text-base">history</span>
                Recent Activity
              </h2>
            </div>
            <div className="divide-y divide-gray-50">
              {recentActivity.map((item) => (
                <div key={item.id} className="px-5 py-3.5 flex items-center gap-3 hover:bg-gray-50 transition-colors">
                  <div className="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                    <span className="material-icons text-gray-500 text-lg">{item.icon}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{item.title}</p>
                    <p className="text-xs text-gray-500">{item.time}</p>
                  </div>
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${
                    item.status === 'completed' ? 'bg-green-50 text-green-600' :
                    item.status === 'executed' ? 'bg-purple-50 text-purple-600' :
                    'bg-blue-50 text-blue-600'
                  }`}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <button className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 text-left hover:shadow-md transition-all group">
              <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center mb-3 group-hover:bg-blue-100 transition-colors">
                <span className="material-icons text-blue-500">forum</span>
              </div>
              <h3 className="text-sm font-semibold text-gray-900">New Debate</h3>
              <p className="text-xs text-gray-500 mt-1">Start a multi-agent debate session</p>
            </button>
            <button className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 text-left hover:shadow-md transition-all group">
              <div className="w-10 h-10 rounded-full bg-purple-50 flex items-center justify-center mb-3 group-hover:bg-purple-100 transition-colors">
                <span className="material-icons text-purple-500">psychology</span>
              </div>
              <h3 className="text-sm font-semibold text-gray-900">Deep Think</h3>
              <p className="text-xs text-gray-500 mt-1">Start a single-agent thinking session</p>
            </button>
            <button className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 text-left hover:shadow-md transition-all group">
              <div className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center mb-3 group-hover:bg-green-100 transition-colors">
                <span className="material-icons text-green-500">download</span>
              </div>
              <h3 className="text-sm font-semibold text-gray-900">Export Data</h3>
              <p className="text-xs text-gray-500 mt-1">Download your memories and history</p>
            </button>
          </div>
        </div>
      )}

      {activeTab === 'settings' && (
        <div className="space-y-6">
          {settingsGroups.map((group) => (
            <div key={group.title} className="bg-white rounded-xl border border-gray-100 shadow-sm">
              <div className="px-5 py-4 border-b border-gray-50">
                <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">{group.title}</h2>
              </div>
              <div className="divide-y divide-gray-50">
                {group.items.map((item) => (
                  <button key={item.label} className="w-full px-5 py-4 flex items-center gap-4 hover:bg-gray-50 transition-colors text-left">
                    <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                      <span className="material-icons text-gray-500 text-lg">{item.icon}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">{item.label}</p>
                      <p className="text-xs text-gray-500">{item.desc}</p>
                    </div>
                    <span className="material-icons text-gray-300">chevron_right</span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function UserSpacePage() {
  const [activePage, setActivePage] = useState<SubPage>('profile');

  return (
    <div className="flex gap-6 animate-fade-in-up">
      {/* Internal Sidebar */}
      <aside className="w-56 flex-shrink-0">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden sticky top-24">
          {/* User Badge */}
          <div className="p-4 border-b border-gray-50 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
              U
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">User</p>
              <p className="text-[10px] text-gray-400 truncate">Pro Plan</p>
            </div>
          </div>

          {/* Sub Navigation */}
          <nav className="p-2 space-y-0.5">
            {subNavItems.map(item => (
              <button
                key={item.key}
                onClick={() => setActivePage(item.key)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium rounded-lg transition-all text-left ${
                  activePage === item.key
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <span className="material-icons text-xl">{item.icon}</span>
                <span className="truncate">{item.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </aside>

      {/* Content Area */}
      <div className="flex-1 min-w-0">
        {activePage === 'profile' && <ProfileContent />}
        {activePage === 'analytics' && <AnalyticsTerminalPage />}
        {activePage === 'help' && <HelpCenterPage />}
      </div>
    </div>
  );
}
