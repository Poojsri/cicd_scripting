import React from 'react';
import { motion } from 'framer-motion';
import { Play, CheckCircle, XCircle, Clock, Terminal } from 'lucide-react';
import { PipelineStep } from '../types';

interface StepStatusProps {
  step: PipelineStep;
  isExpanded: boolean;
  onToggle: () => void;
  stepIndex: number;
}

const StepStatus: React.FC<StepStatusProps> = ({ step, isExpanded, onToggle, stepIndex }) => {
  const getStatusIcon = (status: PipelineStep['status']) => {
    const iconClass = "w-7 h-7 text-icon-contrast";
    switch (status) {
      case 'pending':
        return <Clock className={`${iconClass} text-white drop-shadow-lg`} />;
      case 'running':
        return <Play className={`${iconClass} text-white drop-shadow-lg animate-pulse`} />;
      case 'success':
        return <CheckCircle className={`${iconClass} text-white drop-shadow-lg`} />;
      case 'failed':
        return <XCircle className={`${iconClass} text-white drop-shadow-lg`} />;
      default:
        return <Clock className={`${iconClass} text-gray-600`} />;
    }
  };

  const getStatusClass = (status: PipelineStep['status']) => {
    switch (status) {
      case 'pending':
        return 'status-pending';
      case 'running':
        return 'status-running';
      case 'success':
        return 'status-success';
      case 'failed':
        return 'status-failed';
      default:
        return 'bg-gray-100';
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
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: stepIndex * 0.1 }}
      className="relative mb-6"
    >
      {/* Timeline connector */}
      {stepIndex > 0 && (
        <div className="absolute left-7 -top-6 w-0.5 h-6 bg-gradient-to-b from-[#78B9B5] to-transparent"></div>
      )}
      
      <div className="glass card-hover rounded-2xl p-6 border border-[#78B9B5]/30">
        <div 
          className="flex items-center justify-between cursor-pointer"
          onClick={onToggle}
        >
          <div className="flex items-center space-x-4">
            {/* Status indicator with better visibility */}
            <div className={`p-4 rounded-full ${getStatusClass(step.status)} flex items-center justify-center shadow-lg`}>
              {getStatusIcon(step.status)}
            </div>
            
            <div className="flex-1">
              <div className="flex items-center space-x-3">
                <h3 className="text-xl font-bold text-high-contrast">{step.name}</h3>
                <span className="text-sm text-white bg-[#065084] px-3 py-1 rounded-full font-mono font-semibold">
                  Step {stepIndex + 1}
                </span>
              </div>
              <div className="flex items-center space-x-2 mt-2">
                <Terminal className="w-5 h-5 text-[#0F828C] drop-shadow-sm" />
                <p className="text-medium-contrast font-mono text-sm bg-[#78B9B5]/20 px-3 py-2 rounded-lg border border-[#78B9B5]/30">
                  {step.run}
                </p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Status badge with better contrast */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              className={`px-4 py-2 rounded-full text-white font-bold text-sm shadow-lg ${getStatusClass(step.status)}`}
            >
              {step.status.toUpperCase()}
            </motion.div>
            
            {formatDuration() && (
              <div className="text-sm text-white bg-[#065084] px-3 py-1 rounded-full font-mono font-semibold">
                ⏱️ {formatDuration()}
              </div>
            )}
            
            {/* Expand/collapse indicator */}
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.3 }}
              className="text-[#0F828C] text-xl font-bold drop-shadow-sm"
            >
              ▼
            </motion.div>
          </div>
        </div>

        {/* Progress bar for running steps */}
        {step.status === 'running' && (
          <div className="mt-4 w-full bg-[#78B9B5]/30 rounded-full h-3 overflow-hidden shadow-inner">
            <div className="progress-bar h-full rounded-full"></div>
          </div>
        )}

        {/* Expandable logs section */}
        <motion.div
          initial={false}
          animate={{ height: isExpanded ? 'auto' : 0, opacity: isExpanded ? 1 : 0 }}
          transition={{ duration: 0.3 }}
          className="overflow-hidden"
        >
          {isExpanded && (
            <motion.div
              initial={{ y: -20 }}
              animate={{ y: 0 }}
              className="mt-6 pt-6 border-t border-[#78B9B5]/30"
            >
              <div className="bg-[#1a1a2e] text-[#78B9B5] p-4 rounded-xl font-mono text-sm max-h-80 overflow-y-auto terminal-scrollbar relative shadow-inner">
                {/* Terminal header */}
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-[#320A6B]/50">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-[#500073] rounded-full shadow-sm"></div>
                    <div className="w-3 h-3 bg-[#320A6B] rounded-full shadow-sm"></div>
                    <div className="w-3 h-3 bg-[#0F828C] rounded-full shadow-sm"></div>
                  </div>
                  <span className="text-[#78B9B5]/70 text-xs font-semibold">Terminal Output</span>
                </div>
                
                {step.logs.length > 0 ? (
                  step.logs.map((log, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="mb-2 flex items-start space-x-2"
                    >
                      <span className="text-[#78B9B5]/60 text-xs mt-1 select-none font-mono w-8 text-right">
                        {index + 1}
                      </span>
                      <span className="text-[#78B9B5]/80 mt-1 select-none">$</span>
                      <span className="flex-1 text-[#78B9B5]">{log}</span>
                    </motion.div>
                  ))
                ) : (
                  <div className="text-[#78B9B5]/60 italic flex items-center space-x-2 py-4">
                    <div className="animate-pulse">⚪</div>
                    <span>Waiting for output...</span>
                  </div>
                )}
                
                {step.status === 'running' && (
                  <motion.div
                    animate={{ opacity: [1, 0.3, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                    className="flex items-center space-x-2 mt-2 text-[#78B9B5]"
                  >
                    <span>$</span>
                    <span className="typewriter">Executing...</span>
                  </motion.div>
                )}
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
};

export default StepStatus;