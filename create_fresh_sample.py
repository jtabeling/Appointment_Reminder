"""
Script to create a fresh sample Excel file with appointments in the future.
"""

import pandas as pd
from datetime import datetime, timedelta

# Create fresh sample data with future appointments
now = datetime.now()
sample_appointments = [
    {
        'name': 'Test User',
        'phone_number': 'your_cell_phone_here',  # User will update this
        'email': 'test@example.com',
        'appointment_date': now + timedelta(days=1) + timedelta(hours=2)  # Tomorrow + 2 hours
    },
    {
        'name': 'Test User 2',
        'phone_number': 'your_cell_phone_here',
        'email': 'test2@example.com',
        'appointment_date': now + timedelta(days=2)  # Day after tomorrow
    },
]

# Create DataFrame
df = pd.DataFrame(sample_appointments)

# Save to Excel file
output_file = 'data/sample_appointments.xlsx'
df.to_excel(output_file, index=False)

print(f"Created fresh sample Excel file: {output_file}")
print(f"File contains {len(df)} sample appointments")
print("\nNext step: Update the phone numbers in data/sample_appointments.xlsx with your cell phone")

