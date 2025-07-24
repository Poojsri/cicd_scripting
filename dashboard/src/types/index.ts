export interface Job {
  id: string;
  repo_url: string;
  branch: string;
  commit_sha: string;
  status: 'queued' | 'running' | 'done' | 'failed';
  created_at: string;
  started_at?: string;
  completed_at?: string;
  logs: string[];
  steps: PipelineStep[];
}

export interface PipelineStep {
  name: string;
  run: string;
  status: 'pending' | 'running' | 'success' | 'failed';
  logs: string[];
  started_at?: string;
  completed_at?: string;
}

export interface JobSummary {
  id: string;
  repo_name: string;
  branch: string;
  status: Job['status'];
  created_at: string;
  duration?: number;
}