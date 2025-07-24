#!/usr/bin/env python3
import sys
from shared_queue import job_queue

def show_jobs(limit=10):
    jobs = job_queue.list_jobs(limit)
    
    if not jobs:
        print("No jobs found.")
        return
    
    print(f"\nRecent Jobs (showing {len(jobs)} of {limit})")
    print("=" * 60)
    
    for job_id, job in jobs:
        status_symbol = {
            'queued': '[QUEUED]',
            'running': '[RUNNING]',
            'done': '[DONE]',
            'failed': '[FAILED]'
        }.get(job.status.value, '[UNKNOWN]')
        
        print(f"{status_symbol} {job_id} | {job.repo_url}")
        print(f"   Branch: {job.branch} | Commit: {job.commit_sha[:8]}")
        print(f"   Created: {job.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

def show_logs(job_id):
    job = job_queue.get_job(job_id)
    
    if not job:
        print(f"Job {job_id} not found.")
        return
    
    print(f"\nLogs for Job {job_id}")
    print("=" * 60)
    print(f"Repository: {job.repo_url}")
    print(f"Status: {job.status.value}")
    print("-" * 60)
    
    if job.logs:
        for log in job.logs:
            print(log)
    else:
        print("No logs available.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python simple_dashboard.py jobs [limit]")
        print("  python simple_dashboard.py logs <job_id>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "jobs":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_jobs(limit)
    elif command == "logs":
        if len(sys.argv) < 3:
            print("Please provide job ID")
            sys.exit(1)
        job_id = sys.argv[2]
        show_logs(job_id)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()