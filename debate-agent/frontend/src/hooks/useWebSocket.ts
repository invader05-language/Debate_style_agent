/**
 * WebSocket hook for real-time updates from the backend.
 */

import { useEffect, useRef, useCallback, useState } from "react";
import { WS_BASE } from "../api/client";

export interface WSMessage {
  type: string;
  [key: string]: unknown;
}

export function useWebSocket(taskId?: string) {
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const [messages, setMessages] = useState<WSMessage[]>([]);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const url = taskId
      ? `${WS_BASE}/ws/debate/${taskId}`
      : `${WS_BASE}/ws/global`;

    const ws = new WebSocket(url);

    ws.onopen = () => setConnected(true);
    ws.onclose = () => {
      setConnected(false);
      // Auto-reconnect after 3s
      setTimeout(() => connect(), 3000);
    };
    ws.onerror = () => ws.close();

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as WSMessage;
        setLastMessage(data);
        setMessages((prev) => [...prev, data]);
      } catch {
        // ignore non-JSON messages
      }
    };

    wsRef.current = ws;
  }, [taskId]);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setLastMessage(null);
  }, []);

  return { connected, lastMessage, messages, send, clearMessages };
}
