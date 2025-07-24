#!/usr/bin/env python3
# Minimal working CI/CD test
import subprocess
import os
import json
from datetime import datetime

def run_minimal_pipeline():
    print("=== Minimal Pipeline Test ===")
    
    # 1. Clone repo
    repo_url = "https://github.com/octocat/Hello-World.git"
    workspace = "workspace/minimal-test"
    
    if os.path.exists(workspace):
        subprocess.run(['rmdir', '/s', '/q', workspace], shell=True)
    
    print("1. Cloning repository...")
    result = subprocess.run(['git', 'clone', repo_url, workspace], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"FAILED: {result.stderr}")
        return
    
    print("2. Repository cloned successfully!")
    
    # 2. Run simple pipeline steps
    steps = [
        {"name": "check_python", "run": "python --version"},
        {"name": "list_files", "run": "dir"},
        {"name": "test_echo", "run": "echo Hello CI/CD Pipeline!"}
    ]
    
    print("3. Running pipeline steps...")
    for i, step in enumerate(steps):
        print(f"   Step {i+1}: {step['name']}")
        
        result = subprocess.run(step['run'], shell=True, cwd=workspace,
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   SUCCESS: {result.stdout.strip()[:50]}...")
        else:
            print(f"   FAILED: {result.stderr.strip()}")
            break
    
    print("4. Pipeline completed!")
    
    # Cleanup
    subprocess.run(['rmdir', '/s', '/q', workspace], shell=True)

if __name__ == "__main__":
    run_minimal_pipeline()