#!/usr/bin/env python3
"""
Test smart empathy rewriting functionality
"""
import requests
import json

def test_smart_rewrite(message, expected_behavior):
    """Test a message and check smart rewriting behavior"""
    print(f"\n🔍 Testing: '{message}'")
    print(f"🎯 Expected: {expected_behavior}")
    print("=" * 70)
    
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
            
            # Check for rewrite
            if result.get('is_toxic', False):
                rewrite = result.get('rewrite')
                
                if rewrite:
                    print(f"\n✅ SMART REWRITE: \"{rewrite}\"")
                else:
                    print(f"\n🚫 NO REWRITE PROVIDED (purely derogatory)")
            else:
                print(f"\n✅ Message is SAFE - no rewrite needed")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Smart Empathy Rewriting")
    print("=" * 70)
    
    # Test cases with different behaviors expected
    test_cases = [
        # Mixed messages (should get partial rewrites)
        ("i am doing good. but you are behaving as shit.", "Partial rewrite - keep good part, fix 'shit'"),
        ("Hello there, you fucking idiot", "Partial rewrite - keep greeting, fix insult"),
        ("Thank you for your help, but you're acting like a moron", "Partial rewrite - keep thanks, fix 'moron'"),
        ("I appreciate your work, but stop being such an asshole", "Partial rewrite - keep appreciation, fix profanity"),
        
        # Purely derogatory (should get NO rewrite)
        ("go fuck yourself", "No rewrite - purely derogatory"),
        ("you are an idiot", "No rewrite - purely derogatory"),
        ("shut up bitch", "No rewrite - purely derogatory"),
        ("fucking moron", "No rewrite - purely derogatory"),
    ]
    
    for message, expected in test_cases:
        test_smart_rewrite(message, expected)
    
    print(f"\n🎯 Smart rewriting test completed!")