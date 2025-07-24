#!/usr/bin/env python3
import sys
from datetime import datetime
# Remove this import block

class Dashboard:
    def __init__(self):
        from shared_queue import job_queue
        self.job_queue = job_queue
    
    def show_jobs(self, limit=10):
        """Display recent jobs"""
        jobs = self.job_queue.list_jobs(limit)
        
        if not jobs:
            print("No jobs found.")
            return
        
        print(f"\n📋 Recent Jobs (showing {len(jobs)} of {limit})")
        print("=" * 80)
        
        for job_id, job in jobs:
            status_emoji = {
                'queued': '⏳',
                'running': '🔄',
                'done': '✅',
                'failed': '❌'
            }.get(job.status.value, '❓')
            
            print(f"{status_emoji} {job_id[:8]} | {job.status.value.upper():8} | {job.repo_url}")
            print(f"   Branch: {job.branch} | Commit: {job.commit_sha[:8]}")
            print(f"   Created: {job.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if job.completed_at:
                duration = job.completed_at - job.started_at if job.started_at else None
                if duration:
                    print(f"   Duration: {duration.total_seconds():.1f}s")
            
            print()
    
    def show_job_logs(self, job_id):
        """Display logs for a specific job"""
        job = self.job_queue.get_job(job_id)
        
        if not job:
            print(f"Job {job_id} not found.")
            return
        
        print(f"\n📝 Logs for Job {job_id}")
        print("=" * 80)
        print(f"Repository: {job.repo_url}")
        print(f"Branch: {job.branch}")
        print(f"Commit: {job.commit_sha}")
        print(f"Status: {job.status.value}")
        print("-" * 80)
        
        if job.logs:
            for log in job.logs:
                print(log)
        else:
            print("No logs available.")

def main():
    dashboard = Dashboard()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python dashboard.py jobs [limit]     - Show recent jobs")
        print("  python dashboard.py logs <job_id>    - Show job logs")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "jobs":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        dashboard.show_jobs(limit)
    elif command == "logs":
        if len(sys.argv) < 3:
            print("Please provide job ID")
            sys.exit(1)
        job_id = sys.argv[2]
        dashboard.show_job_logs(job_id)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()