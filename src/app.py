"""
Main application for Appointment Reminder System.
Coordinates all components and provides the main entry point.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import ConfigLoader
from logger import setup_logger
from data_processor import DataProcessor, Appointment
from caller import Caller, CallResult
from batch_logger import BatchLogger


class AppointmentReminderApp:
    """Main application class for appointment reminders."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the application.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = ConfigLoader(config_path)
        
        # Setup logging
        self.logger = setup_logger(
            log_file=self.config.get('logging.log_file', 'logs/appointment_reminder.log'),
            level=self.config.get('logging.log_level', 'INFO'),
            max_bytes=self.config.get('logging.max_log_size', 10485760),
            backup_count=self.config.get('logging.backup_count', 5)
        )
        
        self.logger.info("=" * 60)
        self.logger.info("Appointment Reminder System Starting")
        self.logger.info("=" * 60)
        
        # Initialize components
        self._init_data_processor()
        self._init_caller()
        self._init_batch_logger()
        
        # Statistics
        self.stats = {
            'calls_placed': 0,
            'calls_succeeded': 0,
            'calls_failed': 0,
            'appointments_processed': 0
        }
    
    def _init_data_processor(self):
        """Initialize data processor."""
        required_columns = self.config.get('data.required_columns', [
            'name', 'phone_number', 'email', 'appointment_date'
        ])
        date_format = self.config.get('data.date_format', "%Y-%m-%d %H:%M")
        fallback_format = self.config.get('data.fallback_date_format', "%m/%d/%Y %H:%M")
        
        self.data_processor = DataProcessor(
            required_columns=required_columns,
            date_format=date_format,
            fallback_date_format=fallback_format
        )
        
        self.logger.info("Data processor initialized")
    
    def _init_caller(self):
        """Initialize caller."""
        env_config = self.config.get('env', {})
        
        account_sid = env_config.get('twilio_account_sid')
        auth_token = env_config.get('twilio_auth_token')
        phone_number = env_config.get('twilio_phone_number')
        
        if not all([account_sid, auth_token, phone_number]):
            self.logger.error("Missing Twilio credentials. Check your .env file.")
            raise ValueError("Missing required Twilio configuration")
        
        max_retries = self.config.get('calling.max_retries', 3)
        retry_delay = self.config.get('calling.retry_delay_seconds', 300)
        status_callback_url = self.config.get('calling.status_callback_url')
        webhook_url = self.config.get('calling.webhook_url')
        
        self.caller = Caller(
            account_sid=account_sid,
            auth_token=auth_token,
            from_number=phone_number,
            max_retries=max_retries,
            retry_delay=retry_delay,
            status_callback_url=status_callback_url,
            webhook_url=webhook_url
        )
        if webhook_url:
            self.logger.info(f"Configured interactive webhook: {webhook_url}")
        
        self.logger.info("Caller initialized")
    
    def _init_batch_logger(self):
        """Initialize batch logger."""
        batch_log_file = self.config.get('logging.batch_log_file', 'logs/batch_call_results.csv')
        self.batch_logger = BatchLogger(log_file=batch_log_file)
        self.logger.info("Batch logger initialized")
    
    def load_appointments(self, file_path: str) -> List[Appointment]:
        """Load appointments from Excel file.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            List of Appointment objects
        """
        self.logger.info(f"Loading appointments from: {file_path}")
        
        try:
            appointments = self.data_processor.read_excel(file_path)
            self.logger.info(f"Loaded {len(appointments)} appointments")
            return appointments
        except Exception as e:
            self.logger.error(f"Error loading appointments: {e}")
            raise
    
    def place_calls(self, appointments: List[Appointment]) -> int:
        """Place calls for all appointments immediately.
        
        Args:
            appointments: List of appointments to call
            
        Returns:
            Number of calls successfully placed
        """
        self.logger.info(f"Placing {len(appointments)} calls now")
        
        calls_placed = 0
        message_template = self.config.get(
            'message.message_template',
            "Hello {name}, this is an automated reminder that you have an appointment scheduled for {appointment_date} at {appointment_time}{location_text}. If you need to reschedule, please contact us. Thank you."
        )
        
        # Track batch results for logging
        batch_results = []
        batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for apt in appointments:
            try:
                # Format message
                appointment_date = apt.appointment_datetime.strftime("%B %d, %Y")
                appointment_time = apt.appointment_datetime.strftime("%I:%M %p")
                location = apt.location or ""
                location_text = f", at the {location}" if location else ""
                
                message = message_template.format(
                    name=apt.name,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    location=location,
                    location_text=location_text
                )
                
                # Place the call immediately
                self.logger.info(f"Placing call to {apt.name}")
                try:
                    result = self.caller.place_call(
                        to_number=apt.phone_number,
                        message=message,
                        retry=True
                    )
                    
                    # Update statistics
                    self.stats['calls_placed'] += 1
                    if result.success:
                        self.stats['calls_succeeded'] += 1
                        self.logger.info(f"[OK] Call successful to {apt.name}: {result.status}")
                    else:
                        self.stats['calls_failed'] += 1
                        self.logger.error(f"[FAIL] Call failed to {apt.name}: {result.error}")
                    
                    # Try to get user response from webhook server if available
                    user_response = ''
                    if result.call_id and self.caller.webhook_url:
                        try:
                            from webhook_server import get_appointment_response
                            response_data = get_appointment_response(result.call_id)
                            if response_data:
                                user_response = response_data.get('response', '')
                                if user_response:
                                    self.logger.info(f"User response for {apt.name}: {user_response}")
                        except (ImportError, Exception) as e:
                            self.logger.debug(f"Could not fetch user response: {e}")
                    
                    # Track result for batch logging
                    batch_results.append({
                        'name': apt.name,
                        'phone_number': apt.phone_number,
                        'appointment_date': apt.appointment_datetime.isoformat(),
                        'location': apt.location or '',
                        'answered': self._is_call_answered(result.status),
                        'status': result.status,
                        'duration': result.duration,
                        'call_id': result.call_id,
                        'user_response': user_response,
                        'error': result.error
                    })
                    
                    calls_placed += 1
                except Exception as e:
                    self.logger.error(f"Error placing call to {apt.name}: {e}")
                    # Track error result
                    batch_results.append({
                        'name': apt.name,
                        'phone_number': apt.phone_number,
                        'appointment_date': apt.appointment_datetime.isoformat(),
                        'location': apt.location or '',
                        'answered': False,
                        'status': 'error',
                        'duration': 0,
                        'call_id': None,
                        'user_response': '',
                        'error': str(e)
                    })
                
            except Exception as e:
                self.logger.error(f"Error processing appointment for {apt.name}: {e}")
        
        # Wait for calls to complete, then fetch final status
        if batch_results:
            self.logger.info(f"Waiting for calls to complete before logging final results...")
            wait_time = 30 if self.caller.webhook_url else 10  # Longer wait if using interactive webhook
            self.logger.info(f"Waiting {wait_time} seconds (webhook: {'enabled' if self.caller.webhook_url else 'disabled'})")
            time.sleep(wait_time)  # Wait for calls to complete and user to respond
            
            # Update results with final status and user responses
            for result in batch_results:
                if result.get('call_id') and not result.get('error'):
                    try:
                        self.logger.info(f"Fetching final status for {result['name']}: call_id {result['call_id']}")
                        final_status = self.caller.get_call_status(result['call_id'])
                        if final_status:
                            old_status = result['status']
                            result['status'] = final_status.status
                            result['duration'] = final_status.duration
                            result['answered'] = self._is_call_answered(final_status.status)
                            self.logger.info(f"Updated {result['name']}: {old_status} -> {final_status.status}, duration: {final_status.duration}s")
                        else:
                            self.logger.warning(f"Could not fetch final status for {result['name']} - returned None")
                        
                        # Try to get user response if webhook is configured
                        if self.caller.webhook_url:
                            self.logger.debug(f"Webhook configured, attempting to fetch user response for {result['name']} (call_id: {result['call_id']})")
                            try:
                                import sys
                                from pathlib import Path
                                sys.path.insert(0, str(Path(__file__).parent))
                                from webhook_server import get_appointment_response
                                response_data = get_appointment_response(result['call_id'])
                                if response_data:
                                    user_response = response_data.get('response', '')
                                    if user_response:
                                        result['user_response'] = user_response
                                        self.logger.info(f"Updated {result['name']} user response: {user_response}")
                                    else:
                                        self.logger.debug(f"No user response found yet for {result['name']} (call_id: {result['call_id']})")
                                else:
                                    self.logger.debug(f"No response data found for {result['name']} (call_id: {result['call_id']})")
                            except (ImportError, Exception) as e:
                                self.logger.warning(f"Could not fetch user response for {result['name']}: {e}")
                        else:
                            self.logger.debug(f"No webhook configured, skipping user response fetch for {result['name']}")
                    except Exception as e:
                        self.logger.error(f"Error fetching final status for {result['name']}: {e}")
            
            # Log batch results
            self.batch_logger.log_batch(batch_id, batch_results)
            self.logger.info(f"Logged batch {batch_id} with {len(batch_results)} call results")
        
        self.logger.info(f"Placed {calls_placed} calls")
        return calls_placed
    
    def _is_call_answered(self, status: Optional[str]) -> bool:
        """Determine if a call was answered based on status.
        
        Args:
            status: Call status from Twilio
            
        Returns:
            True if answered, False otherwise
        """
        if not status:
            return False
        
        # Twilio call statuses that indicate answered
        answered_statuses = ['completed', 'answered', 'in-progress']
        return any(status.lower() in answered_statuses for answered_status in answered_statuses)
    
    def print_statistics(self):
        """Print statistics."""
        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)
        print(f"Total Calls Placed: {self.stats['calls_placed']}")
        print(f"Successful Calls: {self.stats['calls_succeeded']}")
        print(f"Failed Calls: {self.stats['calls_failed']}")
        print(f"Appointments Processed: {self.stats['appointments_processed']}")
        print("=" * 60 + "\n")
    
    def run(self, excel_file: str):
        """Run application with Excel file.
        
        Args:
            excel_file: Path to Excel file with appointments
        """
        try:
            # Load appointments
            appointments = self.load_appointments(excel_file)
            
            if not appointments:
                self.logger.warning("No appointments found")
                return
            
            # Place calls immediately
            calls_placed = self.place_calls(appointments)
            self.stats['appointments_processed'] = calls_placed
            
            self.print_statistics()
            
        except Exception as e:
            self.logger.error(f"Error in run: {e}", exc_info=True)
            raise


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Appointment Reminder System - Automated reminder calls via Twilio"
    )
    parser.add_argument(
        'excel_file',
        nargs='?',
        help='Path to Excel file with appointments'
    )
    parser.add_argument(
        '--config',
        default='config/settings.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    if not args.excel_file:
        print("Error: Excel file is required")
        parser.print_help()
        sys.exit(1)
    
    # Create app
    app = AppointmentReminderApp(config_path=args.config)
    
    try:
        app.run(args.excel_file)
    except Exception as e:
        app.logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        app.logger.info("Application completed")


if __name__ == '__main__':
    main()
