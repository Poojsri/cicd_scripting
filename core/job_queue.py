from pymongo import MongoClient
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from config.settings import MONGO_URI, DATABASE_NAME, JOBS_COLLECTION
from models.job import Job, JobStatus

class JobQueue:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[JOBS_COLLECTION]
    
    def add_job(self, job: Job) -> str:
        """Add a job to the queue and return job ID"""
        result = self.collection.insert_one(job.to_dict())
        return str(result.inserted_id)
    
    def get_next_job(self) -> Optional[tuple[str, Job]]:
        """Get the next queued job"""
        job_doc = self.collection.find_one_and_update(
            {'status': JobStatus.QUEUED.value},
            {'$set': {'status': JobStatus.RUNNING.value, 'started_at': datetime.utcnow()}},
            sort=[('created_at', 1)]
        )
        if job_doc:
            return str(job_doc['_id']), Job.from_dict(job_doc)
        return None
    
    def update_job_status(self, job_id: str, status: JobStatus, logs: List[str] = None):
        """Update job status and logs"""
        update_data = {'status': status.value}
        if status in [JobStatus.DONE, JobStatus.FAILED]:
            update_data['completed_at'] = datetime.utcnow()
        if logs:
            update_data['logs'] = logs
        
        self.collection.update_one(
            {'_id': ObjectId(job_id)},
            {'$set': update_data}
        )
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        job_doc = self.collection.find_one({'_id': ObjectId(job_id)})
        return Job.from_dict(job_doc) if job_doc else None
    
    def list_jobs(self, limit: int = 50) -> List[tuple[str, Job]]:
        """List recent jobs"""
        jobs = []
        for doc in self.collection.find().sort('created_at', -1).limit(limit):
            jobs.append((str(doc['_id']), Job.from_dict(doc)))
        return jobs