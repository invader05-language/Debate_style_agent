/**
 * Debate API functions.
 */

import { api } from "./client";

export interface DebateCreate {
  topic: string;
  max_rounds?: number;
  models?: Record<string, string>;
}

export interface MessageResponse {
  id: string;
  debate_id: string;
  round_number: number;
  role: string;
  content: string;
  model_used: string;
  confidence: number;
  created_at?: string;
}

export interface VerdictResponse {
  recommendation: string;
  winner: string;
  confidence: number;
  action_plan: string[];
}

export interface DebateResponse {
  id: string;
  topic: string;
  status: string;
  created_at?: string;
  completed_at?: string;
  verdict?: VerdictResponse;
  action_plan?: string[];
  messages?: MessageResponse[];
}

export interface DebateListResponse {
  debates: DebateResponse[];
  total: number;
  page: number;
  page_size: number;
}

export const debateApi = {
  create: (data: DebateCreate) => api.post<DebateResponse>("/debates", data),
  list: (page = 1, pageSize = 10) =>
    api.get<DebateListResponse>(`/debates?page=${page}&page_size=${pageSize}`),
  get: (id: string) => api.get<DebateResponse>(`/debates/${id}`),
  start: (id: string) => api.post<DebateResponse>(`/debates/${id}/start`),
};
