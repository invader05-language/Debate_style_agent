/**
 * Debate view component for displaying debate messages.
 */

import React from 'react';
import MessageBubble from './MessageBubble';

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

interface DebateViewProps {
  messages: Message[];
  loading?: boolean;
}

const DebateView: React.FC<DebateViewProps> = ({ messages, loading }) => {
  if (loading && (!messages || messages.length === 0)) {
    return (
      <div className="flex flex-col items-center justify-center p-12">
        <div className="relative">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-gray-200 border-t-blue-600"></div>
          <div className="absolute inset-0 rounded-full animate-pulse-ring border-4 border-blue-200"></div>
        </div>
        <span className="mt-4 text-gray-600 font-medium">辩论进行中...</span>
        <span className="mt-1 text-sm text-gray-400">AI 正在思考并生成论点</span>
      </div>
    );
  }

  if (!messages || messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-gray-400">
        <svg className="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <p className="text-lg font-medium">暂无辩论消息</p>
        <p className="text-sm mt-1">输入主题开始一场新的辩论</p>
      </div>
    );
  }

  // Group messages by round
  const rounds: { [key: number]: Message[] } = {};
  messages.forEach(msg => {
    if (!rounds[msg.round_number]) {
      rounds[msg.round_number] = [];
    }
    rounds[msg.round_number].push(msg);
  });

  const roundEntries = Object.entries(rounds).sort(([a], [b]) => Number(a) - Number(b));

  return (
    <div className="space-y-8 debate-scroll">
      {roundEntries.map(([roundNum, roundMessages], roundIndex) => (
        <div key={roundNum} className="animate-fade-in-up" style={{ animationDelay: `${roundIndex * 200}ms` }}>
          {/* Round separator */}
          <div className="round-separator mb-6">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 bg-gray-50 rounded-full border border-gray-200 text-sm font-medium text-gray-600">
              <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">
                {roundNum}
              </span>
              第 {roundNum} 轮辩论
            </span>
          </div>

          {/* Messages */}
          <div className="space-y-5 px-2">
            {roundMessages.map((msg, msgIndex) => (
              <MessageBubble
                key={msg.id}
                role={msg.role}
                content={msg.content}
                modelUsed={msg.model_used}
                roundNumber={msg.round_number}
                confidence={msg.confidence}
                index={msgIndex}
              />
            ))}
          </div>
        </div>
      ))}

      {/* Loading indicator for ongoing round */}
      {loading && (
        <div className="flex items-center justify-center py-4 gap-2 text-gray-400">
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
          <span className="ml-2 text-sm">AI 正在回应...</span>
        </div>
      )}
    </div>
  );
};

export default DebateView;
