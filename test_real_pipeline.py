#!/usr/bin/env python3
import requests
import json

def test_your_repo():
    # Replace with your actual GitHub repo URL
    payload = {
        "ref": "refs/heads/main",
        "after": "main",  # Use branch name for testing
        "repository": {
            "clone_url": "https://github.com/YOUR_USERNAME/YOUR_REPO.git"  # Update this
        },
        "commits": [{"message": "Test CI pipeline"}]
    }
    
    try:
        response = requests.post(
            'http://localhost:8080/webhook',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Webhook Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\nSUCCESS! Job queued. Check dashboard:")
            print("python dashboard.py jobs")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure server is running: python start_server.py")

if __name__ == "__main__":
    print("Update the clone_url with your GitHub repo, then run this test")
    test_your_repo()