from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

class JobStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"

class Job:
    def __init__(self, repo_url: str, commit_sha: str, branch: str = "main"):
        self.repo_url = repo_url
        self.commit_sha = commit_sha
        self.branch = branch
        self.status = JobStatus.QUEUED
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.logs: List[str] = []
        self.steps: List[Dict] = []
        
    def to_dict(self) -> Dict:
        return {
            'repo_url': self.repo_url,
            'commit_sha': self.commit_sha,
            'branch': self.branch,
            'status': self.status.value,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'logs': self.logs,
            'steps': self.steps
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Job':
        job = cls(data['repo_url'], data['commit_sha'], data['branch'])
        job.status = JobStatus(data['status'])
        job.created_at = data['created_at']
        job.started_at = data.get('started_at')
        job.completed_at = data.get('completed_at')
        job.logs = data.get('logs', [])
        job.steps = data.get('steps', [])
        return job