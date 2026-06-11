/**
 * Think engine API functions.
 */

import { api } from "./client";

export interface ThinkCreate {
  topic: string;
  depth?: "quick" | "standard" | "deep";
  models?: string[];
}

export interface ThinkMessageResponse {
  id: string;
  task_id: string;
  model_id?: string;
  role: string;
  round_number: number;
  content: string;
  structured?: Record<string, unknown>;
  created_at?: string;
}

export interface ThinkResponse {
  id: string;
  topic: string;
  status: string;
  depth?: string;
  created_at?: string;
  completed_at?: string;
  synthesis?: string;
  insights?: string[];
  messages?: ThinkMessageResponse[];
}

export interface ThinkListResponse {
  sessions: ThinkResponse[];
  total: number;
  page: number;
  page_size: number;
}

export const thinkApi = {
  create: (data: ThinkCreate) => api.post<ThinkResponse>("/think", data),
  list: (page = 1, pageSize = 10) =>
    api.get<ThinkListResponse>(`/think?page=${page}&page_size=${pageSize}`),
  get: (id: string) => api.get<ThinkResponse>(`/think/${id}`),
  start: (id: string) => api.post<ThinkResponse>(`/think/${id}/start`),
};
