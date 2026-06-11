import React, { useState, useEffect } from 'react';
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
import { dashboardApi, modelsApi, tasksApi, memoryApi, settingsApi } from './api';
import type { DashboardStats, ModelResponse, TaskItem, MemoryResponse, UserSettings } from './api';
import { ActivityItem, ModelStatus, HistoryItem, MemoryInsight, AppSettings } from './types';

export default function App() {
  // Navigation
  const [activeTab, setActiveTab] = useState<string>('home');
  const [activeView, setActiveView] = useState<string>('workspace');

  // API-backed state
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [models, setModels] = useState<ModelStatus[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [memories, setMemories] = useState<MemoryInsight[]>([]);
  const [settings, setSettings] = useState<AppSettings>({
    language: "en",
    themeMode: "light",
    notifications: true,
    weeklyDigest: false,
    apiKey: ""
  });
  const [loading, setLoading] = useState(true);

  // Load all data from API on mount
  useEffect(() => {
    async function loadData() {
      try {
        const [activityRes, modelsRes, tasksRes, memoriesRes, settingsRes] = await Promise.allSettled([
          dashboardApi.recentActivity(10),
          modelsApi.list(),
          tasksApi.list(undefined, undefined, 1, 50),
          memoryApi.list(1, 50),
          settingsApi.get(),
        ]);

        if (activityRes.status === 'fulfilled') {
          const items: ActivityItem[] = activityRes.value.activities.map(a => ({
            id: a.id,
            title: a.title,
            type: a.type === 'debate' ? 'Debate' : 'Think',
            timeAgo: a.created_at ? formatTimeAgo(a.created_at) : 'Unknown',
            status: a.status === 'completed' ? 'Completed' : a.status === 'running' ? 'In Progress' : 'Failed',
          }));
          setActivities(items);
        }

        if (modelsRes.status === 'fulfilled') {
          const items: ModelStatus[] = modelsRes.value.models.map(m => ({
            id: m.id,
            name: m.name,
            provider: m.provider,
            contextWindow: `${Math.round(m.max_tokens / 1000)}k Tokens`,
            apiFormat: m.api_format,
            status: m.is_active ? 'Healthy' : 'Inactive',
            toggle: m.is_active,
            latency: m.last_test_status === 'success' ? 'OK' : 'N/A',
          }));
          setModels(items);
        }

        if (tasksRes.status === 'fulfilled') {
          const items: HistoryItem[] = tasksRes.value.tasks.map(t => ({
            id: t.id,
            title: t.topic,
            type: t.type === 'debate' ? 'DEBATE' : 'THINK',
            status: t.status === 'completed' ? 'COMPLETED' : t.status === 'running' ? 'IN PROGRESS' : 'FAILED',
            description: String(t.result?.synthesis || t.topic),
            agents: [],
            timestamp: t.created_at ? new Date(t.created_at).toLocaleString() : 'Unknown',
          }));
          setHistory(items);
        }

        if (memoriesRes.status === 'fulfilled') {
          const items: MemoryInsight[] = memoriesRes.value.memories.map(m => ({
            id: m.id,
            title: m.topic,
            sourceType: 'DEBATE',
            date: m.created_at ? new Date(m.created_at).toLocaleString() : 'Unknown',
            confidence: Math.round(m.confidence * 100),
            lessons: m.lessons_learned,
            tags: m.tags,
          }));
          setMemories(items);
        }

        if (settingsRes.status === 'fulfilled') {
          const s = settingsRes.value;
          setSettings({
            language: s.language === 'zh' ? 'zh-CN' : 'en',
            themeMode: s.theme_mode as 'light' | 'dark',
            notifications: s.notifications,
            weeklyDigest: s.weekly_digest,
            apiKey: '',
          });
        }
      } catch (e) {
        console.error('Failed to load data:', e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  function formatTimeAgo(dateStr: string): string {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  }

  // Handlers
  const handleToggleModel = async (id: string) => {
    const model = models.find(m => m.id === id);
    if (!model) return;
    const newToggle = !model.toggle;
    try {
      await modelsApi.update(id, { is_active: newToggle });
      setModels(prev => prev.map(m => m.id === id ? { ...m, toggle: newToggle, status: newToggle ? 'Healthy' : 'Inactive' } : m));
    } catch (e) {
      console.error('Toggle model failed:', e);
    }
  };

  const handleAddNewModel = async (newModel: any) => {
    try {
      const created = await modelsApi.create({
        name: newModel.name,
        provider: newModel.provider || 'Unknown',
        model_id: newModel.id || 'custom',
        api_url: newModel.apiUrl || 'https://api.example.com',
        api_key: newModel.apiKey || '',
        api_format: 'openai',
      });
      setModels(prev => [...prev, {
        id: created.id,
        name: created.name,
        provider: created.provider,
        contextWindow: `${Math.round(created.max_tokens / 1000)}k Tokens`,
        apiFormat: created.api_format,
        status: 'Healthy',
        toggle: true,
      }]);
    } catch (e) {
      console.error('Add model failed:', e);
    }
  };

  const handleDeleteSession = async (id: string) => {
    if (!confirm("Are you sure you want to delete this session?")) return;
    try {
      await tasksApi.delete(id);
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (e) {
      console.error('Delete session failed:', e);
    }
  };

  const handleAddMemory = (newMemory: MemoryInsight) => {
    setMemories(prev => [newMemory, ...prev]);
  };

  const handleDeleteMemory = async (id: string) => {
    try {
      await memoryApi.delete(id);
      setMemories(prev => prev.filter(m => m.id !== id));
    } catch (e) {
      console.error('Delete memory failed:', e);
    }
  };

  const handleUpdateSettings = async (newSettings: Partial<AppSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
    try {
      await settingsApi.update({
        language: newSettings.language === 'zh-CN' ? 'zh' : newSettings.language === 'en' ? 'en' : undefined,
        theme_mode: newSettings.themeMode,
        notifications: newSettings.notifications,
        weekly_digest: newSettings.weeklyDigest,
      });
    } catch (e) {
      console.error('Update settings failed:', e);
    }
  };

  const handleNewSessionTrigger = () => {
    setActiveTab('debate');
    setActiveView('workspace');
  };

  // Render
  const renderMainContent = () => {
    if (activeView === 'analytics') return <AnalyticsPanel />;
    if (activeView === 'terminal') return <TerminalPanel />;
    if (activeView === 'settings') return <AccountSettings settings={settings} onUpdateSettings={handleUpdateSettings} />;
    if (activeView === 'help') return <HelpCenter />;

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
        return <DebateWorkspace models={models} />;
      case 'think':
        return <ThinkWorkspace />;
      case 'models':
        return <ModelManagement models={models} onToggleModel={handleToggleModel} onAddNewModel={handleAddNewModel} />;
      case 'history':
        return <HistoryAndLogs history={history} onDeleteSession={handleDeleteSession} />;
      case 'memory':
        return <MemoryBank memories={memories} onAddMemory={handleAddMemory} onDeleteMemory={handleDeleteMemory} />;
      default:
        return <div className="p-12 text-center text-gray-400">Loading workspace...</div>;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-gray-500 font-medium">Loading platform data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen font-sans ${settings.themeMode === 'dark' ? 'dark-theme-mode bg-surface text-on-surface' : 'bg-gray-50 text-gray-800'}`}>
      <Header
        activeTab={activeTab}
        onTabChange={(tab) => { setActiveTab(tab); setActiveView('workspace'); }}
        onViewChange={setActiveView}
      />
      <div className="flex pt-16">
        <Sidebar
          activeView={activeView}
          onViewChange={(view) => {
            setActiveView(view);
            if (view === 'workspace' && activeTab === 'home') setActiveTab('home');
          }}
          onNewSession={handleNewSessionTrigger}
        />
        <main className="flex-1 ml-64 p-8 min-h-[calc(100vh-64px)] relative">
          {renderMainContent()}
        </main>
      </div>
    </div>
  );
}
