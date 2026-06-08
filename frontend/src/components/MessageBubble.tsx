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
  index?: number;
}

const roleConfig: Record<string, { label: string; avatar: string; bgColor: string; borderColor: string; textColor: string; badgeBg: string }> = {
  pro: {
    label: '正方',
    avatar: 'A',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    textColor: 'text-green-700',
    badgeBg: 'bg-green-100'
  },
  con: {
    label: '反方',
    avatar: 'B',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    textColor: 'text-red-700',
    badgeBg: 'bg-red-100'
  },
  judge: {
    label: '裁判',
    avatar: 'J',
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
    textColor: 'text-yellow-700',
    badgeBg: 'bg-yellow-100'
  }
};

const MessageBubble: React.FC<MessageBubbleProps> = ({
  role,
  content,
  modelUsed,
  roundNumber,
  confidence,
  index = 0
}) => {
  const isPro = role === 'pro';
  const isCon = role === 'con';
  const isJudge = role === 'judge';
  const config = roleConfig[role] || roleConfig.judge;

  return (
    <div className={clsx(
      'flex gap-3 animate-fade-in-up',
      isPro ? 'justify-start' : 'justify-end'
    )} style={{ animationDelay: `${index * 100}ms` }}>
      {/* Avatar - left side for pro */}
      {isPro && (
        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 flex items-center justify-center text-white font-bold shadow-md">
          {config.avatar}
        </div>
      )}

      {/* Bubble */}
      <div className={clsx(
        'max-w-[75%] rounded-2xl p-4 shadow-sm transition-all hover:shadow-md',
        config.bgColor,
        `border ${config.borderColor}`,
        isPro ? 'rounded-tl-sm' : 'rounded-tr-sm'
      )}>
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className={clsx(
              'px-2 py-0.5 rounded-full text-xs font-semibold',
              config.badgeBg,
              config.textColor
            )}>
              {config.label}
            </span>
            <span className="text-xs text-gray-500 font-mono">
              {modelUsed}
            </span>
          </div>
          <span className="text-xs text-gray-400">
            R{roundNumber}
          </span>
        </div>

        {/* Content */}
        <div className="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">
          {content}
        </div>

        {/* Confidence bar */}
        <div className="mt-3 flex items-center gap-2">
          <span className="text-xs text-gray-400">信心度</span>
          <div className="flex-1 bg-gray-200 rounded-full h-1.5 max-w-[120px]">
            <div
              className={clsx(
                'h-1.5 rounded-full transition-all duration-500',
                isPro && 'bg-green-500',
                isCon && 'bg-red-500',
                isJudge && 'bg-yellow-500'
              )}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <span className="text-xs text-gray-500 font-mono">
            {(confidence * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {/* Avatar - right side for con/judge */}
      {!isPro && (
        <div className={clsx(
          'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-white font-bold shadow-md',
          isCon ? 'bg-red-500' : 'bg-yellow-500'
        )}>
          {config.avatar}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
