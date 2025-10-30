"""Quick test script to place immediate calls."""

import subprocess
import sys

print("=" * 60)
print("TESTING APPOINTMENT REMINDER - IMMEDIATE CALL MODE")
print("=" * 60)
print()

# Run the app
print("Running application...")
result = subprocess.run(
    [sys.executable, 'src/app.py', 'data/ready_to_test.xlsx'],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

print()
print("=" * 60)
print("Test complete!")
print("=" * 60)
print()
print("Check logs/appointment_reminder.log for details")

