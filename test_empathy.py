#!/usr/bin/env python3
import requests
import json

# Test the enhanced analysis endpoint with rewrites
url = "http://127.0.0.1:5000/api/analyze-realtime"
headers = {'Content-Type': 'application/json'}

# Test messages that should get rewrites
test_messages = [
    "You are so stupid!",
    "I hate this idea, it's terrible",
    "Shut up and go away",
    "THIS IS AWFUL!!!",
    "You always mess everything up",
    "Hello, how are you today?"  # Safe message for comparison
]

print("Testing enhanced analysis with empathy rewrites...")
for message in test_messages:
    data = {'text': message}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        print(f"\n{'='*60}")
        print(f"Original: '{message}'")
        print(f"Label: {result.get('label', 'N/A')} (Score: {result.get('score', 'N/A')})")
        
        if result.get('explanation'):
            print(f"Explanation: {result['explanation'][:80]}...")
        
        if result.get('rewrite'):
            print(f"Rewrite: '{result['rewrite']}'")
        else:
            print("No rewrite needed (message is safe)")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - make sure Flask app is running")
        break
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'='*60}")
print("Test completed!")