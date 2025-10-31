#!/usr/bin/env python3
"""
Test the contextual intelligence of the empathy rewriter
This should demonstrate the difference between removal and rewriting based on context
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the contextual analysis function
from app import analyze_message_context, generate_contextual_empathy_rewrite

def test_contextual_analysis():
    """Test the contextual intelligence with your exact example"""
    
    print("🧪 TESTING CONTEXTUAL EMPATHY REWRITER")
    print("="*70)
    
    # Your exact example
    messages = [
        "Hello team, hope everyone is doing well today!",
        "Great job on the presentation yesterday.",
        "You're an idiot and I hate working with you.",
        "Thanks for helping with the project.",
        "This is stupid and a waste of time.",
        "I appreciate everyone's collaboration."
    ]
    
    print("📋 ORIGINAL MESSAGES:")
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {msg}")
    
    print("\n🧠 CONTEXTUAL ANALYSIS:")
    print("-" * 70)
    
    # Test each potentially toxic message
    toxic_indices = [2, 4]  # "You're an idiot..." and "This is stupid..."
    
    for idx in toxic_indices:
        message = messages[idx]
        print(f"\nAnalyzing message {idx + 1}: '{message}'")
        
        # Test context analysis
        action = analyze_message_context(message, messages, idx)
        print(f"Context decision: {action.upper()}")
        
        # Test contextual rewrite
        result = generate_contextual_empathy_rewrite(message, messages, idx)
        print(f"Rewrite type: {result['type']}")
        print(f"Reason: {result['reason']}")
        if result['rewrite']:
            print(f"Suggested rewrite: '{result['rewrite']}'")
        else:
            print("Action: REMOVE from final text")
    
    print("\n🎯 EXPECTED BEHAVIOR:")
    print("Message 3 ('You're an idiot...'): Should be REMOVED (personal attack, out of context)")
    print("Message 5 ('This is stupid...'): Should be REWRITTEN (criticism of work content)")
    
    print("\n📝 RESULTING CLEANED TEXT SHOULD BE:")
    print("1. Hello team, hope everyone is doing well today!")
    print("2. Great job on the presentation yesterday.")
    print("3. [REMOVED - out of context personal attack]")
    print("4. Thanks for helping with the project.")
    print("5. [REWRITTEN] I have some concerns about this project approach that I'd like to discuss constructively.")
    print("6. I appreciate everyone's collaboration.")

if __name__ == "__main__":
    test_contextual_analysis()