/**
 * Dashboard / Analytics / Tasks / Settings / FAQ / Notifications API functions.
 */

import { api } from "./client";

// Dashboard
export interface DashboardStats {
  total_debates: number;
  total_thinks: number;
  total_memories: number;
  active_models: number;
  recent_debates_7d: number;
  recent_thinks_7d: number;
  completed_debates: number;
  running_debates: number;
}

export interface ActivityItem {
  id: string;
  type: string;
  title: string;
  status: string;
  created_at?: string;
}

export const dashboardApi = {
  stats: () => api.get<DashboardStats>("/dashboard/stats"),
  recentActivity: (limit = 10) =>
    api.get<{ activities: ActivityItem[] }>(`/dashboard/recent-activity?limit=${limit}`),
};

// Analytics
export interface AnalyticsOverview {
  total_debates: number;
  completed_debates: number;
  total_thinks: number;
  total_messages: number;
  avg_rounds_per_debate: number;
  top_models: { model: string; usage_count: number }[];
}

export interface ActivityTrend {
  date: string;
  debates: number;
  tasks: number;
}

export const analyticsApi = {
  overview: () => api.get<AnalyticsOverview>("/analytics/overview"),
  activity: (days = 30) =>
    api.get<{ timeline: ActivityTrend[]; days: number }>(`/analytics/activity?days=${days}`),
};

// Tasks (history)
export interface TaskItem {
  id: string;
  type: string;
  topic: string;
  status: string;
  config?: Record<string, unknown>;
  result?: Record<string, unknown>;
  created_at?: string;
  completed_at?: string;
}

export interface TaskListResponse {
  tasks: TaskItem[];
  total: number;
  page: number;
  page_size: number;
}

export const tasksApi = {
  list: (type?: string, status?: string, page = 1, pageSize = 20) => {
    const params = new URLSearchParams();
    if (type) params.set("type", type);
    if (status) params.set("status", status);
    params.set("page", String(page));
    params.set("page_size", String(pageSize));
    return api.get<TaskListResponse>(`/tasks?${params}`);
  },
  get: (id: string) => api.get<TaskItem & { messages: unknown[] }>(`/tasks/${id}`),
  delete: (id: string) => api.delete(`/tasks/${id}`),
};

// Settings
export interface UserSettings {
  id: string;
  user_id: string;
  language: string;
  theme_mode: string;
  notifications: boolean;
  weekly_digest: boolean;
  created_at?: string;
  updated_at?: string;
}

export const settingsApi = {
  get: () => api.get<UserSettings>("/settings"),
  update: (data: Partial<UserSettings>) => api.patch<UserSettings>("/settings", data),
};

// FAQs
export interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category?: string;
  sort_order: number;
}

export const faqsApi = {
  list: (category?: string) => {
    const params = category ? `?category=${encodeURIComponent(category)}` : "";
    return api.get<{ faqs: FAQItem[]; by_category: Record<string, FAQItem[]> }>(`/faqs${params}`);
  },
};

// Notifications
export interface NotificationItem {
  id: string;
  title: string;
  message?: string;
  type: string;
  is_read: boolean;
  created_at?: string;
}

export const notificationsApi = {
  list: (isRead?: boolean, page = 1) => {
    const params = new URLSearchParams({ page: String(page) });
    if (isRead !== undefined) params.set("is_read", String(isRead));
    return api.get<{
      notifications: NotificationItem[];
      total: number;
      unread_count: number;
    }>(`/notifications?${params}`);
  },
  markRead: (id: string) => api.patch(`/notifications/${id}/read`),
  markAllRead: () => api.post("/notifications/read-all"),
};
