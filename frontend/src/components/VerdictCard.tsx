/**
 * Verdict card component for displaying debate verdict.
 */

import React from 'react';
import clsx from 'clsx';

interface VerdictCardProps {
  recommendation: string;
  winner: string;
  confidence: number;
  actionPlan: string[];
  onExecute?: () => void;
  onRedebate?: () => void;
}

const VerdictCard: React.FC<VerdictCardProps> = ({
  recommendation,
  winner,
  confidence,
  actionPlan,
  onExecute,
  onRedebate
}) => {
  const winnerLabel = winner === 'pro' ? '正方' : winner === 'con' ? '反方' : '平局';

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden animate-fade-in-up">
      {/* Header */}
      <div className={clsx(
        'px-6 py-4',
        winner === 'pro' && 'bg-gradient-to-r from-green-50 to-emerald-50 border-b border-green-100',
        winner === 'con' && 'bg-gradient-to-r from-red-50 to-rose-50 border-b border-red-100',
        winner === 'draw' && 'bg-gradient-to-r from-gray-50 to-slate-50 border-b border-gray-100'
      )}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={clsx(
              'w-10 h-10 rounded-full flex items-center justify-center',
              winner === 'pro' && 'bg-green-500',
              winner === 'con' && 'bg-red-500',
              winner === 'draw' && 'bg-gray-500'
            )}>
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">判决结果</h3>
              <p className="text-sm text-gray-500">辩论已完成</p>
            </div>
          </div>
          <span className={clsx(
            'px-4 py-1.5 rounded-full text-sm font-semibold',
            winner === 'pro' && 'bg-green-100 text-green-700',
            winner === 'con' && 'bg-red-100 text-red-700',
            winner === 'draw' && 'bg-gray-100 text-gray-700'
          )}>
            胜出方: {winnerLabel}
          </span>
        </div>
      </div>

      <div className="p-6 space-y-5">
        {/* Recommendation */}
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-2">推荐方案</h4>
          <p className="text-gray-800 bg-gray-50 p-4 rounded-xl text-sm leading-relaxed border border-gray-100">
            {recommendation}
          </p>
        </div>

        {/* Confidence */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-medium text-gray-500">信心度</h4>
            <span className="text-sm font-semibold text-gray-700">{(confidence * 100).toFixed(0)}%</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-2.5">
            <div
              className={clsx(
                'h-2.5 rounded-full transition-all duration-1000',
                winner === 'pro' && 'bg-gradient-to-r from-green-400 to-green-500',
                winner === 'con' && 'bg-gradient-to-r from-red-400 to-red-500',
                winner === 'draw' && 'bg-gradient-to-r from-gray-400 to-gray-500'
              )}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
        </div>

        {/* Action Plan */}
        {actionPlan && actionPlan.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-3">执行计划</h4>
            <div className="space-y-2">
              {actionPlan.map((step, index) => (
                <div key={index} className="flex items-start gap-3 bg-gray-50 rounded-lg p-3 border border-gray-100">
                  <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                    {index + 1}
                  </span>
                  <span className="text-sm text-gray-700 leading-relaxed">{step}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3 pt-2">
          {onExecute && (
            <button
              onClick={onExecute}
              className="flex-1 flex items-center justify-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all font-medium text-sm shadow-sm shadow-blue-200 hover:shadow-md"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              确认执行
            </button>
          )}
          {onRedebate && (
            <button
              onClick={onRedebate}
              className="flex-1 flex items-center justify-center gap-2 px-5 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all font-medium text-sm"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              重新辩论
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default VerdictCard;
