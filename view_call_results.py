"""
Script to view batch call results in a readable format.
"""

import pandas as pd
from pathlib import Path
import sys

def view_results(csv_file='logs/batch_call_results.csv', limit=None):
    """Display call results in a readable format."""
    
    csv_path = Path(csv_file)
    
    if not csv_path.exists():
        print(f"Error: Log file not found: {csv_file}")
        return
    
    try:
        df = pd.read_csv(csv_path)
        
        if len(df) == 0:
            print("No call results found.")
            return
        
        print("=" * 100)
        print("BATCH CALL RESULTS")
        print("=" * 100)
        print()
        
        # Display summary
        print(f"Total Records: {len(df)}")
        print(f"Total Batches: {df['batch_id'].nunique()}")
        print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print()
        print("=" * 100)
        print()
        
        # Show latest entries
        display_df = df.tail(limit) if limit else df
        
        for idx, row in display_df.iterrows():
            print(f"Batch ID: {row['batch_id']}")
            print(f"Timestamp: {row['timestamp']}")
            print(f"  Name: {row['name']}")
            print(f"  Phone: {row['phone_number']}")
            print(f"  Appointment: {row['appointment_date']}")
            print(f"  Location: {row['location'] if pd.notna(row['location']) else 'N/A'}")
            print(f"  Call Status: {row['call_status']}")
            print(f"  Answered: {row['call_answered']}")
            print(f"  Duration: {row['call_duration_formatted']}")
            print(f"  User Response: {row['user_response'] if pd.notna(row['user_response']) and row['user_response'] else 'None (not using Flask webhook)'}")
            print(f"  Call ID: {row['call_id']}")
            if pd.notna(row['error_message']) and row['error_message']:
                print(f"  Error: {row['error_message']}")
            print()
            print("-" * 100)
            print()
        
        # Summary statistics
        print("=" * 100)
        print("SUMMARY STATISTICS")
        print("=" * 100)
        print()
        print(f"Total Calls: {len(df)}")
        print(f"Answered Calls: {len(df[df['call_answered'] == 'Yes'])}")
        print(f"Not Answered: {len(df[df['call_answered'] == 'No'])}")
        print(f"Completed Calls: {len(df[df['call_status'] == 'completed'])}")
        
        # Calculate average duration (handle numeric conversion)
        try:
            durations = pd.to_numeric(df['call_duration_seconds'], errors='coerce')
            avg_duration = durations.mean()
            if pd.notna(avg_duration):
                print(f"Average Duration: {avg_duration:.1f} seconds")
        except:
            pass
        
        # User responses (if using Flask webhook)
        if 'user_response' in df.columns:
            confirmed = len(df[df['user_response'] == 'confirmed'])
            cancelled = len(df[df['user_response'] == 'cancelled'])
            if confirmed > 0 or cancelled > 0:
                print()
                print("User Responses:")
                print(f"  Confirmed (Pressed 1): {confirmed}")
                print(f"  Cancelled (Pressed 2): {cancelled}")
        
        print()
        
    except Exception as e:
        print(f"Error reading log file: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='View batch call results')
    parser.add_argument(
        '--file',
        default='logs/batch_call_results.csv',
        help='Path to CSV log file'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Show only last N entries'
    )
    
    args = parser.parse_args()
    view_results(args.file, args.limit)

