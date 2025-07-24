import subprocess
import os
import shutil
from datetime import datetime
from typing import List, Dict

# Import removed - using shared_queue
from core.pipeline_parser import PipelineParser
from core.security_scanner import SecurityScanner
from models.job import Job, JobStatus

class PipelineExecutor:
    def __init__(self, job_queue = None):
        if job_queue is None:
            from shared_queue import job_queue as shared_queue
            self.job_queue = shared_queue
        else:
            self.job_queue = job_queue
        self.parser = PipelineParser()
        self.security_scanner = SecurityScanner()
    
    def execute_job(self, job_id: str, job: Job) -> bool:
        """Execute a single job"""
        logs = []
        repo_path = None
        
        try:
            logs.append(f"[{datetime.now()}] Starting job for {job.repo_url}@{job.commit_sha}")
            
            # Clone repository
            logs.append(f"[{datetime.now()}] Cloning repository...")
            repo_path = self.parser.clone_repo(job.repo_url, job.commit_sha, job.branch)
            logs.append(f"[{datetime.now()}] Repository cloned to {repo_path}")
            
            # Parse pipeline
            logs.append(f"[{datetime.now()}] Parsing pipeline...")
            pipeline = self.parser.parse_pipeline(repo_path)
            
            if not self.parser.validate_pipeline(pipeline):
                raise Exception("Invalid pipeline configuration")
            
            logs.append(f"[{datetime.now()}] Pipeline '{pipeline['name']}' loaded with {len(pipeline['steps'])} steps")
            
            # Security scan
            logs.append(f"[{datetime.now()}] Running security scan...")
            security_result = self.security_scanner.scan_repository(repo_path)
            logs.append(f"[{datetime.now()}] Security scan: {security_result['total_issues']} issues found, Risk: {security_result['risk_level']}")
            
            # Block execution if critical security issues found
            if security_result['risk_level'] == 'CRITICAL':
                logs.append(f"[{datetime.now()}] CRITICAL security issues found - blocking execution")
                for issue in security_result['issues']:
                    if issue['severity'] == 'CRITICAL':
                        logs.append(f"  - {issue['description']} in {issue['file']}")
                self.job_queue.update_job_status(job_id, JobStatus.FAILED, logs)
                return False
            
            # Execute steps
            for i, step in enumerate(pipeline['steps']):
                logs.append(f"[{datetime.now()}] Executing step {i+1}: {step['name']}")
                
                result = subprocess.run(
                    step['run'],
                    shell=True,
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per step
                )
                
                if result.stdout:
                    logs.append(f"STDOUT: {result.stdout}")
                if result.stderr:
                    logs.append(f"STDERR: {result.stderr}")
                
                if result.returncode != 0:
                    logs.append(f"[{datetime.now()}] Step failed with exit code {result.returncode}")
                    self.job_queue.update_job_status(job_id, JobStatus.FAILED, logs)
                    return False
                
                logs.append(f"[{datetime.now()}] Step {step['name']} completed successfully")
            
            logs.append(f"[{datetime.now()}] All steps completed successfully")
            self.job_queue.update_job_status(job_id, JobStatus.DONE, logs)
            return True
            
        except Exception as e:
            logs.append(f"[{datetime.now()}] Job failed: {str(e)}")
            self.job_queue.update_job_status(job_id, JobStatus.FAILED, logs)
            return False
        
        finally:
            # Keep workspace for next run (faster git pull)
            if repo_path:
                logs.append(f"[{datetime.now()}] Workspace preserved for future runs")
    
    def run_worker(self):
        """Main worker loop to process jobs"""
        print("Pipeline executor started")
        
        while True:
            try:
                job_data = self.job_queue.get_next_job()
                if job_data:
                    job_id, job = job_data
                    print(f"Processing job {job_id}")
                    self.execute_job(job_id, job)
                else:
                    # No jobs available, wait a bit
                    import time
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                print("Executor stopped")
                break
            except Exception as e:
                print(f"Executor error: {e}")
                import time
                time.sleep(10)