import os

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'ci_pipeline')
JOBS_COLLECTION = 'jobs'

# Webhook Configuration
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 8080))
WEBHOOK_PATH = '/webhook'

# GitHub Configuration
GITHUB_SECRET = os.getenv('GITHUB_SECRET', '')

# Pipeline Configuration
PIPELINE_FILE = '.cicd.yml'
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', './workspace')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')