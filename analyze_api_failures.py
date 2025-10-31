#!/usr/bin/env python3
"""
SafeSpace.AI - API Failure Analysis Script
==========================================

This script analyzes the toxicity test results CSV to identify API failures,
patterns, and potential causes.
"""

import csv
import json
from datetime import datetime

def analyze_csv_failures(csv_file):
    """Analyze the CSV file for API failures and patterns"""
    
    print("🔍 Analyzing API Failures in Toxicity Test Results")
    print("=" * 60)
    
    total_messages = 0
    api_success_count = 0
    api_failure_count = 0
    rule_only_count = 0
    failures = []
    successes = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                total_messages += 1
                message_id = row.get('message_id', 'Unknown')
                message = row.get('message', '')[:50] + '...' if len(row.get('message', '')) > 50 else row.get('message', '')
                
                groq_is_toxic = row.get('groq_is_toxic', '')
                groq_reason = row.get('groq_reason', '')
                groq_tokens = row.get('groq_tokens', '0')
                processing_time = row.get('processing_time_seconds', '0')
                final_source = row.get('final_source', '')
                
                # Check for API failure indicators
                is_api_failure = (
                    groq_is_toxic == '' or 
                    groq_is_toxic == 'None' or
                    groq_reason == 'API call failed' or
                    groq_reason == 'No API key' or
                    groq_tokens == '0' or
                    final_source == 'rules'
                )
                
                if is_api_failure:
                    api_failure_count += 1
                    failures.append({
                        'id': message_id,
                        'message': message,
                        'groq_is_toxic': groq_is_toxic,
                        'groq_reason': groq_reason,
                        'groq_tokens': groq_tokens,
                        'final_source': final_source,
                        'processing_time': processing_time
                    })
                    
                    if final_source == 'rules':
                        rule_only_count += 1
                else:
                    api_success_count += 1
                    successes.append({
                        'id': message_id,
                        'tokens': int(groq_tokens) if groq_tokens.isdigit() else 0,
                        'time': float(processing_time) if processing_time.replace('.', '').isdigit() else 0
                    })
    
    except FileNotFoundError:
        print(f"❌ File {csv_file} not found!")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Calculate statistics
    success_rate = (api_success_count / total_messages * 100) if total_messages > 0 else 0
    failure_rate = (api_failure_count / total_messages * 100) if total_messages > 0 else 0
    
    print(f"📊 OVERALL STATISTICS")
    print(f"   Total Messages: {total_messages}")
    print(f"   API Successes: {api_success_count} ({success_rate:.1f}%)")
    print(f"   API Failures: {api_failure_count} ({failure_rate:.1f}%)")
    print(f"   Rule-only fallbacks: {rule_only_count}")
    print()
    
    # Analyze failure patterns
    if failures:
        print(f"🔴 API FAILURE ANALYSIS")
        print(f"   First 10 failures:")
        
        for i, failure in enumerate(failures[:10], 1):
            print(f"   {i}. ID #{failure['id']}: '{failure['message']}'")
            print(f"      Reason: {failure['groq_reason']}")
            print(f"      Source: {failure['final_source']}")
            print(f"      Tokens: {failure['groq_tokens']}")
            print()
    
    # Analyze success patterns
    if successes:
        avg_tokens = sum(s['tokens'] for s in successes) / len(successes)
        avg_time = sum(s['time'] for s in successes) / len(successes)
        
        print(f"✅ API SUCCESS ANALYSIS")
        print(f"   Average tokens per success: {avg_tokens:.1f}")
        print(f"   Average time per success: {avg_time:.2f}s")
        print()
    
    # Identify potential causes
    print(f"🔍 POTENTIAL FAILURE CAUSES")
    
    # Count different failure types
    empty_groq = sum(1 for f in failures if f['groq_is_toxic'] == '')
    api_call_failed = sum(1 for f in failures if f['groq_reason'] == 'API call failed')
    no_api_key = sum(1 for f in failures if f['groq_reason'] == 'No API key')
    rule_fallbacks = sum(1 for f in failures if f['final_source'] == 'rules')
    
    print(f"   Empty groq_is_toxic: {empty_groq}")
    print(f"   'API call failed': {api_call_failed}")
    print(f"   'No API key': {no_api_key}")
    print(f"   Rule fallbacks: {rule_fallbacks}")
    print()
    
    # Recommendations
    print(f"💡 RECOMMENDATIONS")
    if failure_rate > 50:
        print("   ⚠️  High failure rate detected!")
        if no_api_key > 0:
            print("   🔑 Check if GROQ_API_KEY is properly set")
        if api_call_failed > 0:
            print("   🌐 Check internet connection and API endpoint")
            print("   ⏱️  Consider increasing timeout values")
            print("   📊 Check if rate limits were exceeded")
        if rule_fallbacks > api_success_count:
            print("   🔄 System falling back to rules too often")
    else:
        print("   ✅ API performance looks good overall")
    
    print()
    print("🔧 DEBUGGING SUGGESTIONS")
    print("   1. Test a single API call manually")
    print("   2. Check Groq API dashboard for usage/errors")
    print("   3. Verify API key permissions")
    print("   4. Monitor rate limiting")
    print("   5. Check network connectivity")

def main():
    """Main analysis function"""
    
    # Find the most recent CSV file
    import os
    csv_files = [f for f in os.listdir('.') if f.startswith('toxicity_test_results_') and f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No toxicity test results CSV found!")
        return
    
    # Use the most recent file
    csv_file = sorted(csv_files)[-1]
    print(f"📁 Analyzing: {csv_file}")
    print()
    
    analyze_csv_failures(csv_file)

if __name__ == "__main__":
    main()