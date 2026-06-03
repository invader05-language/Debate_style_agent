/**
 * API service for Multi-AI Debate Agent.
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Debate API
export const createDebate = async (topic: string, maxRounds: number = 3) => {
  const response = await api.post('/api/debates', { topic, max_rounds: maxRounds });
  return response.data;
};

export const listDebates = async (page: number = 1, pageSize: number = 10) => {
  const response = await api.get(`/api/debates?page=${page}&page_size=${pageSize}`);
  return response.data;
};

export const getDebate = async (debateId: string) => {
  const response = await api.get(`/api/debates/${debateId}`);
  return response.data;
};

export const startDebate = async (debateId: string) => {
  const response = await api.post(`/api/debates/${debateId}/start`);
  return response.data;
};

export const executeDebate = async (debateId: string) => {
  const response = await api.post(`/api/debates/${debateId}/execute`);
  return response.data;
};

// Memory API
export const listMemories = async (page: number = 1, pageSize: number = 10) => {
  const response = await api.get(`/api/memories?page=${page}&page_size=${pageSize}`);
  return response.data;
};

export const searchMemories = async (query: string, limit: number = 10) => {
  const response = await api.get(`/api/memories/search?q=${query}&limit=${limit}`);
  return response.data;
};

export const getMemory = async (memoryId: string) => {
  const response = await api.get(`/api/memories/${memoryId}`);
  return response.data;
};

// Execution API
export const getExecution = async (executionId: string) => {
  const response = await api.get(`/api/executions/${executionId}`);
  return response.data;
};

export default api;
