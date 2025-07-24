#!/usr/bin/env python3
import requests
import json

def test_real_webhook():
    # Test with a real public repo
    payload = {
        "ref": "refs/heads/main", 
        "after": "main",  # Use branch name instead of commit
        "repository": {
            "clone_url": "https://github.com/octocat/Hello-World.git"
        },
        "commits": [{"message": "Test CI pipeline"}]
    }
    
    response = requests.post(
        'http://localhost:8080/webhook',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    print("Make sure server is running: python main.py both")
    print("Then run this test...")
    test_real_webhook()