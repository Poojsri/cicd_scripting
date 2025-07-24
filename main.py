#!/usr/bin/env python3
import sys
import threading
from core.webhook_listener import WebhookListener
from core.executor import PipelineExecutor
from core.job_queue import JobQueue

def start_webhook_listener(job_queue):
    """Start webhook listener in a separate thread"""
    listener = WebhookListener(job_queue)
    listener.start()

def start_executor(job_queue):
    """Start job executor in a separate thread"""
    executor = PipelineExecutor(job_queue)
    executor.run_worker()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [webhook|executor|both]")
        sys.exit(1)
    
    mode = sys.argv[1]
    job_queue = JobQueue()
    
    if mode == "webhook":
        start_webhook_listener(job_queue)
    elif mode == "executor":
        start_executor(job_queue)
    elif mode == "both":
        # Start webhook listener in background thread
        webhook_thread = threading.Thread(
            target=start_webhook_listener, 
            args=(job_queue,), 
            daemon=True
        )
        webhook_thread.start()
        
        # Start executor in main thread
        start_executor(job_queue)
    else:
        print("Invalid mode. Use: webhook, executor, or both")
        sys.exit(1)

if __name__ == "__main__":
    main()