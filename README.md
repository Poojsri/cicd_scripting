# Custom CI/CD Pipeline Tool

A minimal, educational CI/CD pipeline tool built from scratch using Python with file-based persistence.

## Features

- 🔗 **Webhook Listener**: Receives GitHub push events via HTTP server
- 📋 **Job Queue**: File-based job management with status tracking
- 📄 **Pipeline Parser**: Reads `.cicd.yml` configuration files
- ⚡ **Executor**: Runs pipeline steps using subprocess
- 📊 **Dashboard**: CLI interface to view jobs and logs

## Quick Start

### 1. Install Dependencies
```bash
pip install pymongo pyyaml requests
```

### 2. Run the CI/CD Server
```bash
python start_server.py
```

### 3. Test the Webhook
```bash
# In another terminal
python debug_test.py
```

### 4. View Jobs
```bash
# Show recent jobs
python simple_dashboard.py jobs

# Show logs for specific job
python simple_dashboard.py logs <job_id>
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
WEBHOOK_PORT=8080
GITHUB_SECRET=your_webhook_secret
WORKSPACE_DIR=./workspace
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GitHub Push    │───▶│ Webhook Listener │───▶│   Job Queue     │
│     Event       │    │  (http.server)  │    │  (jobs.json)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Dashboard    │◀───│   Executor      │◀───│ Pipeline Parser │
│   (CLI/Logs)    │    │ (subprocess)    │    │  (.cicd.yml)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Testing Commands

```bash
# Start server
python start_server.py

# Test webhook (in another terminal)
python debug_test.py

# Create job directly
python direct_test.py

# View jobs
python simple_dashboard.py jobs

# View specific job logs
python simple_dashboard.py logs <job_id>
```

## Project Structure

```
ci_server/
├── core/
│   ├── executor.py           # Pipeline execution engine
│   ├── file_queue.py         # File-based job queue
│   ├── pipeline_parser.py    # .cicd.yml parser & git operations
│   └── webhook_listener.py   # HTTP webhook server
├── models/
│   └── job.py               # Job data model
├── config/
│   └── settings.py          # Configuration settings
├── tests/
│   └── sample_files/        # Test data
├── start_server.py          # Main server entry point
├── simple_dashboard.py      # CLI dashboard
├── shared_queue.py          # Shared job queue instance
├── debug_test.py           # Webhook testing
├── direct_test.py          # Direct job creation test
├── jobs.json               # Persistent job storage (auto-created)
└── workspace/              # Git repositories (auto-created)
```

## Job Statuses

- `queued`: Job waiting to be processed
- `running`: Job currently executing
- `done`: Job completed successfully
- `failed`: Job failed during execution

## Files Created

- `jobs.json`: Persistent job storage
- `workspace/`: Temporary repository clones



## How It Works

### 1. **Webhook Flow**
```
GitHub Push → POST /webhook → Create Job → Save to jobs.json
```

### 2. **Execution Flow**
```
Executor polls jobs.json → Find queued job → git pull/clone → 
Read .cicd.yml → Run steps → Update status → Save logs
```

### 3. **Job States**
- `queued` → `running` → `done` or `failed`

## Troubleshooting

- **Repository not found**: Update test files to use real GitHub repos
- **No jobs found**: Jobs persist in `jobs.json` - check if file exists
- **Webhook not working**: Check server console for debug output
- **Git errors**: Ensure git is installed and accessible from command line

## Real GitHub Integration

1. **Expose server**: `ngrok http 8080`
2. **Add webhook**: GitHub repo → Settings → Webhooks → Add webhook
3. **URL**: `https://your-ngrok-url.ngrok.io/webhook`
4. **Content-type**: `application/json`
5. **Events**: Just push events