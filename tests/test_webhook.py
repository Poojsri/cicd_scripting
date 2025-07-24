#!/usr/bin/env python3
import json
import requests
import sys

def test_webhook():
    """Test webhook endpoint with sample GitHub payload"""
    
    # Load sample webhook data
    with open('tests/sample_files/github_webhook.json', 'r') as f:
        payload = json.load(f)
    
    # Send to webhook endpoint
    url = 'http://localhost:8080/webhook'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to webhook server. Is it running?")
        print("Start with: python main.py webhook")

if __name__ == "__main__":
    test_webhook()