#!/usr/bin/env python3
import subprocess
import os
import shutil
from datetime import datetime
from shared_queue import job_queue
from models.job import JobStatus

def execute_single_job():
    """Execute one job from the queue"""
    
    # Get next job
    job_data = job_queue.get_next_job()
    if not job_data:
        print("No jobs in queue")
        return
    
    job_id, job = job_data
    print(f"Processing job {job_id}")
    
    logs = []
    
    try:
        logs.append(f"[{datetime.now()}] Starting job for {job.repo_url}")
        
        # Setup workspace
        workspace = "workspace"
        os.makedirs(workspace, exist_ok=True)
        
        repo_name = job.repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(workspace, repo_name)
        
        # Clone or update repo
        if os.path.exists(repo_path):
            logs.append(f"[{datetime.now()}] Updating existing repository...")
            result = subprocess.run(['git', 'pull'], cwd=repo_path, 
                                  capture_output=True, text=True)
        else:
            logs.append(f"[{datetime.now()}] Cloning repository...")
            result = subprocess.run(['git', 'clone', job.repo_url, repo_path], 
                                  capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Git operation failed: {result.stderr}")
        
        logs.append(f"[{datetime.now()}] Repository ready at {repo_path}")
        
        # Simple pipeline steps
        steps = [
            {"name": "check_python", "run": "python --version"},
            {"name": "list_files", "run": "dir"},
            {"name": "test_echo", "run": "echo CI/CD Pipeline Success!"}
        ]
        
        # Execute steps
        for i, step in enumerate(steps):
            logs.append(f"[{datetime.now()}] Executing step {i+1}: {step['name']}")
            
            result = subprocess.run(step['run'], shell=True, cwd=repo_path,
                                  capture_output=True, text=True, timeout=60)
            
            if result.stdout:
                logs.append(f"STDOUT: {result.stdout.strip()}")
            if result.stderr:
                logs.append(f"STDERR: {result.stderr.strip()}")
            
            if result.returncode != 0:
                logs.append(f"[{datetime.now()}] Step failed with exit code {result.returncode}")
                job_queue.update_job_status(job_id, JobStatus.FAILED, logs)
                return False
            
            logs.append(f"[{datetime.now()}] Step {step['name']} completed successfully")
        
        logs.append(f"[{datetime.now()}] All steps completed successfully")
        job_queue.update_job_status(job_id, JobStatus.DONE, logs)
        print(f"Job {job_id} completed successfully!")
        return True
        
    except Exception as e:
        logs.append(f"[{datetime.now()}] Job failed: {str(e)}")
        job_queue.update_job_status(job_id, JobStatus.FAILED, logs)
        print(f"Job {job_id} failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Fixed Executor Test ===")
    execute_single_job()