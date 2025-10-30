"""
Script to create a sample Excel file for testing the appointment reminder system.
"""

import pandas as pd
from datetime import datetime, timedelta

# Create sample data
sample_appointments = [
    {
        'name': 'John Doe',
        'phone_number': '555-123-4567',
        'email': 'john.doe@example.com',
        'appointment_date': datetime.now() + timedelta(days=1)  # Tomorrow
    },
    {
        'name': 'Jane Smith',
        'phone_number': '555-987-6543',
        'email': 'jane.smith@example.com',
        'appointment_date': datetime.now() + timedelta(days=2)  # Day after tomorrow
    },
    {
        'name': 'Bob Johnson',
        'phone_number': '(555) 456-7890',
        'email': 'bob.johnson@example.com',
        'appointment_date': datetime.now() + timedelta(days=3)
    },
]

# Create DataFrame
df = pd.DataFrame(sample_appointments)

# Save to Excel file
output_file = 'data/sample_appointments.xlsx'
df.to_excel(output_file, index=False)

print(f"Created sample Excel file: {output_file}")
print(f"File contains {len(df)} sample appointments")
print("\nAppointments:")
for idx, row in df.iterrows():
    print(f"  {row['name']}: {row['appointment_date']}")

