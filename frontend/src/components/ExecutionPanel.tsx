/**
 * Execution panel component for displaying code execution results.
 */

import React from 'react';
import clsx from 'clsx';

interface ExecutionPanelProps {
  status: string;
  codeGenerated?: string;
  executionResult?: string;
  errorMessage?: string;
  onExecute?: () => void;
}

const ExecutionPanel: React.FC<ExecutionPanelProps> = ({
  status,
  codeGenerated,
  executionResult,
  errorMessage,
  onExecute
}) => {
  const isPending = status === 'pending';
  const isRunning = status === 'running';
  const isSuccess = status === 'success';
  const isFailed = status === 'failed';

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          代码执行
        </h3>
        <span className={clsx(
          'px-3 py-1 rounded-full text-sm font-medium',
          isPending && 'bg-gray-100 text-gray-800',
          isRunning && 'bg-blue-100 text-blue-800',
          isSuccess && 'bg-green-100 text-green-800',
          isFailed && 'bg-red-100 text-red-800'
        )}>
          {isPending && '等待执行'}
          {isRunning && '执行中...'}
          {isSuccess && '执行成功'}
          {isFailed && '执行失败'}
        </span>
      </div>

      {/* Code Generated */}
      {codeGenerated && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            生成的代码
          </h4>
          <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm">
            {codeGenerated}
          </pre>
        </div>
      )}

      {/* Execution Result */}
      {executionResult && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            执行结果
          </h4>
          <pre className={clsx(
            'p-4 rounded-lg overflow-x-auto text-sm',
            isSuccess ? 'bg-green-50 text-green-800' : 'bg-gray-50 text-gray-800'
          )}>
            {executionResult}
          </pre>
        </div>
      )}

      {/* Error Message */}
      {errorMessage && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-red-700 mb-2">
            错误信息
          </h4>
          <pre className="bg-red-50 text-red-800 p-4 rounded-lg overflow-x-auto text-sm">
            {errorMessage}
          </pre>
        </div>
      )}

      {/* Loading State */}
      {isRunning && (
        <div className="flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">代码执行中...</span>
        </div>
      )}

      {/* Execute Button */}
      {isPending && onExecute && (
        <button
          onClick={onExecute}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          执行代码
        </button>
      )}
    </div>
  );
};

export default ExecutionPanel;
