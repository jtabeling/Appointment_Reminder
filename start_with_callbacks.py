"""
Quick start script to run the app with status callbacks.
Requires ngrok to be running on port 8080.
"""

import sys
from pathlib import Path

# Check if ngrok is running
print("Checking for ngrok on port 8080...")
try:
    import urllib.request
    response = urllib.request.urlopen('http://localhost:8080', timeout=2)
    print("✓ ngrok is running")
except:
    print("✗ Error: ngrok is not running on port 8080")
    print("\nPlease start ngrok first:")
    print("  1. Run: ngrok http 8080")
    print("  2. Copy your HTTPS URL (e.g., https://abc123.ngrok.io)")
    print("  3. Update config/settings.yaml with the URL")
    print("  4. Run this script again")
    sys.exit(1)

# Import and run
from src.status_callback_handler import StatusCallbackServer
import threading
import time

# Start callback server in background
print("\nStarting status callback server...")
server = StatusCallbackServer(port=8080)
server_thread = threading.Thread(target=server.start, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)

print("✓ Callback server running")
print("\nNow starting app...\n")

# Run the app
if len(sys.argv) > 1:
    excel_file = sys.argv[1]
else:
    excel_file = 'data/batch_test.xlsx'

from src.app import AppointmentReminderApp

app = AppointmentReminderApp()
app.start()

try:
    app.run_interactive(excel_file)
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    app.stop()

