#!/usr/bin/env python3
# Test job creation directly
from shared_queue import job_queue
from models.job import Job

def test_direct_job_creation():
    print("Testing direct job creation...")
    
    # Create a job directly
    job = Job(
        repo_url="https://github.com/user/test-repo.git",
        commit_sha="def456ghi789",
        branch="main"
    )
    
    job_id = job_queue.add_job(job)
    print(f"Created job: {job_id}")
    
    # List jobs
    jobs = job_queue.list_jobs()
    print(f"Jobs in queue: {len(jobs)}")
    
    for jid, j in jobs:
        print(f"  {jid}: {j.status.value} - {j.repo_url}")

if __name__ == "__main__":
    test_direct_job_creation()