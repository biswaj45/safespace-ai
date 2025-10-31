#!/usr/bin/env python3
"""
Quick test script for simplified Groq-only detection
"""
import requests
import json

def test_message(message, expected_toxic=None):
    """Test a message and show results"""
    print(f"\n🔍 Testing: '{message}'")
    print("=" * 50)
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/analyze-realtime',
            json={'message': message},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"🏷️  Classification: {result.get('label', 'unknown').upper()}")
            print(f"📊 Confidence: {result.get('confidence', 0):.3f}")
            print(f"📝 Explanation: {result.get('explanation', 'No explanation')}")
            print(f"🔧 Source: {result.get('source', 'unknown')}")
            
            if expected_toxic is not None:
                actual_toxic = result.get('is_toxic', False)
                if actual_toxic == expected_toxic:
                    print(f"✅ CORRECT: Expected {'TOXIC' if expected_toxic else 'SAFE'}")
                else:
                    print(f"❌ WRONG: Expected {'TOXIC' if expected_toxic else 'SAFE'}, got {'TOXIC' if actual_toxic else 'SAFE'}")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Simplified Groq-Only Detection")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        ("i am doing good. but you are behaving as shit.", True),
        ("hello, how are you today?", False),
        ("you are an idiot", True),
        ("thank you for your help", False),
        ("go fuck yourself", True),
        ("have a nice day", False)
    ]
    
    for message, expected in test_cases:
        test_message(message, expected)
    
    print(f"\n🎯 Testing completed!")