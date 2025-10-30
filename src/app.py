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
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import ConfigLoader
from logger import setup_logger
from data_processor import DataProcessor, Appointment
from scheduler import Scheduler
from caller import Caller, CallResult


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
        self._init_scheduler()
        self._init_apscheduler()
        
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
        
        self.caller = Caller(
            account_sid=account_sid,
            auth_token=auth_token,
            from_number=phone_number,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        self.logger.info("Caller initialized")
    
    def _init_scheduler(self):
        """Initialize scheduler."""
        reminder_hours = self.config.get('scheduling.reminder_hours_before', 24)
        self.scheduler = Scheduler(reminder_hours_before=reminder_hours)
        self.logger.info("Scheduler initialized")
    
    def _init_apscheduler(self):
        """Initialize APScheduler for periodic checks."""
        self.apscheduler = BackgroundScheduler()
        check_interval = self.config.get('scheduling.check_interval_minutes', 60)
        
        # Schedule periodic check for due calls
        self.apscheduler.add_job(
            self.process_due_calls,
            trigger=IntervalTrigger(minutes=check_interval),
            id='process_due_calls',
            name='Process Due Calls',
            replace_existing=True
        )
        
        self.logger.info(f"APScheduler initialized with {check_interval} minute interval")
    
    def load_appointments(self, file_path: str) -> List[Appointment]:
        """Load appointments from Excel file.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            List of Appointment objects
        """
        self.logger.info(f"Loading appointments from: {file_path}")
        
        call_immediately = self.config.get('scheduling.call_immediately', False)
        
        try:
            appointments = self.data_processor.read_excel(file_path)
            
            if call_immediately:
                # Don't filter - use all appointments
                self.logger.info(f"Loaded {len(appointments)} appointments (immediate mode - using all)")
                return appointments
            else:
                # Filter to upcoming appointments only
                upcoming = self.data_processor.get_upcoming_appointments(appointments)
                self.logger.info(f"Loaded {len(appointments)} total, {len(upcoming)} upcoming")
                return upcoming
            
        except Exception as e:
            self.logger.error(f"Error loading appointments: {e}")
            raise
    
    def schedule_appointments(self, appointments: List[Appointment]) -> int:
        """Schedule calls for all appointments.
        
        Args:
            appointments: List of appointments to schedule
            
        Returns:
            Number of appointments successfully scheduled
        """
        call_immediately = self.config.get('scheduling.call_immediately', False)
        
        if call_immediately:
            self.logger.info(f"Call immediately mode: Placing {len(appointments)} calls now")
        else:
            self.logger.info(f"Scheduling reminders for {len(appointments)} appointments")
        
        scheduled_count = 0
        message_template = self.config.get(
            'message.message_template',
            "Hello {name}, this is an automated reminder that you have an appointment scheduled for {appointment_date} at {appointment_time}. If you need to reschedule, please contact us. Thank you."
        )
        
        for apt in appointments:
            try:
                # Format message
                appointment_date = apt.appointment_datetime.strftime("%B %d, %Y")
                appointment_time = apt.appointment_datetime.strftime("%I:%M %p")
                
                message = message_template.format(
                    name=apt.name,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time
                )
                
                # Create appointment ID
                appointment_id = f"{apt.name}_{apt.appointment_datetime.isoformat()}"
                
                if call_immediately:
                    # Call immediately instead of scheduling
                    self.logger.info(f"Placing immediate call to {apt.name}")
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
                        
                        scheduled_count += 1
                    except Exception as e:
                        self.logger.error(f"Error placing call to {apt.name}: {e}")
                else:
                    # Schedule the call for later
                    scheduled = self.scheduler.schedule_appointment(
                        appointment_id=appointment_id,
                        phone_number=apt.phone_number,
                        name=apt.name,
                        message=message,
                        appointment_datetime=apt.appointment_datetime,
                        callback=lambda apt_id=appointment_id: self._place_reminder_call(apt_id)
                    )
                    
                    if scheduled:
                        scheduled_count += 1
                        self.logger.debug(f"Scheduled reminder for {apt.name}")
                
            except Exception as e:
                self.logger.error(f"Error processing appointment for {apt.name}: {e}")
        
        if call_immediately:
            self.logger.info(f"Placed {scheduled_count} immediate calls")
        else:
            self.logger.info(f"Scheduled {scheduled_count} reminder calls")
        return scheduled_count
    
    def _place_reminder_call(self, appointment_id: str) -> CallResult:
        """Place a reminder call (callback for scheduled calls).
        
        Args:
            appointment_id: Unique appointment identifier
            
        Returns:
            CallResult object
        """
        scheduled_call = self.scheduler.get_scheduled_call(appointment_id)
        if not scheduled_call:
            self.logger.error(f"Could not find scheduled call for {appointment_id}")
            return CallResult(success=False, error="Scheduled call not found")
        
        self.logger.info(f"Placing call to {scheduled_call.name} at {scheduled_call.phone_number}")
        
        # Place the call
        result = self.caller.place_call(
            to_number=scheduled_call.phone_number,
            message=scheduled_call.message,
            retry=True
        )
        
        # Update statistics
        self.stats['calls_placed'] += 1
        if result.success:
            self.stats['calls_succeeded'] += 1
        else:
            self.stats['calls_failed'] += 1
        
        # Log result
        if result.success:
            self.logger.info(
                f"✓ Call successful to {scheduled_call.name}: {result.status}"
            )
        else:
            self.logger.error(
                f"✗ Call failed to {scheduled_call.name}: {result.error}"
            )
        
        # Remove from scheduler after processing
        self.scheduler.remove_call(appointment_id)
        
        return result
    
    def process_due_calls(self):
        """Process all due calls (called periodically by APScheduler)."""
        self.logger.debug("Checking for due calls...")
        
        due_calls = self.scheduler.get_due_calls()
        
        if not due_calls:
            self.logger.debug("No calls are due")
            return
        
        self.logger.info(f"Processing {len(due_calls)} due calls")
        
        for scheduled_call in due_calls:
            try:
                self._place_reminder_call(scheduled_call.appointment_id)
            except Exception as e:
                self.logger.error(f"Error processing call for {scheduled_call.name}: {e}")
    
    def start(self):
        """Start the application."""
        self.logger.info("Starting appointment reminder system...")
        
        # Start APScheduler
        self.apscheduler.start()
        self.logger.info("APScheduler started")
        
        # Process any immediately due calls
        self.process_due_calls()
        
        self.logger.info("Application started successfully")
        self.print_status()
    
    def stop(self):
        """Stop the application."""
        self.logger.info("Stopping appointment reminder system...")
        
        if self.apscheduler.running:
            self.apscheduler.shutdown()
            self.logger.info("APScheduler stopped")
        
        self.print_statistics()
        self.logger.info("Application stopped")
    
    def print_status(self):
        """Print current status."""
        print("\n" + "=" * 60)
        print("APPOINTMENT REMINDER SYSTEM - STATUS")
        print("=" * 60)
        print(f"Total Scheduled Calls: {self.scheduler.count()}")
        
        upcoming = self.scheduler.get_upcoming_calls(limit=5)
        if upcoming:
            print("\nNext 5 Scheduled Calls:")
            for call in upcoming:
                print(f"  • {call.name}: {call.call_time.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("\nNo upcoming calls scheduled")
        
        print("=" * 60 + "\n")
    
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
    
    def run_interactive(self, excel_file: str):
        """Run application interactively with immediate processing.
        
        Args:
            excel_file: Path to Excel file with appointments
        """
        try:
            # Load appointments
            appointments = self.load_appointments(excel_file)
            
            if not appointments:
                self.logger.warning("No upcoming appointments found")
                return
            
            # Schedule them
            scheduled_count = self.schedule_appointments(appointments)
            self.stats['appointments_processed'] = scheduled_count
            
            self.print_status()
            
            # Keep running to process calls as they become due
            self.logger.info("Waiting for scheduled reminder times...")
            print("\nPress Ctrl+C to stop...")
            
            try:
                while True:
                    time.sleep(60)  # Check every minute
                    self.process_due_calls()
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt")
            
        except Exception as e:
            self.logger.error(f"Error in interactive mode: {e}", exc_info=True)
            raise
        finally:
            self.stop()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Appointment Reminder System - Automated reminder calls via Google Voice"
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
    
    # Create app
    app = AppointmentReminderApp(config_path=args.config)
    
    try:
        app.start()
        
        # If Excel file provided, process it
        if args.excel_file:
            app.run_interactive(args.excel_file)
        else:
            # Just run the scheduler
            print("\nNo Excel file provided. Running scheduler only...")
            print("Press Ctrl+C to stop...")
            
            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                pass
        
    except Exception as e:
        app.logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        app.stop()


if __name__ == '__main__':
    main()

