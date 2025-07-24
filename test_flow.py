#!/usr/bin/env python3
# Test the complete CI/CD flow
import time
import subprocess
import threading
from shared_queue import job_queue
from models.job import Job

def test_complete_flow():
    print("=== Testing Complete CI/CD Flow ===")
    
    # 1. Create a job
    print("1. Creating job...")
    job = Job(
        repo_url="https://github.com/octocat/Hello-World.git",
        commit_sha="main",
        branch="main"
    )
    job_id = job_queue.add_job(job)
    print(f"   Job created: {job_id}")
    
    # 2. Check job status
    print("2. Checking job status...")
    jobs = job_queue.list_jobs(1)
    if jobs:
        job_id, job = jobs[0]
        print(f"   Status: {job.status.value}")
    
    # 3. Start executor in background
    print("3. Starting executor...")
    def run_executor():
        from core.executor import PipelineExecutor
        executor = PipelineExecutor()
        executor.execute_job(job_id, job)
    
    executor_thread = threading.Thread(target=run_executor)
    executor_thread.start()
    
    # 4. Wait and check results
    print("4. Waiting for execution...")
    executor_thread.join(timeout=60)  # Wait max 60 seconds
    
    # 5. Check final status
    print("5. Checking final status...")
    final_job = job_queue.get_job(job_id)
    if final_job:
        print(f"   Final status: {final_job.status.value}")
        if final_job.logs:
            print("   Recent logs:")
            for log in final_job.logs[-3:]:
                print(f"     {log}")
    
    return final_job.status.value if final_job else "unknown"

if __name__ == "__main__":
    result = test_complete_flow()
    if result == "done":
        print("\nSUCCESS: CI/CD pipeline works!")
    else:
        print(f"\nResult: {result}")
        print("Check logs for details")