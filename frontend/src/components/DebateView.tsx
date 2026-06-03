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
  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">辩论进行中...</span>
      </div>
    );
  }

  if (!messages || messages.length === 0) {
    return (
      <div className="text-center p-8 text-gray-500">
        暂无辩论消息
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

  return (
    <div className="space-y-6">
      {Object.entries(rounds).map(([roundNum, roundMessages]) => (
        <div key={roundNum} className="border rounded-lg p-4 bg-gray-50">
          <h3 className="text-sm font-medium text-gray-500 mb-4">
            第 {roundNum} 轮
          </h3>
          <div className="space-y-4">
            {roundMessages.map((msg) => (
              <MessageBubble
                key={msg.id}
                role={msg.role}
                content={msg.content}
                modelUsed={msg.model_used}
                roundNumber={msg.round_number}
                confidence={msg.confidence}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default DebateView;
