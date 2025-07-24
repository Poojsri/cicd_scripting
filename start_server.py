#!/usr/bin/env python3
import threading
import time
from core.webhook_listener import WebhookListener
from core.executor import PipelineExecutor
from shared_queue import job_queue

def start_full_server():
    
    print("Starting CI/CD Pipeline Server...")
    
    # Start webhook listener in background
    def webhook_worker():
        listener = WebhookListener(job_queue)
        listener.start()
    
    webhook_thread = threading.Thread(target=webhook_worker, daemon=True)
    webhook_thread.start()
    
    print("Webhook listener: http://localhost:8080/webhook")
    
    # Wait for webhook to start
    time.sleep(2)
    
    # Start executor in main thread
    print("Starting job executor...")
    executor = PipelineExecutor(job_queue)
    
    try:
        executor.run_worker()
    except KeyboardInterrupt:
        print("\nServer stopped!")

if __name__ == "__main__":
    start_full_server()