#!/usr/bin/env python3
import subprocess
import os

def simple_test():
    print("=== Simple CI/CD Test ===")
    
    # Test git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(f"Git: {result.stdout.strip()}")
    except:
        print("ERROR: Git not installed")
        return
    
    # Create workspace
    if not os.path.exists("workspace"):
        os.makedirs("workspace")
    
    # Test simple git clone
    test_path = "workspace/hello-test"
    if os.path.exists(test_path):
        subprocess.run(['rmdir', '/s', '/q', test_path], shell=True)
    
    print("Testing git clone...")
    try:
        result = subprocess.run([
            'git', 'clone', 
            'https://github.com/octocat/Hello-World.git', 
            test_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("SUCCESS: Git clone works!")
            
            # Test running commands in the repo
            print("Testing command execution...")
            cmd_result = subprocess.run(['dir'], shell=True, cwd=test_path, 
                                      capture_output=True, text=True)
            print(f"Command output: {cmd_result.stdout[:100]}...")
            
            # Cleanup
            subprocess.run(['rmdir', '/s', '/q', test_path], shell=True)
            print("System is ready!")
            
        else:
            print(f"FAILED: {result.stderr}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    simple_test()