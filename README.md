# Custom CI/CD Pipeline Tool

A minimal, educational CI/CD pipeline tool built from scratch using Python and MongoDB.

## Features

- 🔗 **Webhook Listener**: Receives GitHub push events via HTTP server
- 📋 **Job Queue**: MongoDB-based job management with status tracking
- 📄 **Pipeline Parser**: Reads `.cicd.yml` configuration files
- ⚡ **Executor**: Runs pipeline steps using subprocess
- 📊 **Dashboard**: CLI interface to view jobs and logs

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB
Make sure MongoDB is running on `localhost:27017` (default).

### 3. Run the CI/CD Server

**Option A: Run both webhook listener and executor**
```bash
python main.py both
```

**Option B: Run components separately**
```bash
# Terminal 1: Start webhook listener
python main.py webhook

# Terminal 2: Start job executor
python main.py executor
```

### 4. Test the Webhook
```bash
python tests/test_webhook.py
```

### 5. View Jobs
```bash
# Show recent jobs
python dashboard.py jobs

# Show logs for specific job
python dashboard.py logs <job_id>
```

## Pipeline Configuration

Create a `.cicd.yml` file in your repository:

```yaml
name: "My Pipeline"
steps:
  - name: "setup"
    run: "python --version"
  
  - name: "install"
    run: "pip install -r requirements.txt"
  
  - name: "test"
    run: "python -m pytest"
  
  - name: "build"
    run: "python setup.py sdist"
```

## GitHub Webhook Setup

1. Go to your GitHub repository settings
2. Add webhook: `http://your-server:8080/webhook`
3. Set content type to `application/json`
4. Select "Push events"

## Environment Variables

```bash
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=ci_pipeline
WEBHOOK_PORT=8080
GITHUB_SECRET=your_webhook_secret
WORKSPACE_DIR=./workspace
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GitHub Push    │───▶│ Webhook Listener │───▶│   Job Queue     │
│     Event       │    │  (http.server)  │    │   (MongoDB)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Dashboard    │◀───│   Executor      │◀───│ Pipeline Parser │
│   (CLI/Logs)    │    │ (subprocess)    │    │  (.cicd.yml)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Job Statuses

- `queued`: Job waiting to be processed
- `running`: Job currently executing
- `done`: Job completed successfully
- `failed`: Job failed during execution