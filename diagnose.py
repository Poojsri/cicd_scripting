#!/usr/bin/env python3
import subprocess
import os

def check_system():
    print("=== System Diagnostics ===")
    
    # Check Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(f"✅ Git: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Git not found - Install Git first!")
        return False
    
    # Check Python
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Python not found")
        return False
    
    # Check workspace
    workspace = "./workspace"
    if not os.path.exists(workspace):
        os.makedirs(workspace)
        print(f"✅ Created workspace: {workspace}")
    else:
        print(f"✅ Workspace exists: {workspace}")
    
    # Test git clone
    print("\n=== Testing Git Clone ===")
    test_repo = "https://github.com/octocat/Hello-World.git"
    test_path = "./workspace/test-clone"
    
    if os.path.exists(test_path):
        subprocess.run(['rmdir', '/s', '/q', test_path], shell=True, check=False)
    
    try:
        result = subprocess.run(['git', 'clone', test_repo, test_path], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Git clone works!")
            # Cleanup
            subprocess.run(['rmdir', '/s', '/q', test_path], shell=True, check=False)
            return True
        else:
            print(f"❌ Git clone failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Git clone error: {e}")
        return False

if __name__ == "__main__":
    if check_system():
        print("\n🎉 System ready for CI/CD pipeline!")
    else:
        print("\n🔧 Fix the issues above before running the pipeline")