import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import HomeDashboard from './components/HomeDashboard';
import DebateWorkspace from './components/DebateWorkspace';
import ThinkWorkspace from './components/ThinkWorkspace';
import ModelManagement from './components/ModelManagement';
import HistoryAndLogs from './components/HistoryAndLogs';
import MemoryBank from './components/MemoryBank';
import AnalyticsPanel from './components/AnalyticsPanel';
import TerminalPanel from './components/TerminalPanel';
import AccountSettings from './components/AccountSettings';
import HelpCenter from './components/HelpCenter';
import { 
  INITIAL_ACTIVITIES, 
  INITIAL_MODELS, 
  INITIAL_HISTORY, 
  INITIAL_MEMORIES 
} from './data';
import { ActivityItem, ModelStatus, HistoryItem, MemoryInsight, AppSettings } from './types';

export default function App() {
  // Navigation Tabs & Views
  const [activeTab, setActiveTab] = useState<string>('home');
  const [activeView, setActiveView] = useState<string>('workspace');

  // Shared platform records state
  const [activities, setActivities] = useState<ActivityItem[]>(INITIAL_ACTIVITIES);
  const [models, setModels] = useState<ModelStatus[]>(INITIAL_MODELS);
  const [history, setHistory] = useState<HistoryItem[]>(INITIAL_HISTORY);
  const [memories, setMemories] = useState<MemoryInsight[]>(INITIAL_MEMORIES);
  const [settings, setSettings] = useState<AppSettings>({
    language: "en",
    themeMode: "light",
    notifications: true,
    weeklyDigest: false,
    apiKey: "as_live_5fa79b87ea418a2036b933cc4efb07a1aa"
  });

  // Action actions callbacks
  const handleToggleModel = (id: string) => {
    setModels(prev => prev.map(m => m.id === id ? { ...m, toggle: !m.toggle, status: !m.toggle ? "Healthy" : "Inactive" } : m));
  };

  const handleAddNewModel = (newModel: ModelStatus) => {
    setModels(prev => [...prev, newModel]);
    setActivities(prev => [{
      id: `act-${Date.now()}`,
      title: `Added Model: ${newModel.name}`,
      type: "Think",
      agentName: "Registry System",
      timeAgo: "Just now",
      status: "Completed"
    }, ...prev]);
  };

  const handleDeleteSession = (id: string) => {
    if (confirm("Are you sure you want to prune this session log permanently?")) {
      setHistory(prev => prev.filter(item => item.id !== id));
    }
  };

  const handleAddMemory = (newMemory: MemoryInsight) => {
    setMemories(prev => [newMemory, ...prev]);
  };

  const handleDeleteMemory = (id: string) => {
    setMemories(prev => prev.filter(m => m.id !== id));
  };

  const handleUpdateSettings = (newSettings: Partial<AppSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  const handleNewSessionTrigger = () => {
    setActiveTab('debate');
    setActiveView('workspace');
    alert("New dialectical debate session initialized. Configure topics on the screen.");
  };

  // Render view dispatcher
  const renderMainContent = () => {
    // If we clicked a sidebar link other than workspace, override top tabs!
    if (activeView === 'analytics') {
      return <AnalyticsPanel />;
    }
    if (activeView === 'terminal') {
      return <TerminalPanel />;
    }
    if (activeView === 'settings') {
      return <AccountSettings settings={settings} onUpdateSettings={handleUpdateSettings} />;
    }
    if (activeView === 'help') {
      return <HelpCenter />;
    }

    // Standard Tab Rendering under Core Workspace
    switch (activeTab) {
      case 'home':
        return (
          <HomeDashboard 
            activities={activities} 
            models={models}
            onSelectDebate={() => setActiveTab('debate')}
            onSelectThink={() => setActiveTab('think')}
            onViewAllHistory={() => setActiveTab('history')}
            onViewModelStatus={() => setActiveTab('models')}
          />
        );
      case 'debate':
        return <DebateWorkspace />;
      case 'think':
        return <ThinkWorkspace />;
      case 'models':
        return (
          <ModelManagement 
            models={models} 
            onToggleModel={handleToggleModel} 
            onAddNewModel={handleAddNewModel} 
          />
        );
      case 'history':
        return <HistoryAndLogs history={history} onDeleteSession={handleDeleteSession} />;
      case 'memory':
        return (
          <MemoryBank 
            memories={memories} 
            onAddMemory={handleAddMemory} 
            onDeleteMemory={handleDeleteMemory} 
          />
        );
      default:
        return <div className="p-12 text-center text-gray-400">Loading workspace components...</div>;
    }
  };

  return (
    <div className={`min-h-screen font-sans ${settings.themeMode === 'dark' ? 'dark-theme-mode bg-surface text-on-surface' : 'bg-gray-50 text-gray-800'}`}>
      {/* Top Header */}
      <Header 
        activeTab={activeTab} 
        onTabChange={(tab) => {
          setActiveTab(tab);
          setActiveView('workspace'); // click top tabs forces focus back to core workspace
        }} 
        onViewChange={setActiveView}
      />

      {/* Main Structural Frame */}
      <div className="flex pt-16">
        {/* Left Side menu Bar */}
        <Sidebar 
          activeView={activeView} 
          onViewChange={(view) => {
            setActiveView(view);
            // If workspace is clicked, fallback to active tab or home
            if (view === 'workspace' && activeTab === 'home') {
              setActiveTab('home');
            }
          }} 
          onNewSession={handleNewSessionTrigger}
        />

        {/* Dynamic page container */}
        <main className="flex-1 ml-64 p-8 min-h-[calc(100vh-64px)] relative">
          {renderMainContent()}
        </main>
      </div>
    </div>
  );
}
