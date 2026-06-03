/**
 * Message bubble component for debate messages.
 */

import React from 'react';
import clsx from 'clsx';

interface MessageBubbleProps {
  role: string;
  content: string;
  modelUsed: string;
  roundNumber: number;
  confidence: number;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({
  role,
  content,
  modelUsed,
  roundNumber,
  confidence
}) => {
  const isPro = role === 'pro';
  const isCon = role === 'con';
  const isJudge = role === 'judge';

  const roleLabel = isPro ? '正方' : isCon ? '反方' : '裁判';
  const roleColor = isPro ? 'green' : isCon ? 'red' : 'yellow';

  return (
    <div className={clsx(
      'flex',
      isPro ? 'justify-start' : 'justify-end'
    )}>
      <div className={clsx(
        'max-w-[80%] rounded-lg p-4',
        isPro && 'bg-green-50 border border-green-200',
        isCon && 'bg-red-50 border border-red-200',
        isJudge && 'bg-yellow-50 border border-yellow-200'
      )}>
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <span className={clsx(
            'text-sm font-medium',
            isPro && 'text-green-700',
            isCon && 'text-red-700',
            isJudge && 'text-yellow-700'
          )}>
            {roleLabel} ({modelUsed})
          </span>
          <span className="text-xs text-gray-500">
            第 {roundNumber} 轮
          </span>
        </div>

        {/* Content */}
        <p className="text-gray-800 whitespace-pre-wrap">
          {content}
        </p>

        {/* Confidence */}
        <div className="mt-2 flex items-center">
          <span className="text-xs text-gray-500">信心度:</span>
          <div className="ml-2 w-20 bg-gray-200 rounded-full h-2">
            <div
              className={clsx(
                'h-2 rounded-full',
                isPro && 'bg-green-500',
                isCon && 'bg-red-500',
                isJudge && 'bg-yellow-500'
              )}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <span className="ml-2 text-xs text-gray-500">
            {(confidence * 100).toFixed(0)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
