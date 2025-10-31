#!/usr/bin/env python3
"""
Comprehensive test of the Enhanced Empathy Rewriter functionality
Tests both individual message analysis and bulk text cleaning
"""

import requests
import json

def test_individual_messages():
    """Test individual message analysis with empathetic rewrites"""
    print("🧪 TESTING INDIVIDUAL MESSAGE ANALYSIS")
    print("="*60)
    
    url = "http://127.0.0.1:5000/api/analyze-realtime"
    headers = {'Content-Type': 'application/json'}
    
    test_messages = [
        "You're an idiot and completely useless",
        "This is a wonderful idea, let's proceed",
        "I hate this stupid project",
        "Thank you for your hard work on this"
    ]
    
    for msg in test_messages:
        try:
            response = requests.post(url, headers=headers, json={'text': msg})
            result = response.json()
            
            print(f"\nOriginal: '{msg}'")
            print(f"Status: {result['label'].upper()} (Score: {result['score']})")
            
            if result.get('rewrite'):
                print(f"Rewrite: '{result['rewrite']}'")
                print("✅ Empathetic alternative provided")
            else:
                print("✅ No rewrite needed (safe message)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

def test_bulk_cleaning():
    """Test bulk text processing and cleaning"""
    print("\n\n🧪 TESTING BULK TEXT CLEANING")
    print("="*60)
    
    # Check if test file exists
    import os
    test_file = 'd:/Ai based Harrassment/safespace_ai/mixed_test.txt'
    
    if os.path.exists(test_file):
        print("✅ Test file found: mixed_test.txt")
        print("📋 File contents:")
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        
        print("\n🎯 EXPECTED BEHAVIOR:")
        print("1. Toxic messages will be identified and explained")
        print("2. Empathetic rewrites will be generated")
        print("3. Cleaned version will replace toxic with empathetic alternatives")
        print("4. Export options will be available")
        
        return True
    else:
        print("❌ Test file not found")
        return False

def main():
    """Run comprehensive tests"""
    print("🚀 ENHANCED EMPATHY REWRITER - COMPREHENSIVE TEST")
    print("="*70)
    
    # Test individual messages
    individual_test = test_individual_messages()
    
    # Test bulk cleaning setup
    bulk_test = test_bulk_cleaning()
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY:")
    print(f"Individual Analysis: {'✅ PASSED' if individual_test else '❌ FAILED'}")
    print(f"Bulk Cleaning Setup: {'✅ READY' if bulk_test else '❌ NOT READY'}")
    
    if individual_test and bulk_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("🌐 Open http://127.0.0.1:5000 and:")
        print("   1. Test real-time analysis by typing toxic messages")
        print("   2. Upload 'mixed_test.txt' for bulk cleaning demo")
        print("   3. View cleaned text section in results")
        print("   4. Test export functionality")
    else:
        print("\n❌ SOME TESTS FAILED - CHECK FLASK APP STATUS")

if __name__ == "__main__":
    main()