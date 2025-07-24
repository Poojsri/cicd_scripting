import json
import os
import uuid
from typing import Optional, List
from datetime import datetime

from models.job import Job, JobStatus

class FileJobQueue:
    def __init__(self, file_path="jobs.json"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
    
    def _load_jobs(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        jobs = {}
        for job_id, job_data in data.items():
            # Convert datetime strings back to datetime objects
            if job_data.get('created_at'):
                job_data['created_at'] = datetime.fromisoformat(job_data['created_at'])
            if job_data.get('started_at'):
                job_data['started_at'] = datetime.fromisoformat(job_data['started_at'])
            if job_data.get('completed_at'):
                job_data['completed_at'] = datetime.fromisoformat(job_data['completed_at'])
            
            jobs[job_id] = Job.from_dict(job_data)
        return jobs
    
    def _save_jobs(self, jobs):
        data = {}
        for job_id, job in jobs.items():
            job_dict = job.to_dict()
            # Convert datetime objects to strings
            if job_dict.get('created_at'):
                job_dict['created_at'] = job_dict['created_at'].isoformat()
            if job_dict.get('started_at'):
                job_dict['started_at'] = job_dict['started_at'].isoformat()
            if job_dict.get('completed_at'):
                job_dict['completed_at'] = job_dict['completed_at'].isoformat()
            
            data[job_id] = job_dict
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_job(self, job: Job) -> str:
        jobs = self._load_jobs()
        job_id = str(uuid.uuid4())[:8]
        jobs[job_id] = job
        self._save_jobs(jobs)
        return job_id
    
    def get_next_job(self) -> Optional[tuple[str, Job]]:
        jobs = self._load_jobs()
        for job_id, job in jobs.items():
            if job.status == JobStatus.QUEUED:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.utcnow()
                self._save_jobs(jobs)
                return job_id, job
        return None
    
    def update_job_status(self, job_id: str, status: JobStatus, logs: List[str] = None):
        jobs = self._load_jobs()
        if job_id in jobs:
            jobs[job_id].status = status
            if status in [JobStatus.DONE, JobStatus.FAILED]:
                jobs[job_id].completed_at = datetime.utcnow()
            if logs:
                jobs[job_id].logs = logs
            self._save_jobs(jobs)
    
    def get_job(self, job_id: str) -> Optional[Job]:
        jobs = self._load_jobs()
        return jobs.get(job_id)
    
    def list_jobs(self, limit: int = 50) -> List[tuple[str, Job]]:
        jobs = self._load_jobs()
        items = list(jobs.items())
        items.sort(key=lambda x: x[1].created_at, reverse=True)
        return items[:limit]