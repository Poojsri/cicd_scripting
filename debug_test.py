#!/usr/bin/env python3
import requests
import json

def debug_webhook():
    # Use the sample webhook data
    with open('tests/sample_files/github_webhook.json', 'r') as f:
        payload = json.load(f)
    
    print("Sending webhook...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        'http://localhost:8080/webhook',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    debug_webhook()