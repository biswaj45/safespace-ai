#!/usr/bin/env python3
"""
Debug the bulk analysis process to see why contextual logic isn't working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the analysis functions
from app import (
    classify_message_toxicity_with_explanation,
    generate_contextual_empathy_rewrite,
    analyze_message_context
)

def debug_bulk_analysis():
    """Debug the bulk analysis flow"""
    
    print("🔍 DEBUGGING BULK ANALYSIS FLOW")
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
    
    print("📋 MESSAGES:")
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {msg}")
    
    print("\n🔍 STEP-BY-STEP ANALYSIS:")
    print("-" * 70)
    
    for i, message in enumerate(messages, 1):
        print(f"\n📝 ANALYZING MESSAGE {i}: '{message}'")
        
        # Step 1: Basic toxicity classification
        classification = classify_message_toxicity_with_explanation(message)
        print(f"Basic classification: {classification['label']} (score: {classification['score']})")
        
        if classification["label"] == "toxic":
            print(f"🧠 APPLYING CONTEXTUAL ANALYSIS...")
            
            # Step 2: Contextual analysis
            action = analyze_message_context(message, messages, i-1)
            print(f"Context decision: {action}")
            
            # Step 3: Generate contextual rewrite
            contextual_result = generate_contextual_empathy_rewrite(message, messages, i-1)
            print(f"Contextual result: {contextual_result}")
            
            if contextual_result.get('type') == 'remove':
                print(f"🗑️ FINAL DECISION: REMOVE")
                print(f"Reason: {contextual_result.get('reason')}")
            else:
                print(f"✏️ FINAL DECISION: REWRITE")
                print(f"Rewrite: '{contextual_result.get('rewrite')}'")
                print(f"Reason: {contextual_result.get('reason')}")
        else:
            print(f"✅ SAFE MESSAGE - Keep as is")
    
    print("\n" + "="*70)
    print("🎯 EXPECTED OUTPUT FOR CLEANED TEXT:")
    print("1. Hello team, hope everyone is doing well today!")
    print("2. Great job on the presentation yesterday.")
    print("3. [REMOVED]")
    print("4. Thanks for helping with the project.")
    print("5. I have some concerns about this project approach that I'd like to discuss constructively.")
    print("6. I appreciate everyone's collaboration.")

if __name__ == "__main__":
    debug_bulk_analysis()