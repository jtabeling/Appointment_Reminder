"""
Data processor for reading and validating Excel appointment files.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


class Appointment:
    """Represents a single appointment."""
    
    def __init__(
        self,
        name: str,
        phone_number: str,
        email: str,
        appointment_datetime: datetime,
        row_index: Optional[int] = None
    ):
        """Initialize appointment.
        
        Args:
            name: Patient/taxpayer name
            phone_number: Contact phone number
            email: Contact email address
            appointment_datetime: Date and time of appointment
            row_index: Original row number in Excel file (for tracking)
        """
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.appointment_datetime = appointment_datetime
        self.row_index = row_index
    
    def __repr__(self) -> str:
        return f"Appointment(name={self.name}, datetime={self.appointment_datetime})"


class DataProcessor:
    """Processes Excel files containing appointment data."""
    
    def __init__(
        self,
        required_columns: Optional[List[str]] = None,
        date_format: str = "%Y-%m-%d %H:%M",
        fallback_date_format: str = "%m/%d/%Y %H:%M"
    ):
        """Initialize data processor.
        
        Args:
            required_columns: List of required column names
            date_format: Expected date format in Excel
            fallback_date_format: Alternative date format to try
        """
        self.required_columns = required_columns or [
            'name', 'phone_number', 'email', 'appointment_date'
        ]
        self.date_format = date_format
        self.fallback_date_format = fallback_date_format
    
    def read_excel(self, file_path: str, sheet_name: Optional[str] = None) -> List[Appointment]:
        """Read appointments from Excel file.
        
        Args:
            file_path: Path to Excel file
            sheet_name: Name of sheet to read (None for first sheet)
            
        Returns:
            List of Appointment objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing or data is invalid
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        logger.info(f"Reading Excel file: {file_path}")
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded {len(df)} rows from Excel file")
            
            # Handle case where pd.read_excel returns a dict (multiple sheets)
            if isinstance(df, dict):
                # Use first sheet if multiple sheets found
                sheet_key = list(df.keys())[0]
                logger.info(f"Multiple sheets found, using: {sheet_key}")
                df = df[sheet_key]
            
            # Normalize column names (lowercase, strip whitespace)
            df.columns = df.columns.str.lower().str.strip()
            logger.debug(f"Columns found: {list(df.columns)}")
            
            # Validate required columns
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Process each row
            appointments = []
            for idx, row in df.iterrows():
                try:
                    appointment = self._parse_row(row, idx + 2)  # +2 for Excel row number (header + 0-index)
                    if appointment:
                        appointments.append(appointment)
                except Exception as e:
                    logger.warning(f"Error parsing row {idx + 2}: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(appointments)} appointments")
            return appointments
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            raise
    
    def _parse_row(self, row: pd.Series, row_index: int) -> Optional[Appointment]:
        """Parse a single row into an Appointment object.
        
        Args:
            row: Pandas Series representing a row
            row_index: Original row number in Excel
            
        Returns:
            Appointment object or None if parsing fails
        """
        try:
            # Extract basic fields
            name = str(row['name']).strip()
            phone_number = str(row['phone_number']).strip()
            email = str(row['email']).strip()
            
            # Parse appointment date
            appointment_datetime = self._parse_datetime(row['appointment_date'], row_index)
            
            # Validate required fields
            if not all([name, phone_number, email]):
                logger.warning(f"Row {row_index}: Missing required fields")
                return None
            
            if appointment_datetime is None:
                logger.warning(f"Row {row_index}: Could not parse appointment date")
                return None
            
            return Appointment(
                name=name,
                phone_number=phone_number,
                email=email,
                appointment_datetime=appointment_datetime,
                row_index=row_index
            )
            
        except Exception as e:
            logger.error(f"Error parsing row {row_index}: {e}")
            return None
    
    def _parse_datetime(self, value: Any, row_index: int) -> Optional[datetime]:
        """Parse datetime value from various formats.
        
        Args:
            value: Datetime value from Excel (could be string, datetime, etc.)
            row_index: Row number for error reporting
            
        Returns:
            Datetime object or None if parsing fails
        """
        # If already a datetime object
        if isinstance(value, datetime):
            return value
        
        # If it's a pandas Timestamp
        if pd.notna(value) and hasattr(value, 'to_pydatetime'):
            return value.to_pydatetime()
        
        # Convert to string and try parsing
        value_str = str(value).strip()
        
        if not value_str or value_str.lower() in ['nan', 'none', '']:
            return None
        
        # Try primary format
        try:
            return datetime.strptime(value_str, self.date_format)
        except ValueError:
            pass
        
        # Try fallback format
        try:
            return datetime.strptime(value_str, self.fallback_date_format)
        except ValueError:
            pass
        
        # Try pandas to_datetime (very flexible)
        try:
            result = pd.to_datetime(value)
            if pd.notna(result):
                return result.to_pydatetime()
        except Exception:
            pass
        
        logger.warning(f"Row {row_index}: Could not parse datetime: {value_str}")
        return None
    
    def get_upcoming_appointments(
        self,
        appointments: List[Appointment],
        hours_from_now: float = 24
    ) -> List[Appointment]:
        """Filter appointments to only upcoming ones within specified time window.
        
        Args:
            appointments: List of all appointments
            hours_from_now: How many hours ahead to look
            
        Returns:
            List of upcoming appointments
        """
        now = datetime.now()
        cutoff_time = now.replace(microsecond=0)
        
        upcoming = [
            apt for apt in appointments
            if apt.appointment_datetime >= cutoff_time
        ]
        
        logger.info(f"Found {len(upcoming)} upcoming appointments out of {len(appointments)} total")
        return upcoming

