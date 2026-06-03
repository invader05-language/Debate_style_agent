/**
 * Custom hook for debate state management.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { createDebate, getDebate, startDebate } from '../services/api';

interface Message {
  id: string;
  debate_id: string;
  round_number: number;
  role: string;
  content: string;
  model_used: string;
  confidence: number;
  created_at: string | null;
}

interface Verdict {
  recommendation: string;
  winner: string;
  confidence: number;
  action_plan: string[];
}

interface Debate {
  id: string;
  topic: string;
  status: string;
  created_at: string | null;
  completed_at: string | null;
  verdict: Verdict | null;
  action_plan: string[] | null;
  messages: Message[];
}

interface UseDebateReturn {
  debate: Debate | null;
  loading: boolean;
  error: string | null;
  wsConnected: boolean;
  createNewDebate: (topic: string) => Promise<string>;
  startDebateById: (debateId: string) => Promise<void>;
  connectWebSocket: (debateId: string) => void;
  disconnectWebSocket: () => void;
}

export const useDebate = (): UseDebateReturn => {
  const [debate, setDebate] = useState<Debate | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const createNewDebate = async (topic: string): Promise<string> => {
    setLoading(true);
    setError(null);
    try {
      const result = await createDebate(topic);
      setDebate(result);
      return result.id;
    } catch (err: any) {
      setError(err.message || 'Failed to create debate');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const startDebateById = async (debateId: string): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const result = await startDebate(debateId);
      setDebate(result);
    } catch (err: any) {
      setError(err.message || 'Failed to start debate');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = useCallback((debateId: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.close();
    }

    const wsUrl = `ws://localhost:8000/ws/debate/${debateId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setWsConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'debate_message') {
        setDebate(prev => {
          if (!prev) return prev;
          const newMessage: Message = {
            id: `msg-${Date.now()}`,
            debate_id: debateId,
            round_number: data.round_number,
            role: data.role,
            content: data.content,
            model_used: data.model_used,
            confidence: 0.8,
            created_at: data.timestamp
          };
          return {
            ...prev,
            messages: [...(prev.messages || []), newMessage]
          };
        });
      } else if (data.type === 'verdict') {
        setDebate(prev => {
          if (!prev) return prev;
          return {
            ...prev,
            verdict: data.verdict,
            status: 'completed'
          };
        });
      } else if (data.type === 'status_update') {
        setDebate(prev => {
          if (!prev) return prev;
          return {
            ...prev,
            status: data.status
          };
        });
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('WebSocket connection error');
    };

    ws.onclose = () => {
      setWsConnected(false);
      console.log('WebSocket disconnected');
    };

    wsRef.current = ws;
  }, []);

  const disconnectWebSocket = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => {
      disconnectWebSocket();
    };
  }, [disconnectWebSocket]);

  return {
    debate,
    loading,
    error,
    wsConnected,
    createNewDebate,
    startDebateById,
    connectWebSocket,
    disconnectWebSocket
  };
};
