#!/usr/bin/env python3
from shared_queue import job_queue

def check_job_status():
    jobs = job_queue.list_jobs()
    
    print(f"Total jobs: {len(jobs)}")
    print("=" * 50)
    
    for job_id, job in jobs:
        status_symbol = {
            'queued': '⏳ QUEUED',
            'running': '🔄 RUNNING',
            'done': '✅ DONE',
            'failed': '❌ FAILED'
        }.get(job.status.value, '❓ UNKNOWN')
        
        print(f"{status_symbol} {job_id} | {job.repo_url}")
        
        # Show recent logs for running/failed jobs
        if job.status.value in ['running', 'failed'] and job.logs:
            print("  Recent logs:")
            for log in job.logs[-3:]:  # Last 3 logs
                print(f"    {log}")
        print()

if __name__ == "__main__":
    check_job_status()