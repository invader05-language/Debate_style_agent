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

const statusConfig: Record<string, { label: string; color: string; dot: string; bg: string }> = {
  pending: { label: '等待执行', color: 'text-gray-600', dot: 'bg-gray-400', bg: 'bg-gray-50' },
  running: { label: '执行中...', color: 'text-blue-600', dot: 'bg-blue-500', bg: 'bg-blue-50' },
  success: { label: '执行成功', color: 'text-green-600', dot: 'bg-green-500', bg: 'bg-green-50' },
  failed: { label: '执行失败', color: 'text-red-600', dot: 'bg-red-500', bg: 'bg-red-50' }
};

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
  const config = statusConfig[status] || statusConfig.pending;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden animate-fade-in-up">
      {/* Header */}
      <div className={clsx('px-6 py-4 border-b border-gray-100', config.bg)}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={clsx(
              'w-10 h-10 rounded-full flex items-center justify-center',
              isPending && 'bg-gray-200',
              isRunning && 'bg-blue-200',
              isSuccess && 'bg-green-200',
              isFailed && 'bg-red-200'
            )}>
              {isRunning ? (
                <svg className="animate-spin w-5 h-5 text-blue-600" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              ) : isSuccess ? (
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : isFailed ? (
                <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">代码执行</h3>
              <span className={clsx('text-sm', config.color)}>{config.label}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-4">
        {/* Code Generated */}
        {codeGenerated && (
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-2">生成的代码</h4>
            <pre className="bg-gray-900 text-green-400 p-4 rounded-xl overflow-x-auto text-sm font-mono leading-relaxed">
              {codeGenerated}
            </pre>
          </div>
        )}

        {/* Execution Result */}
        {executionResult && (
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-2">执行结果</h4>
            <pre className={clsx(
              'p-4 rounded-xl overflow-x-auto text-sm font-mono leading-relaxed',
              isSuccess ? 'bg-green-50 text-green-800 border border-green-100' : 'bg-gray-50 text-gray-800 border border-gray-100'
            )}>
              {executionResult}
            </pre>
          </div>
        )}

        {/* Error Message */}
        {errorMessage && (
          <div>
            <h4 className="text-sm font-medium text-red-600 mb-2">错误信息</h4>
            <pre className="bg-red-50 text-red-700 p-4 rounded-xl overflow-x-auto text-sm font-mono leading-relaxed border border-red-100">
              {errorMessage}
            </pre>
          </div>
        )}

        {/* Loading State */}
        {isRunning && (
          <div className="flex items-center justify-center py-6 gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
            <span className="ml-2 text-sm text-gray-500">代码执行中...</span>
          </div>
        )}

        {/* Execute Button */}
        {isPending && onExecute && (
          <button
            onClick={onExecute}
            className="w-full flex items-center justify-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all font-medium text-sm shadow-sm shadow-blue-200 hover:shadow-md"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            执行代码
          </button>
        )}
      </div>
    </div>
  );
};

export default ExecutionPanel;
