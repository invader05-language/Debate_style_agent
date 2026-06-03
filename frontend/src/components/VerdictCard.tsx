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
  const winnerColor = winner === 'pro' ? 'green' : winner === 'con' ? 'red' : 'gray';

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          判决结果
        </h3>
        <span className={clsx(
          'px-3 py-1 rounded-full text-sm font-medium',
          winner === 'pro' && 'bg-green-100 text-green-800',
          winner === 'con' && 'bg-red-100 text-red-800',
          winner === 'draw' && 'bg-gray-100 text-gray-800'
        )}>
          胜出方: {winnerLabel}
        </span>
      </div>

      {/* Recommendation */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">
          推荐方案
        </h4>
        <p className="text-gray-800 bg-gray-50 p-3 rounded-lg">
          {recommendation}
        </p>
      </div>

      {/* Confidence */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-700">
            信心度
          </h4>
          <span className="text-sm text-gray-500">
            {(confidence * 100).toFixed(0)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={clsx(
              'h-3 rounded-full',
              winner === 'pro' && 'bg-green-500',
              winner === 'con' && 'bg-red-500',
              winner === 'draw' && 'bg-gray-500'
            )}
            style={{ width: `${confidence * 100}%` }}
          />
        </div>
      </div>

      {/* Action Plan */}
      {actionPlan && actionPlan.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            执行计划
          </h4>
          <ol className="list-decimal list-inside space-y-1">
            {actionPlan.map((step, index) => (
              <li key={index} className="text-gray-800">
                {step}
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Actions */}
      <div className="flex space-x-3 mt-6">
        {onExecute && (
          <button
            onClick={onExecute}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            确认执行
          </button>
        )}
        {onRedebate && (
          <button
            onClick={onRedebate}
            className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            重新辩论
          </button>
        )}
      </div>
    </div>
  );
};

export default VerdictCard;
