"""
Test script to verify batch logging functionality.
Creates a test Excel file and runs the app to generate batch logs.
"""

import pandas as pd
from datetime import datetime

# Create a simple test file
now = datetime.now()
test_appointments = [
    {
        'name': 'Test Batch 1',
        'phone_number': '443-506-3813',
        'email': 'test1@example.com',
        'appointment_date': now
    },
    {
        'name': 'Test Batch 2',
        'phone_number': '443-506-3813',
        'email': 'test2@example.com',
        'appointment_date': now
    },
]

df = pd.DataFrame(test_appointments)
df.to_excel('data/batch_test.xlsx', index=False)

print("Created test file: data/batch_test.xlsx")
print("Run: python src/app.py data/batch_test.xlsx")
print("Check: logs/batch_call_results.csv")

