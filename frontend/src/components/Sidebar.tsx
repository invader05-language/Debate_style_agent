import React from 'react';
import { 
  Plus, 
  Layout, 
  BarChart3, 
  Terminal as TerminalIcon, 
  Settings as SettingsIcon, 
  HelpCircle, 
  LogOut, 
  User 
} from 'lucide-react';

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  onNewSession: () => void;
}

export default function Sidebar({ activeView, onViewChange, onNewSession }: SidebarProps) {
  const menuItems = [
    { id: 'workspace', label: 'Workspace', icon: Layout },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'terminal', label: 'Terminal', icon: TerminalIcon },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
    { id: 'help', label: 'Help', icon: HelpCircle },
  ];

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col justify-between h-[calc(100vh-64px)] fixed left-0 top-[64px] z-20">
      {/* Top Part */}
      <div className="p-4 flex flex-col gap-6">
        {/* User Context */}
        <div className="flex items-center gap-3 px-2 py-1">
          <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center text-primary border border-blue-100">
            <User className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-semibold text-sm text-gray-900">AI Architect</h4>
            <p className="text-xs text-on-surface-variant font-medium">Pro Plan</p>
          </div>
        </div>

        {/* Action Button */}
        <button 
          onClick={onNewSession}
          className="w-full flex items-center justify-center gap-2 bg-[#2170e4] hover:bg-opacity-90 text-white font-medium text-sm py-2.5 px-4 rounded-lg shadow-sm transition-all hover:scale-[1.02] active:scale-[0.98]"
        >
          <Plus className="w-4 h-4" />
          New Session
        </button>

        {/* Navigation List */}
        <nav className="flex flex-col gap-1.5">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onViewChange(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive 
                    ? 'bg-secondary-container text-white shadow-sm' 
                    : 'text-on-surface-variant hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-on-surface-variant'}`} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Part */}
      <div className="p-4 border-t border-gray-100">
        <button 
          onClick={() => alert('Simulating Logout. Session state has been reset.')}
          className="w-full flex items-center gap-3 px-3 py-2.5 text-red-600 hover:bg-red-50 hover:text-red-700 rounded-lg text-sm font-medium transition-colors"
        >
          <LogOut className="w-4 h-4 text-red-500" />
          Logout
        </button>
      </div>
    </aside>
  );
}
