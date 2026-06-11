/**
 * AI Model management API functions.
 */

import { api } from "./client";

export interface ModelCreate {
  name: string;
  provider: string;
  model_id: string;
  api_url: string;
  api_key: string;
  api_format?: string;
  max_tokens?: number;
  temperature?: number;
  is_preset?: boolean;
  icon?: string;
  color?: string;
}

export interface ModelUpdate {
  name?: string;
  provider?: string;
  model_id?: string;
  api_url?: string;
  api_key?: string;
  api_format?: string;
  max_tokens?: number;
  temperature?: number;
  is_active?: boolean;
  icon?: string;
  color?: string;
}

export interface ModelResponse {
  id: string;
  name: string;
  provider: string;
  model_id: string;
  api_url: string;
  api_format: string;
  max_tokens: number;
  temperature: number;
  is_preset: boolean;
  is_active: boolean;
  icon?: string;
  color?: string;
  last_tested_at?: string;
  last_test_status?: string;
  created_at?: string;
}

export interface ModelTestResponse {
  model_id: string;
  status: "success" | "failed";
  latency_ms?: number;
  error?: string;
  response_preview?: string;
}

export interface ModelListResponse {
  models: ModelResponse[];
  total: number;
}

export const modelsApi = {
  list: (includeInactive = false) =>
    api.get<ModelListResponse>(`/models?include_inactive=${includeInactive}`),
  create: (data: ModelCreate) => api.post<ModelResponse>("/models", data),
  get: (id: string) => api.get<ModelResponse>(`/models/${id}`),
  update: (id: string, data: ModelUpdate) =>
    api.patch<ModelResponse>(`/models/${id}`, data),
  delete: (id: string) => api.delete(`/models/${id}`),
  test: (id: string) => api.post<ModelTestResponse>(`/models/${id}/test`),
};
