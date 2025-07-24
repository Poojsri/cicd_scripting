import json
import hmac
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from config.settings import WEBHOOK_PORT, WEBHOOK_PATH, GITHUB_SECRET
from models.job import Job

class WebhookHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, job_queue = None, **kwargs):
        if job_queue is None:
            try:
                from shared_queue import job_queue as shared_queue
                self.job_queue = shared_queue
            except ImportError:
                from core.job_queue import JobQueue
                self.job_queue = JobQueue()
        else:
            self.job_queue = job_queue
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path != WEBHOOK_PATH:
            self.send_response(404)
            self.end_headers()
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        # Verify GitHub signature if secret is configured
        if GITHUB_SECRET and not self._verify_signature(body):
            self.send_response(401)
            self.end_headers()
            return
        
        try:
            payload = json.loads(body.decode('utf-8'))
            print(f"DEBUG: Received payload: {payload}")
            
            if self._is_push_event(payload):
                print("DEBUG: Is push event - creating job")
                job = self._create_job_from_payload(payload)
                job_id = self.job_queue.add_job(job)
                print(f"Job {job_id} queued for {job.repo_url}@{job.commit_sha}")
            else:
                print("DEBUG: Not a push event, ignoring")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception as e:
            print(f"Webhook error: {e}")
            self.send_response(500)
            self.end_headers()
    
    def _verify_signature(self, body: bytes) -> bool:
        signature = self.headers.get('X-Hub-Signature-256', '')
        if not signature.startswith('sha256='):
            return False
        
        expected = hmac.new(
            GITHUB_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected}", signature)
    
    def _is_push_event(self, payload: dict) -> bool:
        return 'commits' in payload and 'repository' in payload
    
    def _create_job_from_payload(self, payload: dict) -> Job:
        repo_url = payload['repository']['clone_url']
        commit_sha = payload['after']
        branch = payload['ref'].split('/')[-1]
        return Job(repo_url, commit_sha, branch)

class WebhookListener:
    def __init__(self, job_queue = None):
        if job_queue is None:
            try:
                from shared_queue import job_queue as shared_queue
                self.job_queue = shared_queue
            except ImportError:
                from core.job_queue import JobQueue
                self.job_queue = JobQueue()
        else:
            self.job_queue = job_queue
    
    def start(self):
        def handler(*args, **kwargs):
            return WebhookHandler(*args, job_queue=self.job_queue, **kwargs)
        
        server = HTTPServer(('', WEBHOOK_PORT), handler)
        print(f"Webhook listener started on port {WEBHOOK_PORT}")
        server.serve_forever()