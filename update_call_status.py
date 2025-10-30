"""
Utility script to check and update call statuses in batch logs.
Use this if you want to check for completed calls after the batch runs.
"""

import csv
from pathlib import Path
from src.caller import Caller
from src.config_loader import ConfigLoader
import os
from dotenv import load_dotenv


def update_call_statuses():
    """Update call statuses in the batch log file."""
    load_dotenv()
    
    # Initialize
    config = ConfigLoader()
    batch_log_file = config.get('logging.batch_log_file', 'logs/batch_call_results.csv')
    
    env_config = config.get('env', {})
    caller = Caller(
        account_sid=env_config.get('twilio_account_sid'),
        auth_token=env_config.get('twilio_auth_token'),
        from_number=env_config.get('twilio_phone_number')
    )
    
    # Read current log
    log_path = Path(batch_log_file)
    if not log_path.exists():
        print(f"Log file not found: {batch_log_file}")
        return
    
    # Read all rows
    rows = []
    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Update status for each row
    updated = 0
    for row in rows:
        call_id = row.get('call_id')
        if not call_id:
            continue
        
        try:
            status = caller.get_call_status(call_id)
            if status:
                # Update row with latest status
                old_status = row['call_status']
                row['call_status'] = status.status
                row['call_duration_seconds'] = status.duration or 0
                
                # Format duration
                duration = status.duration or 0
                if duration >= 60:
                    minutes = int(duration // 60)
                    seconds = int(duration % 60)
                    row['call_duration_formatted'] = f"{minutes}m {seconds}s"
                else:
                    row['call_duration_formatted'] = f"{int(duration)}s"
                
                # Update answered status
                answered_statuses = ['completed', 'answered', 'in-progress']
                row['call_answered'] = 'Yes' if status.status in answered_statuses else 'No'
                
                if old_status != status.status:
                    print(f"Updated {row['name']}: {old_status} -> {status.status}, duration: {duration}s")
                    updated += 1
        except Exception as e:
            print(f"Error updating {row['name']}: {e}")
    
    # Write updated rows
    if updated > 0:
        with open(log_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nUpdated {updated} call statuses in {batch_log_file}")
    else:
        print("No updates needed")


if __name__ == '__main__':
    print("Updating call statuses...")
    update_call_statuses()
    print("Done!")

