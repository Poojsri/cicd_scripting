#!/usr/bin/env python3
import threading
import time
import json
import requests
from core.webhook_listener import WebhookListener
from core.executor import PipelineExecutor
from core.memory_queue import MemoryJobQueue

def test_ci_pipeline():
    # Use in-memory queue for testing
    job_queue = MemoryJobQueue()
    
    # Start webhook listener in background
    def start_webhook():
        listener = WebhookListener(job_queue)
        listener.start()
    
    webhook_thread = threading.Thread(target=start_webhook, daemon=True)
    webhook_thread.start()
    
    print("🚀 CI/CD Server started!")
    print("📡 Webhook listener: http://localhost:8080/webhook")
    
    # Wait for server to start
    time.sleep(2)
    
    # Send test webhook
    print("\n📤 Sending test webhook...")
    
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
        print(f"✅ Webhook response: {response.status_code}")
        
        # Show jobs
        time.sleep(1)
        jobs = job_queue.list_jobs()
        print(f"\n📋 Jobs in queue: {len(jobs)}")
        
        for job_id, job in jobs:
            print(f"  {job_id}: {job.status.value} - {job.repo_url}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🔄 Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopped!")

if __name__ == "__main__":
    test_ci_pipeline()