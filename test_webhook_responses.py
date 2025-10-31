"""
Quick test script to verify Flask webhook server is storing responses correctly.
Run this after a call to check if responses were captured.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from webhook_server import get_appointment_response
import json
from pathlib import Path

# Load responses from file
RESPONSES_FILE = Path(__file__).parent / 'logs' / 'webhook_responses.json'

print("=" * 60)
print("FLASK WEBHOOK RESPONSE TEST")
print("=" * 60)
print()

if RESPONSES_FILE.exists():
    try:
        with open(RESPONSES_FILE, 'r') as f:
            appointment_responses = json.load(f)
        
        if appointment_responses:
            print(f"Found {len(appointment_responses)} stored responses:\n")
            for call_sid, response_data in appointment_responses.items():
                print(f"Call SID: {call_sid}")
                print(f"  Response: {response_data.get('response', 'N/A')}")
                print(f"  Name: {response_data.get('name', 'N/A')}")
                print()
        else:
            print("Response file exists but is empty.")
    except Exception as e:
        print(f"Error reading response file: {e}")
else:
    print("No responses stored in webhook server.")
    print("\nPossible reasons:")
    print("  1. No calls have been answered yet")
    print("  2. Users haven't pressed 1 or 2")
    print("  3. Flask webhook server isn't receiving requests")
    print("  4. ngrok tunnel isn't working")
    print()

print("=" * 60)
print("To check a specific call ID from CSV:")
print("  python test_webhook_responses.py <call_sid>")
print("=" * 60)

# If call_sid provided as argument, check it
if len(sys.argv) > 1:
    call_sid = sys.argv[1]
    response = get_appointment_response(call_sid)
    print(f"\nResponse for {call_sid}:")
    print(f"  {response if response else 'Not found'}")

