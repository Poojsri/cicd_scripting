from typing import Optional, List
from datetime import datetime
import uuid

from models.job import Job, JobStatus

class MemoryJobQueue:
    def __init__(self):
        self.jobs = {}
        self.queue = []
    
    def add_job(self, job: Job) -> str:
        job_id = str(uuid.uuid4())[:8]
        self.jobs[job_id] = job
        self.queue.append(job_id)
        return job_id
    
    def get_next_job(self) -> Optional[tuple[str, Job]]:
        for job_id in self.queue:
            if job_id in self.jobs and self.jobs[job_id].status == JobStatus.QUEUED:
                self.jobs[job_id].status = JobStatus.RUNNING
                self.jobs[job_id].started_at = datetime.utcnow()
                return job_id, self.jobs[job_id]
        return None
    
    def update_job_status(self, job_id: str, status: JobStatus, logs: List[str] = None):
        if job_id in self.jobs:
            self.jobs[job_id].status = status
            if status in [JobStatus.DONE, JobStatus.FAILED]:
                self.jobs[job_id].completed_at = datetime.utcnow()
            if logs:
                self.jobs[job_id].logs = logs
    
    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)
    
    def list_jobs(self, limit: int = 50) -> List[tuple[str, Job]]:
        items = list(self.jobs.items())
        items.sort(key=lambda x: x[1].created_at, reverse=True)
        return items[:limit]