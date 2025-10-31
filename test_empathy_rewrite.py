#!/usr/bin/env python3
"""
Test empathy rewriting functionality
"""
import requests
import json

def test_empathy_rewrite(message):
    """Test a toxic message and check if empathy rewrite is provided"""
    print(f"\n🔍 Testing empathy rewrite for: '{message}'")
    print("=" * 60)
    
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
            
            # Check for empathy rewrite
            if result.get('is_toxic', False):
                rewrite = result.get('rewrite')
                empathy_rewrite = result.get('empathy_rewrite') 
                suggestion = result.get('suggestion')
                
                print(f"\n💡 Empathy Rewrite Fields:")
                print(f"   - rewrite: {rewrite}")
                print(f"   - empathy_rewrite: {empathy_rewrite}")
                print(f"   - suggestion: {suggestion}")
                
                if rewrite:
                    print(f"\n✅ EMPATHY REWRITE: \"{rewrite}\"")
                else:
                    print(f"\n❌ NO EMPATHY REWRITE PROVIDED")
            else:
                print(f"\n✅ Message is SAFE - no rewrite needed")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Empathy Rewriting Feature")
    print("=" * 60)
    
    # Test toxic messages that should get empathy rewrites
    toxic_messages = [
        "i am doing good. but you are behaving as shit.",
        "you are an idiot and I hate you",
        "go fuck yourself you moron",
        "shut up you stupid bitch"
    ]
    
    for message in toxic_messages:
        test_empathy_rewrite(message)
    
    print(f"\n🎯 Empathy rewriting test completed!")