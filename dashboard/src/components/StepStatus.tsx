import React from 'react';
import { PipelineStep } from '../types';

interface StepStatusProps {
  step: PipelineStep;
  isExpanded: boolean;
  onToggle: () => void;
}

const StepStatus: React.FC<StepStatusProps> = ({ step, isExpanded, onToggle }) => {
  const getStatusIcon = (status: PipelineStep['status']) => {
    switch (status) {
      case 'pending':
        return '🟡';
      case 'running':
        return '🟢';
      case 'success':
        return '✅';
      case 'failed':
        return '❌';
      default:
        return '⚪';
    }
  };

  const getStatusColor = (status: PipelineStep['status']) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-600 bg-yellow-50';
      case 'running':
        return 'text-blue-600 bg-blue-50';
      case 'success':
        return 'text-green-600 bg-green-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const formatDuration = () => {
    if (!step.started_at) return '';
    const start = new Date(step.started_at);
    const end = step.completed_at ? new Date(step.completed_at) : new Date();
    const duration = Math.floor((end.getTime() - start.getTime()) / 1000);
    return `${duration}s`;
  };

  return (
    <div className="border rounded-lg p-4 mb-4 bg-white shadow-sm">
      <div 
        className="flex items-center justify-between cursor-pointer"
        onClick={onToggle}
      >
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{getStatusIcon(step.status)}</span>
          <div>
            <h3 className="font-semibold text-gray-900">{step.name}</h3>
            <p className="text-sm text-gray-600 font-mono">{step.run}</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(step.status)}`}>
            {step.status.toUpperCase()}
          </span>
          {formatDuration() && (
            <span className="text-sm text-gray-500">{formatDuration()}</span>
          )}
          <span className="text-gray-400">
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>

      {isExpanded && (
        <div className="mt-4 pt-4 border-t">
          <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm max-h-64 overflow-y-auto">
            {step.logs.length > 0 ? (
              step.logs.map((log, index) => (
                <div key={index} className="mb-1">
                  {log}
                </div>
              ))
            ) : (
              <div className="text-gray-500 italic">No logs yet...</div>
            )}
            {step.status === 'running' && (
              <div className="animate-pulse">▋</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default StepStatus;