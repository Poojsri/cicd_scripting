import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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
    // Simulate API call - replace with real API later
    const fetchJob = async () => {
      setLoading(true);
      try {
        // For now, use mock data
        setJob(mockData.jobDetails);
      } catch (error) {
        console.error('Failed to fetch job:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJob();

    // Poll for updates every 2 seconds if job is running
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
    switch (status) {
      case 'queued': return '⏳';
      case 'running': return '🔄';
      case 'done': return '✅';
      case 'failed': return '❌';
      default: return '❓';
    }
  };

  const getJobStatusColor = (status: Job['status']) => {
    switch (status) {
      case 'queued': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'running': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'done': return 'text-green-600 bg-green-50 border-green-200';
      case 'failed': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const formatDuration = () => {
    if (!job?.started_at) return 'Not started';
    const start = new Date(job.started_at);
    const end = job.completed_at ? new Date(job.completed_at) : new Date();
    const duration = Math.floor((end.getTime() - start.getTime()) / 1000);
    return `${duration}s`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading job details...</p>
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-600">Job not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-8 px-4">
        {/* Job Header */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">{getJobStatusIcon(job.status)}</span>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Job {job.id}</h1>
                <p className="text-gray-600">{job.repo_url}</p>
              </div>
            </div>
            <div className={`px-4 py-2 rounded-lg border ${getJobStatusColor(job.status)}`}>
              <span className="font-semibold">{job.status.toUpperCase()}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Branch:</span>
              <p className="font-semibold">{job.branch}</p>
            </div>
            <div>
              <span className="text-gray-500">Commit:</span>
              <p className="font-mono text-sm">{job.commit_sha.substring(0, 8)}</p>
            </div>
            <div>
              <span className="text-gray-500">Duration:</span>
              <p className="font-semibold">{formatDuration()}</p>
            </div>
            <div>
              <span className="text-gray-500">Started:</span>
              <p className="font-semibold">
                {job.started_at ? new Date(job.started_at).toLocaleTimeString() : 'Not started'}
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Pipeline Steps */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Pipeline Steps</h2>
            {job.steps.map((step) => (
              <StepStatus
                key={step.name}
                step={step}
                isExpanded={expandedSteps.has(step.name)}
                onToggle={() => toggleStepExpansion(step.name)}
              />
            ))}
          </div>

          {/* Job Logs */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Job Logs</h2>
            <LogViewer
              logs={job.logs}
              isLive={job.status === 'running'}
              title="Job Execution Logs"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetails;