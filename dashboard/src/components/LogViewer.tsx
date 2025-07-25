import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Copy, Download, Maximize2, Radio } from 'lucide-react';

interface LogViewerProps {
  logs: string[];
  isLive?: boolean;
  title?: string;
}

const LogViewer: React.FC<LogViewerProps> = ({ logs, isLive = false, title = "Logs" }) => {
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isLive && logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, isLive]);

  const copyToClipboard = () => {
    const logText = logs.join('\n');
    navigator.clipboard.writeText(logText);
  };

  const downloadLogs = () => {
    const logText = logs.join('\n');
    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pipeline-logs.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  const formatLogLine = (log: string, index: number) => {
    let className = 'text-[#78B9B5]';
    let icon = '→';
    
    if (log.includes('ERROR') || log.includes('FAILED') || log.includes('failed')) {
      className = 'text-[#ff6b6b]';
      icon = '✗';
    } else if (log.includes('WARN') || log.includes('WARNING')) {
      className = 'text-[#ffd93d]';
      icon = '⚠';
    } else if (log.includes('SUCCESS') || log.includes('completed successfully')) {
      className = 'text-[#6bcf7f]';
      icon = '✓';
    } else if (log.startsWith('[') && log.includes(']')) {
      className = 'text-[#74c0fc]';
      icon = '⏰';
    }

    return (
      <motion.div
        key={index}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: index * 0.02 }}
        className={`mb-2 flex items-start space-x-3 ${className} hover:bg-[#2A004E]/20 px-2 py-1 rounded transition-colors`}
      >
        <span className="text-[#78B9B5]/60 text-xs mt-1 select-none font-mono w-8 text-right">
          {index + 1}
        </span>
        <span className="text-[#78B9B5]/80 mt-1 select-none">{icon}</span>
        <span className="flex-1 break-all">{log}</span>
      </motion.div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl border border-[#78B9B5]/30 overflow-hidden shadow-lg"
    >
      {/* Header with controls */}
      <div className="flex items-center justify-between p-4 border-b border-[#78B9B5]/30 bg-gradient-to-r from-[#2A004E] to-[#320A6B]">
        <div className="flex items-center space-x-3">
          <h3 className="font-bold text-white text-lg drop-shadow-sm">{title}</h3>
          {isLive && (
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="flex items-center space-x-2 bg-[#500073]/40 px-3 py-1 rounded-full border border-[#500073]/60 shadow-sm"
            >
              <Radio className="w-4 h-4 text-white drop-shadow-sm" />
              <span className="text-white text-sm font-semibold">LIVE</span>
            </motion.div>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={copyToClipboard}
            className="p-2 text-white/80 hover:text-white bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-200 shadow-sm"
            title="Copy logs to clipboard"
          >
            <Copy className="w-4 h-4 drop-shadow-sm" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={downloadLogs}
            className="p-2 text-white/80 hover:text-white bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-200 shadow-sm"
            title="Download logs"
          >
            <Download className="w-4 h-4 drop-shadow-sm" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="p-2 text-white/80 hover:text-white bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-200 shadow-sm"
            title="Fullscreen"
          >
            <Maximize2 className="w-4 h-4 drop-shadow-sm" />
          </motion.button>
        </div>
      </div>
      
      {/* Terminal window */}
      <div className="bg-[#1a1a2e] text-sm font-mono relative">
        {/* Terminal header */}
        <div className="flex items-center justify-between px-4 py-2 bg-[#2A004E] border-b border-[#320A6B]">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-[#ff6b6b] rounded-full shadow-sm"></div>
            <div className="w-3 h-3 bg-[#ffd93d] rounded-full shadow-sm"></div>
            <div className="w-3 h-3 bg-[#6bcf7f] rounded-full shadow-sm"></div>
          </div>
          <span className="text-[#78B9B5]/80 text-xs font-semibold">bash</span>
        </div>
        
        {/* Log content */}
        <div className="p-4 max-h-96 overflow-y-auto terminal-scrollbar">
          {logs.length > 0 ? (
            <>
              {logs.map((log, index) => formatLogLine(log, index))}
              <div ref={logEndRef} />
            </>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-[#78B9B5]/60 italic flex items-center justify-center py-8"
            >
              <div className="text-center">
                <div className="text-4xl mb-2">📝</div>
                <div className="text-[#78B9B5]">No logs available yet</div>
                <div className="text-xs mt-1 text-[#78B9B5]/70">Logs will appear here when the job starts</div>
              </div>
            </motion.div>
          )}
          
          {isLive && (
            <motion.div
              animate={{ opacity: [1, 0.3, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="flex items-center space-x-2 text-[#78B9B5] mt-4"
            >
              <span>$</span>
              <span className="typewriter">Streaming live output...</span>
            </motion.div>
          )}
        </div>
        
        {/* Status bar */}
        <div className="flex items-center justify-between px-4 py-2 bg-[#2A004E] border-t border-[#320A6B] text-xs text-[#78B9B5]/80">
          <div className="flex items-center space-x-4">
            <span>Lines: {logs.length}</span>
            <span>Size: {new Blob([logs.join('\n')]).size} bytes</span>
          </div>
          {isLive && (
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-[#6bcf7f] rounded-full animate-pulse shadow-sm"></div>
              <span>Live streaming</span>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default LogViewer;