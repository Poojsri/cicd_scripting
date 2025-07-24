#!/usr/bin/env python3
import requests
import json
import time

def quick_test():
    payload = {
        "ref": "refs/heads/main",
        "after": "abc123",
        "repository": {
            "clone_url": "https://github.com/octocat/Hello-World.git"
        },
        "commits": [{"message": "Test"}]
    }
    
    # Send webhook
    response = requests.post('http://localhost:8080/webhook', json=payload)
    print(f"Webhook: {response.status_code}")
    
    # Check jobs immediately
    from shared_queue import job_queue
    jobs = job_queue.list_jobs()
    print(f"Jobs in queue: {len(jobs)}")
    
    for job_id, job in jobs:
        print(f"  {job_id}: {job.status.value} - {job.repo_url}")

if __name__ == "__main__":
    quick_test()