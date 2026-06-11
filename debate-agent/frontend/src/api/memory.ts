/**
 * Memory API functions.
 */

import { api } from "./client";

export interface MemoryCreate {
  topic: string;
  debate_summary: string;
  outcome?: string;
  confidence?: number;
  tags?: string[];
  lessons_learned?: string[];
}

export interface MemoryUpdate {
  topic?: string;
  debate_summary?: string;
  outcome?: string;
  confidence?: number;
  tags?: string[];
  lessons_learned?: string[];
}

export interface MemoryResponse {
  id: string;
  topic: string;
  debate_summary: string;
  outcome?: string;
  confidence: number;
  tags: string[];
  lessons_learned: string[];
  created_at?: string;
}

export interface MemorySearchResponse {
  memories: MemoryResponse[];
  total: number;
  query: string;
}

export const memoryApi = {
  list: (page = 1, pageSize = 10) =>
    api.get<MemorySearchResponse>(`/memories?page=${page}&page_size=${pageSize}`),
  search: (q: string, limit = 10, useSemantic = true) =>
    api.get<MemorySearchResponse>(
      `/memories/search?q=${encodeURIComponent(q)}&limit=${limit}&use_semantic=${useSemantic}`
    ),
  get: (id: string) => api.get<MemoryResponse>(`/memories/${id}`),
  create: (data: MemoryCreate) => api.post<MemoryResponse>("/memories", data),
  update: (id: string, data: MemoryUpdate) =>
    api.patch<MemoryResponse>(`/memories/${id}`, data),
  delete: (id: string) => api.delete(`/memories/${id}`),
};
