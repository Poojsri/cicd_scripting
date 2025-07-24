import React, { useEffect, useRef } from 'react';

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

  const formatLogLine = (log: string, index: number) => {
    // Color coding based on log content
    let className = 'text-green-400';
    
    if (log.includes('ERROR') || log.includes('FAILED') || log.includes('failed')) {
      className = 'text-red-400';
    } else if (log.includes('WARN') || log.includes('WARNING')) {
      className = 'text-yellow-400';
    } else if (log.includes('SUCCESS') || log.includes('completed successfully')) {
      className = 'text-green-400';
    } else if (log.startsWith('[') && log.includes(']')) {
      className = 'text-blue-400'; // Timestamps
    }

    return (
      <div key={index} className={`mb-1 ${className}`}>
        <span className="text-gray-500 text-xs mr-2">{index + 1}</span>
        {log}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border">
      <div className="flex items-center justify-between p-3 border-b bg-gray-50">
        <h3 className="font-semibold text-gray-900 flex items-center">
          {title}
          {isLive && (
            <span className="ml-2 flex items-center">
              <span className="animate-pulse w-2 h-2 bg-green-500 rounded-full mr-1"></span>
              <span className="text-xs text-green-600">LIVE</span>
            </span>
          )}
        </h3>
        <button
          onClick={copyToClipboard}
          className="text-sm text-gray-600 hover:text-gray-900 px-2 py-1 rounded hover:bg-gray-200"
          title="Copy logs to clipboard"
        >
          📋 Copy
        </button>
      </div>
      
      <div className="bg-gray-900 text-sm font-mono p-4 max-h-96 overflow-y-auto">
        {logs.length > 0 ? (
          <>
            {logs.map((log, index) => formatLogLine(log, index))}
            <div ref={logEndRef} />
          </>
        ) : (
          <div className="text-gray-500 italic">No logs available</div>
        )}
        
        {isLive && (
          <div className="animate-pulse text-green-400 mt-2">▋</div>
        )}
      </div>
    </div>
  );
};

export default LogViewer;