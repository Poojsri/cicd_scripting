#!/usr/bin/env python3
import threading
import time
import json
import requests
from core.webhook_listener import WebhookListener
from core.memory_queue import MemoryJobQueue

def test_webhook():
    # Use in-memory queue
    job_queue = MemoryJobQueue()
    
    # Start webhook listener
    def start_webhook():
        listener = WebhookListener(job_queue)
        listener.start()
    
    webhook_thread = threading.Thread(target=start_webhook, daemon=True)
    webhook_thread.start()
    
    print("CI/CD Server started on http://localhost:8080/webhook")
    time.sleep(2)
    
    # Test webhook
    payload = {
        "ref": "refs/heads/main",
        "after": "abc123def",
        "repository": {
            "clone_url": "https://github.com/octocat/Hello-World.git"
        },
        "commits": [{"message": "Test commit"}]
    }
    
    try:
        response = requests.post(
            'http://localhost:8080/webhook',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Webhook response: {response.status_code}")
        
        # Show jobs
        jobs = job_queue.list_jobs()
        print(f"Jobs created: {len(jobs)}")
        
        for job_id, job in jobs:
            print(f"  {job_id}: {job.status.value} - {job.repo_url}")
            
        print("SUCCESS: Webhook working!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_webhook()