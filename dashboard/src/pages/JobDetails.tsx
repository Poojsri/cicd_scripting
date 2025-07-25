import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { GitBranch, Clock, Play, CheckCircle, XCircle, AlertCircle, ArrowLeft } from 'lucide-react';
import { Job } from '../types';
import { mockData } from '../services/api';
import StepStatus from '../components/StepStatus';
import LogViewer from '../components/LogViewer';

const JobDetails: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<Job | null>(null);
  const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJob = async () => {
      setLoading(true);
      try {
        setJob(mockData.jobDetails);
      } catch (error) {
        console.error('Failed to fetch job:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJob();

    const interval = setInterval(() => {
      if (job?.status === 'running') {
        fetchJob();
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, job?.status]);

  const toggleStepExpansion = (stepName: string) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepName)) {
      newExpanded.delete(stepName);
    } else {
      newExpanded.add(stepName);
    }
    setExpandedSteps(newExpanded);
  };

  const getJobStatusIcon = (status: Job['status']) => {
    const iconClass = "w-8 h-8 text-white drop-shadow-lg";
    switch (status) {
      case 'queued': return <Clock className={iconClass} />;
      case 'running': return <Play className={`${iconClass} animate-pulse`} />;
      case 'done': return <CheckCircle className={iconClass} />;
      case 'failed': return <XCircle className={iconClass} />;
      default: return <AlertCircle className={iconClass} />;
    }
  };

  const getJobStatusClass = (status: Job['status']) => {
    switch (status) {
      case 'queued': return 'status-pending';
      case 'running': return 'status-running';
      case 'done': return 'status-success';
      case 'failed': return 'status-failed';
      default: return 'bg-gray-100';
    }
  };

  const formatDuration = () => {
    if (!job?.started_at) return 'Not started';
    const start = new Date(job.started_at);
    const end = job.completed_at ? new Date(job.completed_at) : new Date();
    const duration = Math.floor((end.getTime() - start.getTime()) / 1000);
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    return minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`;
  };

  const getRepoName = (url: string) => {
    return url.split('/').slice(-2).join('/').replace('.git', '');
  };

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center text-white"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-16 h-16 border-4 border-white/30 border-t-white rounded-full mx-auto mb-4 shadow-lg"
          />
          <p className="text-xl font-semibold drop-shadow-sm">Loading pipeline details...</p>
          <p className="text-white/80 mt-2 drop-shadow-sm">Fetching job information</p>
        </motion.div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white"
        >
          <XCircle className="w-24 h-24 mx-auto mb-4 text-white drop-shadow-lg" />
          <p className="text-2xl font-bold drop-shadow-sm">Job not found</p>
          <p className="text-white/80 mt-2 drop-shadow-sm">The requested pipeline job could not be located</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen gradient-bg">
      {/* Animated background elements with reduced opacity */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-white/3 rounded-full blur-3xl float-animation"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-white/2 rounded-full blur-3xl float-animation" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto py-8 px-4">
        {/* Navigation */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-6"
        >
          <button className="flex items-center space-x-2 text-white/90 hover:text-white transition-colors drop-shadow-sm">
            <ArrowLeft className="w-5 h-5" />
            <span className="font-semibold">Back to Jobs</span>
          </button>
        </motion.div>

        {/* Job Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-3xl p-8 mb-8 border border-[#78B9B5]/30 shadow-xl"
        >
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center space-x-6">
              <div className={`p-4 rounded-2xl ${getJobStatusClass(job.status)} flex items-center justify-center shadow-lg`}>
                {getJobStatusIcon(job.status)}
              </div>
              <div>
                <h1 className="text-4xl font-bold text-high-contrast mb-2 drop-shadow-sm">
                  {getRepoName(job.repo_url)}
                </h1>
                <p className="text-medium-contrast text-lg font-mono">Job #{job.id}</p>
                <p className="text-[#0F828C] mt-1 font-medium">{job.repo_url}</p>
              </div>
            </div>
            
            <motion.div
              whileHover={{ scale: 1.05 }}
              className={`px-6 py-3 rounded-2xl text-white font-bold text-lg shadow-lg ${getJobStatusClass(job.status)}`}
            >
              {job.status.toUpperCase()}
            </motion.div>
          </div>

          {/* Job metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="content-bg rounded-xl p-4 text-center shadow-md border border-[#78B9B5]/20"
            >
              <GitBranch className="w-6 h-6 text-[#065084] mx-auto mb-2 drop-shadow-sm" />
              <p className="text-[#320A6B]/80 text-sm font-semibold">Branch</p>
              <p className="text-high-contrast font-bold text-lg">{job.branch}</p>
            </motion.div>
            
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="content-bg rounded-xl p-4 text-center shadow-md border border-[#78B9B5]/20"
            >
              <div className="w-6 h-6 text-[#320A6B] mx-auto mb-2 font-mono font-bold text-xl drop-shadow-sm">#</div>
              <p className="text-[#320A6B]/80 text-sm font-semibold">Commit</p>
              <p className="text-high-contrast font-mono text-lg">{job.commit_sha.substring(0, 8)}</p>
            </motion.div>
            
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="content-bg rounded-xl p-4 text-center shadow-md border border-[#78B9B5]/20"
            >
              <Clock className="w-6 h-6 text-[#0F828C] mx-auto mb-2 drop-shadow-sm" />
              <p className="text-[#320A6B]/80 text-sm font-semibold">Duration</p>
              <p className="text-high-contrast font-bold text-lg">{formatDuration()}</p>
            </motion.div>
            
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="content-bg rounded-xl p-4 text-center shadow-md border border-[#78B9B5]/20"
            >
              <div className="w-6 h-6 text-[#78B9B5] mx-auto mb-2 text-xl drop-shadow-sm">🚀</div>
              <p className="text-[#320A6B]/80 text-sm font-semibold">Started</p>
              <p className="text-high-contrast font-bold text-lg">
                {job.started_at ? new Date(job.started_at).toLocaleTimeString() : 'Pending'}
              </p>
            </motion.div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Pipeline Steps */}
          <div className="xl:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className="text-3xl font-bold text-white mb-6 neon-text">
                Pipeline Steps
              </h2>
              <div className="space-y-4">
                {job.steps.map((step, index) => (
                  <StepStatus
                    key={step.name}
                    step={step}
                    stepIndex={index}
                    isExpanded={expandedSteps.has(step.name)}
                    onToggle={() => toggleStepExpansion(step.name)}
                  />
                ))}
              </div>
            </motion.div>
          </div>

          {/* Job Logs */}
          <div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <h2 className="text-3xl font-bold text-white mb-6 neon-text">
                Execution Logs
              </h2>
              <LogViewer
                logs={job.logs}
                isLive={job.status === 'running'}
                title="Job Execution Logs"
              />
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetails;