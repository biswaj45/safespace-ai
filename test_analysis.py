#!/usr/bin/env python3
import requests
import json

# Test the real-time analysis endpoint
url = "http://127.0.0.1:5000/api/analyze-realtime"
headers = {'Content-Type': 'application/json'}

# Test messages
test_messages = [
    "Hello world",
    "You are stupid",
    "That's a great idea",
    "I hate this"
]

print("Testing analysis endpoint...")
for message in test_messages:
    data = {'text': message}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\nMessage: '{message}'")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - make sure Flask app is running")
        break
    except Exception as e:
        print(f"❌ Error: {e}")