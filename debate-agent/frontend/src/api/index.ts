/**
 * API module — re-exports all API functions and types.
 */

export { api, API_BASE, WS_BASE } from "./client";
export { debateApi } from "./debate";
export type {
  DebateCreate,
  DebateResponse,
  DebateListResponse,
  MessageResponse,
  VerdictResponse,
} from "./debate";
export { thinkApi } from "./think";
export type {
  ThinkCreate,
  ThinkResponse,
  ThinkListResponse,
  ThinkMessageResponse,
} from "./think";
export { modelsApi } from "./models";
export type {
  ModelCreate,
  ModelUpdate,
  ModelResponse,
  ModelTestResponse,
  ModelListResponse,
} from "./models";
export { memoryApi } from "./memory";
export type {
  MemoryCreate,
  MemoryUpdate,
  MemoryResponse,
  MemorySearchResponse,
} from "./memory";
export {
  dashboardApi,
  analyticsApi,
  tasksApi,
  settingsApi,
  faqsApi,
  notificationsApi,
} from "./dashboard";
export type {
  DashboardStats,
  ActivityItem,
  AnalyticsOverview,
  ActivityTrend,
  TaskItem,
  TaskListResponse,
  UserSettings,
  FAQItem,
  NotificationItem,
} from "./dashboard";
