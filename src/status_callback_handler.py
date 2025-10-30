"""
Twilio Status Callback Handler for receiving call status updates.
Provides an HTTP server to receive and process Twilio status callbacks.
"""

import logging
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class StatusCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for Twilio status callbacks."""
    
    @staticmethod
    def set_status_store(store):
        """Set the shared status store for storing callbacks.
        
        Args:
            store: Dictionary to store call status updates
        """
        StatusCallbackHandler.status_store = store
    
    def do_POST(self):
        """Handle POST request from Twilio status callback."""
        try:
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            parsed_data = parse_qs(post_data)
            
            # Extract key fields
            call_sid = parsed_data.get('CallSid', [''])[0]
            call_status = parsed_data.get('CallStatus', [''])[0]
            call_duration = parsed_data.get('CallDuration', [''])[0]
            
            # Log the callback
            logger.info(f"Received status callback: CallSid={call_sid}, Status={call_status}, Duration={call_duration}")
            
            # Store the status
            if hasattr(StatusCallbackHandler, 'status_store'):
                StatusCallbackHandler.status_store[call_sid] = {
                    'status': call_status,
                    'duration': float(call_duration) if call_duration else None,
                    'timestamp': datetime.now(),
                    'raw_data': {k: v[0] if v else None for k, v in parsed_data.items()}
                }
            
            # Send success response to Twilio
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml')
            self.end_headers()
            self.wfile.write(b'<?xml version="1.0" encoding="UTF-8"?><Response></Response>')
            
            logger.debug(f"Sent 200 response for callback from {call_sid}")
            
        except Exception as e:
            logger.error(f"Error handling status callback: {e}")
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Override to use our logger instead of print."""
        logger.debug("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))


class StatusCallbackServer:
    """HTTP server for receiving Twilio status callbacks."""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize status callback server.
        
        Args:
            host: Host address to bind to
            port: Port to bind to
        """
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.status_store = {}
        
        # Set the status store for the handler
        StatusCallbackHandler.set_status_store(self.status_store)
    
    def start(self):
        """Start the status callback server."""
        self.server = HTTPServer((self.host, self.port), StatusCallbackHandler)
        logger.info(f"Status callback server started on http://{self.host}:{self.port}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Status callback server stopping...")
            self.stop()
    
    def stop(self):
        """Stop the status callback server."""
        if self.server:
            self.server.shutdown()
            logger.info("Status callback server stopped")
    
    def get_url(self) -> str:
        """Get the URL for status callbacks.
        
        Returns:
            URL string
        """
        return f"http://{self.host}:{self.port}/status"
    
    def get_status(self, call_sid: str) -> Optional[dict]:
        """Get the latest status for a call.
        
        Args:
            call_sid: Twilio Call SID
            
        Returns:
            Status dictionary or None if not found
        """
        return self.status_store.get(call_sid)

