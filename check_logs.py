#!/usr/bin/env python3
from shared_queue import job_queue

def check_failed_jobs():
    jobs = job_queue.list_jobs()
    
    for job_id, job in jobs:
        if job.status.value == 'failed':
            print(f"\n=== Job {job_id} FAILED ===")
            print(f"Repo: {job.repo_url}")
            print("Logs:")
            for log in job.logs:
                print(f"  {log}")

if __name__ == "__main__":
    check_failed_jobs()