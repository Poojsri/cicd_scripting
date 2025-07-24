#!/usr/bin/env python3
import subprocess
import os
import shutil

def working_pipeline():
    print("=== Working Pipeline Test ===")
    
    # Setup
    repo_url = "https://github.com/octocat/Hello-World.git"
    workspace = "workspace"
    repo_dir = os.path.join(workspace, "hello-world")
    
    # Create workspace
    os.makedirs(workspace, exist_ok=True)
    
    # Remove existing repo
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    
    print("1. Cloning repository...")
    result = subprocess.run(['git', 'clone', repo_url, repo_dir], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Clone failed: {result.stderr}")
        return False
    
    print("2. Repository cloned successfully!")
    
    # Run pipeline steps
    steps = [
        "python --version",
        "dir",
        "echo Pipeline works!"
    ]
    
    print("3. Running pipeline steps...")
    for i, cmd in enumerate(steps):
        print(f"   Step {i+1}: {cmd}")
        
        result = subprocess.run(cmd, shell=True, cwd=repo_dir,
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"   SUCCESS: {output[:50]}...")
        else:
            print(f"   FAILED: {result.stderr.strip()}")
            return False
    
    print("4. All steps completed successfully!")
    
    # Keep workspace for reuse
    print("5. Workspace preserved for next run")
    return True

if __name__ == "__main__":
    if working_pipeline():
        print("\nSUCCESS: Your system can run CI/CD pipelines!")
        print("The issue might be in the job queue or executor logic.")
    else:
        print("\nFAILED: System setup needs fixing.")