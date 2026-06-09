/**
 * Round progress stepper component for debate rounds.
 */

import React from 'react';
import clsx from 'clsx';

interface RoundProgressProps {
  currentRound: number;
  maxRounds: number;
  status: string;
}

const RoundProgress: React.FC<RoundProgressProps> = ({
  currentRound,
  maxRounds,
  status
}) => {
  const rounds = Array.from({ length: maxRounds }, (_, i) => i + 1);

  return (
    <div className="flex items-center justify-center space-x-2 py-4">
      {rounds.map((round, index) => {
        const isCompleted = round < currentRound || status === 'completed';
        const isCurrent = round === currentRound && status === 'running';
        const isPending = round > currentRound && status !== 'completed';

        return (
          <React.Fragment key={round}>
            {/* Round circle */}
            <div className="flex flex-col items-center">
              <div className={clsx(
                'w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300',
                isCompleted && 'bg-green-500 text-white shadow-md shadow-green-200',
                isCurrent && 'bg-blue-500 text-white shadow-md shadow-blue-200 animate-pulse-ring',
                isPending && 'bg-gray-200 text-gray-500'
              )}>
                {isCompleted ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  round
                )}
              </div>
              <span className={clsx(
                'text-xs mt-1 font-medium',
                isCompleted && 'text-green-600',
                isCurrent && 'text-blue-600',
                isPending && 'text-gray-400'
              )}>
                第{round}轮
              </span>
            </div>

            {/* Connector line */}
            {index < rounds.length - 1 && (
              <div className={clsx(
                'w-16 h-0.5 mt-[-20px] transition-all duration-300',
                round < currentRound || status === 'completed'
                  ? 'bg-green-400'
                  : round === currentRound && status === 'running'
                    ? 'bg-gradient-to-r from-blue-400 to-gray-200'
                    : 'bg-gray-200'
              )} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default RoundProgress;
