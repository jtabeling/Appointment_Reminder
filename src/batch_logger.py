"""
Batch call logger for tracking call results in CSV format.
Creates detailed logs of each batch of calls with results.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import logging


logger = logging.getLogger(__name__)


class BatchLogger:
    """Logs batch call results to CSV files."""
    
    def __init__(self, log_file: str = "logs/batch_call_results.csv"):
        """Initialize batch logger.
        
        Args:
            log_file: Path to CSV log file
        """
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize CSV file with headers if it doesn't exist."""
        if not self.log_file.exists():
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'batch_id',
                    'timestamp',
                    'name',
                    'phone_number',
                    'appointment_date',
                    'location',
                    'call_answered',
                    'call_status',
                    'call_duration_seconds',
                    'call_duration_formatted',
                    'call_id',
                    'error_message'
                ])
            logger.info(f"Initialized batch log file: {self.log_file}")
    
    def log_batch(
        self,
        batch_id: str,
        call_results: List[Dict[str, Any]]
    ):
        """Log a batch of call results.
        
        Args:
            batch_id: Unique identifier for this batch
            call_results: List of call result dictionaries with keys:
                - name: Person's name
                - phone_number: Phone number called
                - appointment_date: Appointment date/time
                - location: Appointment location (optional)
                - answered: Boolean indicating if call was answered
                - status: Call status from Twilio
                - duration: Duration in seconds
                - call_id: Twilio call ID
                - error: Error message if any
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            
            for result in call_results:
                # Format duration
                duration_seconds = result.get('duration', 0)
                duration_formatted = self._format_duration(duration_seconds)
                
                writer.writerow([
                    batch_id,
                    timestamp,
                    result.get('name', ''),
                    result.get('phone_number', ''),
                    result.get('appointment_date', ''),
                    result.get('location', ''),
                    'Yes' if result.get('answered', False) else 'No',
                    result.get('status', ''),
                    duration_seconds,
                    duration_formatted,
                    result.get('call_id', ''),
                    result.get('error', '')
                ])
        
        logger.info(f"Logged batch {batch_id} with {len(call_results)} calls to {self.log_file}")
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable format.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string (e.g., "2m 15s" or "45s")
        """
        if seconds is None or seconds == 0:
            return "0s"
        
        int_seconds = int(seconds)
        minutes, secs = divmod(int_seconds, 60)
        
        if minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    def get_recent_batches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent batch summaries.
        
        Args:
            limit: Maximum number of recent batches to return
            
        Returns:
            List of batch summaries
        """
        if not self.log_file.exists():
            return []
        
        batches = {}
        
        try:
            with open(self.log_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    batch_id = row['batch_id']
                    if batch_id not in batches:
                        batches[batch_id] = {
                            'batch_id': batch_id,
                            'timestamp': row['timestamp'],
                            'total_calls': 0,
                            'answered': 0,
                            'not_answered': 0,
                            'errors': 0
                        }
                    
                    batches[batch_id]['total_calls'] += 1
                    if row['call_answered'] == 'Yes':
                        batches[batch_id]['answered'] += 1
                    else:
                        batches[batch_id]['not_answered'] += 1
                    if row['error_message']:
                        batches[batch_id]['errors'] += 1
        
        except Exception as e:
            logger.error(f"Error reading batch log: {e}")
            return []
        
        # Return most recent batches
        sorted_batches = sorted(
            batches.values(),
            key=lambda x: x['timestamp'],
            reverse=True
        )
        
        return sorted_batches[:limit]

