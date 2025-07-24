#!/usr/bin/env python3
# Test dashboard directly
from shared_queue import job_queue

def test_dashboard():
    print("Testing dashboard access to shared queue...")
    
    jobs = job_queue.list_jobs()
    print(f"Jobs found: {len(jobs)}")
    
    for job_id, job in jobs:
        print(f"  {job_id}: {job.status.value} - {job.repo_url}")

if __name__ == "__main__":
    test_dashboard()