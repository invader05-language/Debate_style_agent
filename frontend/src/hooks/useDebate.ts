/**
 * 辩论状态管理 Hook。
 * 支持 WebSocket 实时消息、断线自动重连、轮次进度追踪。
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
  currentRound: number;
  maxRounds: number;
  createNewDebate: (topic: string) => Promise<string>;
  startDebateById: (debateId: string) => Promise<void>;
  connectWebSocket: (debateId: string) => void;
  disconnectWebSocket: () => void;
}

const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY_MS = 2000;
const MAX_DEBATE_ROUNDS = 3;

export const useDebate = (): UseDebateReturn => {
  const [debate, setDebate] = useState<Debate | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [currentRound, setCurrentRound] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const debateIdRef = useRef<string | null>(null);

  const createNewDebate = async (topic: string): Promise<string> => {
    setLoading(true);
    setError(null);
    setCurrentRound(0);
    try {
      const result = await createDebate(topic);
      setDebate(result);
      return result.id;
    } catch (err: any) {
      setError(err.message || '创建辩论失败');
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
      setError(err.message || '启动辩论失败');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = useCallback((debateId: string) => {
    debateIdRef.current = debateId;
    reconnectAttemptsRef.current = 0;

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.close();
    }

    const wsUrl = `ws://localhost:8000/ws/debate/${debateId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setWsConnected(true);
      reconnectAttemptsRef.current = 0;
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'debate_message') {
        setCurrentRound(data.round_number);
        setDebate(prev => {
          if (!prev) return prev;
          const newMessage: Message = {
            id: `msg-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
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

    ws.onerror = () => {
      setError('WebSocket 连接错误');
    };

    ws.onclose = () => {
      setWsConnected(false);
      // 自动重连
      if (
        debateIdRef.current === debateId &&
        reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS
      ) {
        reconnectAttemptsRef.current += 1;
        reconnectTimerRef.current = setTimeout(() => {
          connectWebSocket(debateId);
        }, RECONNECT_DELAY_MS);
      }
    };

    wsRef.current = ws;
  }, []);

  const disconnectWebSocket = useCallback(() => {
    debateIdRef.current = null;
    if (reconnectTimerRef.current) {
      clearTimeout(reconnectTimerRef.current);
      reconnectTimerRef.current = null;
    }
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
    currentRound,
    maxRounds: MAX_DEBATE_ROUNDS,
    createNewDebate,
    startDebateById,
    connectWebSocket,
    disconnectWebSocket
  };
};
