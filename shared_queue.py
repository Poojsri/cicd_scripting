# Shared job queue instance
from core.file_queue import FileJobQueue

# Global shared instance with file persistence
job_queue = FileJobQueue()