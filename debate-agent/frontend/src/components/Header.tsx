import React from 'react';
import { Settings, Sparkles } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  onViewChange: (view: string) => void;
}

export default function Header({ activeTab, onTabChange, onViewChange }: HeaderProps) {
  const tabs = [
    { id: 'home', label: 'Home' },
    { id: 'debate', label: 'Debate' },
    { id: 'think', label: 'Think' },
    { id: 'models', label: 'Models' },
    { id: 'history', label: 'History' },
    { id: 'memory', label: 'Memory' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 shadow-sm flex items-center justify-between px-6 z-30">
      {/* Brand Logo */}
      <button 
        onClick={() => {
          onTabChange('home');
          onViewChange('workspace');
        }}
        className="flex items-center gap-2 group transition-all"
      >
        <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-primary to-secondary flex items-center justify-center shadow-md shadow-blue-100 group-hover:scale-105 transition-transform">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <span className="font-bold text-xl bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent font-headline-2 tracking-tight">
          AuraSynth
        </span>
      </button>

      {/* Center Tabs Navigation */}
      <nav className="hidden md:flex items-center gap-8 h-full">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                onTabChange(tab.id);
                onViewChange('workspace'); // Workspace is the core hub container
              }}
              className={`h-full flex items-center px-1 border-b-2 text-sm font-medium transition-all ${
                isActive 
                  ? 'border-primary text-primary font-semibold' 
                  : 'border-transparent text-gray-500 hover:text-gray-900 hover:border-gray-200'
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Settings button */}
        <button 
          onClick={() => onViewChange('settings')}
          className="p-2 text-gray-500 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
          title="Account Settings"
        >
          <Settings className="w-5 h-5" />
        </button>

        {/* User Avatar */}
        <div 
          onClick={() => onViewChange('settings')}
          className="w-9 h-9 rounded-full bg-[#e9ddff] text-[#23005c] border border-[#d0bcff] hover:brightness-95 cursor-pointer flex items-center justify-center font-bold text-xs shadow-sm"
          title="View profile"
        >
          JD
        </div>
      </div>
    </header>
  );
}
