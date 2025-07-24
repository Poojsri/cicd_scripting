import axios from 'axios';
import { Job, JobSummary } from '../types';

const API_BASE_URL = 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const jobsApi = {
  // Get all jobs
  getJobs: async (): Promise<JobSummary[]> => {
    const response = await api.get('/jobs');
    return response.data;
  },

  // Get specific job details
  getJob: async (jobId: string): Promise<Job> => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  // Get job logs (for real-time updates)
  getJobLogs: async (jobId: string): Promise<string[]> => {
    const response = await api.get(`/jobs/${jobId}/logs`);
    return response.data;
  },
};

// Mock data for development
export const mockData = {
  jobs: [
    {
      id: '8f27a832',
      repo_name: 'octocat/Hello-World',
      branch: 'main',
      status: 'done' as const,
      created_at: '2025-07-24T15:24:00Z',
      duration: 45,
    },
    {
      id: '443656dc',
      repo_name: 'user/test-repo',
      branch: 'feature/new-api',
      status: 'running' as const,
      created_at: '2025-07-24T15:30:00Z',
    },
    {
      id: '1b428ada',
      repo_name: 'company/backend',
      branch: 'main',
      status: 'failed' as const,
      created_at: '2025-07-24T15:25:00Z',
      duration: 120,
    },
  ] as JobSummary[],

  jobDetails: {
    id: '8f27a832',
    repo_url: 'https://github.com/octocat/Hello-World.git',
    branch: 'main',
    commit_sha: 'abc123def456',
    status: 'running' as const,
    created_at: '2025-07-24T15:24:00Z',
    started_at: '2025-07-24T15:24:05Z',
    logs: [
      '[2025-07-24 15:24:05] Starting job for https://github.com/octocat/Hello-World.git@main',
      '[2025-07-24 15:24:05] Security scan: 0 issues found, Risk: LOW',
      '[2025-07-24 15:24:06] Pipeline loaded with 3 steps',
    ],
    steps: [
      {
        name: 'check_python',
        run: 'python --version',
        status: 'success' as const,
        logs: ['Python 3.12.2'],
        started_at: '2025-07-24T15:24:06Z',
        completed_at: '2025-07-24T15:24:06Z',
      },
      {
        name: 'list_files',
        run: 'dir',
        status: 'running' as const,
        logs: [
          'Volume in drive C has no label.',
          'Directory of c:\\workspace\\Hello-World',
          '24/07/2025  15:24    <DIR>          .',
          '24/07/2025  15:24    <DIR>          ..',
          '24/07/2025  15:24             1,234 README.md',
        ],
        started_at: '2025-07-24T15:24:07Z',
      },
      {
        name: 'test_echo',
        run: 'echo "Pipeline completed successfully!"',
        status: 'pending' as const,
        logs: [],
      },
    ],
  } as Job,
};