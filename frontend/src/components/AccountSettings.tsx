import React, { useState } from 'react';
import { 
  User, 
  Lock, 
  Languages, 
  Sun, 
  Moon, 
  Bell, 
  Key, 
  Copy, 
  Check, 
  ShieldAlert,
  Save,
  CheckCircle2,
  Cpu
} from 'lucide-react';
import { AppSettings } from '../types';

interface AccountSettingsProps {
  settings: AppSettings;
  onUpdateSettings: (newSettings: Partial<AppSettings>) => void;
}

export default function AccountSettings({ settings, onUpdateSettings }: AccountSettingsProps) {
  const [apiKeyVisible, setApiKeyVisible] = useState(false);
  const [copied, setCopied] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleCopyKey = () => {
    navigator.clipboard.writeText(settings.apiKey);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSave = () => {
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h1 className="font-bold text-2xl text-gray-900 tracking-tight font-headline-2">Account settings</h1>
        <p className="text-gray-500 font-body-md mt-1">
          Manage your interface preferences, language packs, database schemas, and developer API permissions.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Side: General preferences settings */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* General Config section */}
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-5">
            <h3 className="font-bold text-base text-gray-900 flex items-center gap-2 pb-3 border-b border-gray-100">
              <User className="w-5 h-5 text-primary" />
              General Preferences
            </h3>

            {/* Language Selection */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-gray-500 uppercase tracking-widest flex items-center gap-1">
                  <Languages className="w-3.5 h-3.5 text-gray-400" />
                  Primary Language
                </label>
                <select
                  value={settings.language}
                  onChange={(e) => onUpdateSettings({ language: e.target.value as any })}
                  className="w-full border border-gray-200 rounded-xl text-sm px-3.5 py-2.5 focus:outline-none"
                >
                  <option value="en">English (United States)</option>
                  <option value="zh-CN">Simplified Chinese (简体中文)</option>
                </select>
              </div>

              {/* Theme Settings Mode */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-gray-500 uppercase tracking-widest flex items-center gap-1">
                  <Sun className="w-3.5 h-3.5 text-gray-400" />
                  Primary Interface Theme
                </label>
                <div className="flex gap-2">
                  <button 
                    type="button"
                    onClick={() => onUpdateSettings({ themeMode: "light" })}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-xl border text-sm font-semibold transition ${
                      settings.themeMode === 'light' 
                        ? 'bg-blue-50 border-blue-200 text-blue-700 font-bold' 
                        : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Sun className="w-4 h-4" />
                    Light
                  </button>
                  <button 
                    type="button"
                    onClick={() => onUpdateSettings({ themeMode: "dark" })}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-xl border text-sm font-semibold transition ${
                      settings.themeMode === 'dark' 
                        ? 'bg-[#23005c] border-transparent text-white font-bold' 
                        : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Moon className="w-4 h-4" />
                    Dark
                  </button>
                </div>
              </div>
            </div>

            {/* Notification triggers */}
            <div className="space-y-3.5 pt-3">
              <label className="text-xs font-bold text-gray-500 uppercase tracking-widest block">Notification Matrix</label>
              
              <div className="space-y-3">
                {/* Switch 1 */}
                <div className="flex items-center justify-between">
                  <div>
                    <h5 className="font-bold text-sm text-gray-900">Push Notifications</h5>
                    <p className="text-xs text-gray-400">Trigger standard alarms when high-depth synthesize models complete compilation.</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => onUpdateSettings({ notifications: !settings.notifications })}
                    className={`w-9 h-5 rounded-full p-0.5 transition-colors ${
                      settings.notifications ? 'bg-green-500' : 'bg-gray-200'
                    }`}
                  >
                    <div className={`w-4 h-4 rounded-full bg-white shadow transition-transform ${
                      settings.notifications ? 'translate-x-4' : 'translate-x-0'
                    }`} />
                  </button>
                </div>

                {/* Switch 2 */}
                <div className="flex items-center justify-between">
                  <div>
                    <h5 className="font-bold text-sm text-gray-900">Weekly Compilation Digest</h5>
                    <p className="text-xs text-gray-400">Receive security and token cost optimization reports on active nodes via email.</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => onUpdateSettings({ weeklyDigest: !settings.weeklyDigest })}
                    className={`w-9 h-5 rounded-full p-0.5 transition-colors ${
                      settings.weeklyDigest ? 'bg-green-500' : 'bg-gray-200'
                    }`}
                  >
                    <div className={`w-4 h-4 rounded-full bg-white shadow transition-transform ${
                      settings.weeklyDigest ? 'translate-x-4' : 'translate-x-0'
                    }`} />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Key Management Segment */}
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <h3 className="font-bold text-base text-gray-900 flex items-center gap-2 pb-3 border-b border-gray-100">
              <Key className="w-5 h-5 text-primary" />
              Developer API Key Management
            </h3>

            <p className="text-xs text-gray-400 leading-relaxed">
              Use this key to authorize custom integrations with terminal clients and export synthesized logs. Keep this key secret under all circumstances.
            </p>

            <div className="flex items-center gap-2 bg-gray-50 border border-gray-100 p-3 rounded-xl">
              <input
                type={apiKeyVisible ? "text" : "password"}
                readOnly
                value={settings.apiKey}
                className="flex-1 bg-transparent border-none text-xs font-mono text-gray-700 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => setApiKeyVisible(!apiKeyVisible)}
                className="text-primary hover:underline text-xs font-semibold px-2"
              >
                {apiKeyVisible ? "Hide" : "Reveal"}
              </button>
              <button
                type="button"
                onClick={handleCopyKey}
                className="p-1.5 text-gray-400 hover:text-gray-700 bg-white border border-gray-200 rounded-lg shadow-2xs hover:shadow-sm"
                title="Copy to clipboard"
              >
                {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Action Trigger Save panel */}
          <div className="flex justify-end gap-3 items-center">
            {saveSuccess && (
              <span className="text-green-600 text-xs font-semibold flex items-center gap-1 animate-fade-in">
                <CheckCircle2 className="w-4 text-green-500" />
                Settings compiled successfully.
              </span>
            )}
            <button
              onClick={handleSave}
              className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-xl shadow-sm transition"
            >
              Save Configuration
            </button>
          </div>
        </div>

        {/* Right Side: Security Stats sidebar */}
        <div className="lg:col-span-4 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="pb-2 border-b border-gray-100 flex items-center gap-2">
            <Lock className="w-4 h-4 text-purple-600" />
            <h3 className="font-bold text-base text-gray-900">Security Guard</h3>
          </div>

          <div className="space-y-4 text-xs">
            {/* Status indicators */}
            <div className="flex justify-between items-center py-1">
              <span className="text-gray-500 font-semibold">2FA Factor Auth</span>
              <span className="text-xs font-bold text-green-600 uppercase">● Enabled</span>
            </div>

            <div className="flex justify-between items-center py-1">
              <span className="text-gray-500 font-semibold">Security Level</span>
              <span className="text-xs font-bold text-blue-600">Enterprise Standard</span>
            </div>

            <div className="flex justify-between items-center py-1 border-b border-gray-100 pb-3">
              <span className="text-gray-500 font-semibold">Quota Remaining</span>
              <span className="text-xs font-bold text-gray-900">124,500/150,000 Tokens</span>
            </div>

            {/* Alert info block */}
            <div className="p-3 bg-blue-50/50 border border-blue-100/60 rounded-xl flex gap-2.5">
              <ShieldAlert className="w-5 text-blue-600 shrink-0 mt-0.5" />
              <p className="text-[11px] text-blue-800 leading-normal font-medium">
                Last login attempted from California, USA (Oct 24, 2023 at 14:02 GMT). Verified match with secure certificate.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
