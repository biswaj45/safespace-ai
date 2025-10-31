#!/usr/bin/env python3
import requests
import json

# Test messages with mix of toxic and safe content
test_text = """Hello team, I hope everyone is doing well.
You are so stupid and incompetent at your job.
This project looks really promising, great work!
I hate this idea, it's completely terrible.
Thanks for the collaboration, looking forward to our next meeting.
Shut up and stop bothering me with this nonsense.
Your presentation was very informative and well-structured."""

print("Testing bulk analysis with mixed content...")
print("="*60)
print("ORIGINAL TEXT:")
print("="*60)
print(test_text)
print("="*60)

# Save to file and test bulk upload simulation
with open('d:/Ai based Harrassment/safespace_ai/mixed_test.txt', 'w', encoding='utf-8') as f:
    f.write(test_text)

print("Test file created: mixed_test.txt")
print("You can now upload this file through the web interface to see:")
print("1. Original toxic messages identified")
print("2. Explanations for why they're toxic")
print("3. Empathetic rewrites suggested")
print("4. Cleaned version with toxic messages replaced")
print("5. Export options for cleaned text")
print("\n✅ Ready for testing at http://127.0.0.1:5000")