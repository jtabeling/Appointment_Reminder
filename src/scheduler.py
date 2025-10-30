"""
Scheduler for managing appointment reminder timing.
Coordinates when to place reminder calls.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Callable, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ScheduledCall:
    """Represents a call scheduled for a specific time."""
    
    appointment_id: str  # Unique identifier
    phone_number: str
    name: str
    message: str
    call_time: datetime
    appointment_datetime: datetime
    callback: Optional[Callable] = None  # Function to call when time arrives
    
    def __repr__(self) -> str:
        return f"ScheduledCall(name={self.name}, call_time={self.call_time})"


class Scheduler:
    """Manages scheduling of reminder calls."""
    
    def __init__(self, reminder_hours_before: int = 24):
        """Initialize scheduler.
        
        Args:
            reminder_hours_before: How many hours before appointment to place call
        """
        self.reminder_hours_before = reminder_hours_before
        self.scheduled_calls: List[ScheduledCall] = []
        logger.info(f"Initialized scheduler with {reminder_hours_before}h reminder window")
    
    def schedule_appointment(
        self,
        appointment_id: str,
        phone_number: str,
        name: str,
        message: str,
        appointment_datetime: datetime,
        callback: Optional[Callable] = None
    ) -> Optional[ScheduledCall]:
        """Schedule a reminder call for an appointment.
        
        Args:
            appointment_id: Unique ID for the appointment
            phone_number: Phone number to call
            name: Patient/taxpayer name
            message: Message to deliver during call
            appointment_datetime: When the appointment is
            callback: Function to call when reminder time arrives
            
        Returns:
            ScheduledCall object if scheduled, None if already past reminder time
        """
        # Calculate when to place the call
        call_time = appointment_datetime - timedelta(hours=self.reminder_hours_before)
        
        # Check if reminder time is in the past
        now = datetime.now()
        if call_time < now:
            logger.warning(
                f"Appointment {appointment_id} reminder time ({call_time}) is in the past. "
                f"Skipping scheduling."
            )
            return None
        
        # Check if already scheduled
        existing = self.get_scheduled_call(appointment_id)
        if existing:
            logger.debug(f"Appointment {appointment_id} already scheduled")
            return existing
        
        # Create scheduled call
        scheduled_call = ScheduledCall(
            appointment_id=appointment_id,
            phone_number=phone_number,
            name=name,
            message=message,
            call_time=call_time,
            appointment_datetime=appointment_datetime,
            callback=callback
        )
        
        self.scheduled_calls.append(scheduled_call)
        logger.info(f"Scheduled call for {name} at {call_time}")
        
        return scheduled_call
    
    def get_scheduled_call(self, appointment_id: str) -> Optional[ScheduledCall]:
        """Get a scheduled call by appointment ID.
        
        Args:
            appointment_id: Unique appointment identifier
            
        Returns:
            ScheduledCall if found, None otherwise
        """
        for call in self.scheduled_calls:
            if call.appointment_id == appointment_id:
                return call
        return None
    
    def get_due_calls(self, current_time: Optional[datetime] = None) -> List[ScheduledCall]:
        """Get all calls that are due (current time >= call time).
        
        Args:
            current_time: Time to check against (default: now)
            
        Returns:
            List of due calls
        """
        current_time = current_time or datetime.now()
        
        due_calls = [
            call for call in self.scheduled_calls
            if call.call_time <= current_time
        ]
        
        return due_calls
    
    def remove_call(self, appointment_id: str) -> bool:
        """Remove a scheduled call.
        
        Args:
            appointment_id: Unique appointment identifier
            
        Returns:
            True if removed, False if not found
        """
        initial_count = len(self.scheduled_calls)
        self.scheduled_calls = [
            call for call in self.scheduled_calls
            if call.appointment_id != appointment_id
        ]
        
        removed = len(self.scheduled_calls) < initial_count
        if removed:
            logger.info(f"Removed scheduled call for appointment {appointment_id}")
        
        return removed
    
    def get_upcoming_calls(self, limit: int = 10) -> List[ScheduledCall]:
        """Get the next N upcoming calls.
        
        Args:
            limit: Maximum number of calls to return
            
        Returns:
            List of upcoming calls, sorted by call time
        """
        now = datetime.now()
        upcoming = sorted(
            [call for call in self.scheduled_calls if call.call_time > now],
            key=lambda x: x.call_time
        )
        
        return upcoming[:limit]
    
    def get_all_scheduled(self) -> List[ScheduledCall]:
        """Get all scheduled calls.
        
        Returns:
            List of all scheduled calls
        """
        return self.scheduled_calls.copy()
    
    def clear_completed(self, current_time: Optional[datetime] = None) -> int:
        """Remove calls that have already passed.
        
        Args:
            current_time: Time to check against (default: now)
            
        Returns:
            Number of calls removed
        """
        current_time = current_time or datetime.now()
        initial_count = len(self.scheduled_calls)
        
        self.scheduled_calls = [
            call for call in self.scheduled_calls
            if call.call_time > current_time
        ]
        
        removed = initial_count - len(self.scheduled_calls)
        if removed > 0:
            logger.info(f"Cleared {removed} completed calls from scheduler")
        
        return removed
    
    def count(self) -> int:
        """Get total number of scheduled calls.
        
        Returns:
            Number of scheduled calls
        """
        return len(self.scheduled_calls)

