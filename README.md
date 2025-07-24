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

## Job Statuses

- `queued`: Job waiting to be processed
- `running`: Job currently executing
- `done`: Job completed successfully
- `failed`: Job failed during execution

## Files Created

- `jobs.json`: Persistent job storage
- `workspace/`: Temporary repository clones

## GitHub Webhook Setup (Optional)

1. Expose local server using ngrok: `ngrok http 8080`
2. Go to GitHub repo → Settings → Webhooks
3. Add webhook: `http://your-ngrok-url.ngrok.io/webhook`
4. Set content type: `application/json`
5. Select "Push events"

## Troubleshooting

- **No jobs found**: Use `python simple_dashboard.py jobs` instead of `python dashboard.py jobs`
- **Webhook not working**: Check server console for debug output
- **Jobs not persisting**: Check if `jobs.json` file is created