"""
Call handling module for placing automated calls via Twilio.
Provides abstraction for making reminder calls to taxpayers.
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
import phonenumbers
from phonenumbers import NumberParseException
import urllib.parse

try:
    from twilio.rest import Client as TwilioClient
    from twilio.base.exceptions import TwilioRestException
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Twilio not installed. Install with: pip install twilio")


logger = logging.getLogger(__name__)


class CallResult:
    """Represents the result of a call attempt."""
    
    def __init__(
        self,
        success: bool,
        call_id: Optional[str] = None,
        status: Optional[str] = None,
        duration: Optional[float] = None,
        error: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        """Initialize call result.
        
        Args:
            success: Whether the call was successfully placed
            call_id: Unique call ID from provider
            status: Call status (answered, busy, failed, etc.)
            duration: Call duration in seconds
            error: Error message if call failed
            timestamp: When the call was placed
        """
        self.success = success
        self.call_id = call_id
        self.status = status
        self.duration = duration
        self.error = error
        self.timestamp = timestamp or datetime.now()
    
    def __repr__(self) -> str:
        return f"CallResult(success={self.success}, status={self.status})"


class Caller:
    """Handles placing calls via Twilio."""
    
    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
        max_retries: int = 3,
        retry_delay: int = 300
    ):
        """Initialize caller with Twilio credentials.
        
        Args:
            account_sid: Twilio account SID
            auth_token: Twilio auth token
            from_number: Phone number to call from (Google Voice number)
            max_retries: Maximum retry attempts for failed calls
            retry_delay: Seconds to wait between retries
        """
        if not TWILIO_AVAILABLE:
            raise ImportError("Twilio library not installed")
        
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize Twilio client
        self.client = TwilioClient(account_sid, auth_token)
        
        logger.info(f"Initialized Twilio caller with number: {from_number}")
    
    def normalize_phone_number(self, phone_number: str) -> str:
        """Normalize phone number to E.164 format.
        
        Args:
            phone_number: Phone number in any format
            
        Returns:
            Phone number in E.164 format (e.g., +1234567890)
        """
        try:
            # Try to parse as US number first
            parsed = phonenumbers.parse(phone_number, "US")
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            pass
        
        try:
            # Try parsing without region
            parsed = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            pass
        
        logger.warning(f"Could not normalize phone number: {phone_number}")
        return phone_number
    
    def place_call(
        self,
        to_number: str,
        message: str,
        retry: bool = True
    ) -> CallResult:
        """Place a call to the specified number with the given message.
        
        Args:
            to_number: Phone number to call
            message: Message to speak during the call
            retry: Whether to retry on failure
            
        Returns:
            CallResult object with call outcome
        """
        to_number = self.normalize_phone_number(to_number)
        
        logger.info(f"Placing call to {to_number}")
        logger.debug(f"Message: {message}")
        
        attempt = 0
        last_error = None
        
        while attempt <= self.max_retries:
            try:
                # Create TwiML instructions for the call
                twiml_url = self._generate_twiml_url(message)
                
                # Place the call
                call = self.client.calls.create(
                    to=to_number,
                    from_=self.from_number,
                    url=twiml_url,
                    method='GET'
                )
                
                # Wait a moment for call to be initiated
                time.sleep(2)
                
                # Get call status
                call = self.client.calls(call.sid).fetch()
                
                result = CallResult(
                    success=True,
                    call_id=call.sid,
                    status=call.status,
                    duration=float(call.duration) if call.duration else None
                )
                
                logger.info(f"Call placed successfully: {call.sid}, status: {call.status}")
                return result
                
            except TwilioRestException as e:
                last_error = str(e)
                logger.error(f"Twilio error on attempt {attempt + 1}: {e}")
                
                if attempt < self.max_retries and retry:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    attempt += 1
                else:
                    break
            
            except Exception as e:
                last_error = str(e)
                logger.error(f"Unexpected error placing call: {e}")
                break
        
        # All attempts failed
        result = CallResult(
            success=False,
            error=last_error or "Unknown error"
        )
        
        logger.error(f"Failed to place call to {to_number} after {attempt + 1} attempts")
        return result
    
    def _generate_twiml_url(self, message: str) -> str:
        """Generate TwiML URL for text-to-speech.
        
        Note: For production, you should host your own TwiML endpoint using
        the TwiMLServer class or use Twilio Functions.
        
        Args:
            message: Message to speak
            
        Returns:
            URL with TwiML instructions
        """
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        
        # Using Twilio Function endpoint for appointment reminders
        twiml_url = f"https://appointmentreminder-1291.twil.io/path_1?message={encoded_message}"
        
        logger.info(f"Using Twilio Function: {twiml_url}")
        logger.debug(f"Message: {message[:100]}...")
        
        return twiml_url
    
    def get_call_status(self, call_id: str) -> Optional[CallResult]:
        """Get the status of a previously placed call.
        
        Args:
            call_id: Call SID from Twilio
            
        Returns:
            CallResult with current status
        """
        try:
            call = self.client.calls(call_id).fetch()
            
            result = CallResult(
                success=call.status in ['completed', 'in-progress'],
                call_id=call.sid,
                status=call.status,
                duration=float(call.duration) if call.duration else None
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching call status: {e}")
            return None

