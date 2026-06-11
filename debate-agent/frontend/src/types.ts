export interface DebateRound {
  id: string;
  agent: string;
  role: "PROPONENT" | "OPPONENT" | "SYNTHESIZER";
  text: string;
  confidence: number;
  depth?: number;
  timestamp: string;
}

export interface ActivityItem {
  id: string;
  title: string;
  type: "Debate" | "Think" | "Synthesis";
  agentsCount?: number;
  agentName?: string;
  timeAgo: string;
  status: "Completed" | "In Progress" | "Failed";
}

export interface ModelStatus {
  id: string;
  name: string;
  provider: string;
  contextWindow: string;
  apiFormat: string;
  status: "Online" | "Offline" | "Healthy" | "Inactive";
  toggle: boolean;
  latency?: string;
}

export interface HistoryItem {
  id: string;
  title: string;
  type: "DEBATE" | "THINK" | "SYNTHESIS";
  status: "COMPLETED" | "IN PROGRESS" | "FAILED";
  description: string;
  agents: string[];
  timestamp: string;
}

export interface MemoryInsight {
  id: string;
  title: string;
  sourceType: "DEBATE" | "THINK" | "SYNTHESIS";
  date: string;
  confidence: number;
  lessons: string[];
  tags: string[];
  imageUrl?: string;
}

export interface AppSettings {
  language: "zh-CN" | "en";
  themeMode: "light" | "dark";
  notifications: boolean;
  weeklyDigest: boolean;
  apiKey: string;
}
