"""
Simple TwiML server for Twilio callbacks.
Hosts an endpoint that Twilio can fetch to get call instructions.
"""

import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from typing import Optional

logger = logging.getLogger(__name__)


class TwiMLHandler(BaseHTTPRequestHandler):
    """HTTP handler for TwiML responses."""
    
    def do_GET(self):
        """Handle GET request from Twilio."""
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get message from query params or use default
            message = query_params.get('message', ['Default reminder message'])[0]
            
            # Generate TwiML
            twiml = self._generate_twiml(message)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml')
            self.end_headers()
            self.wfile.write(twiml.encode('utf-8'))
            
            logger.debug(f"Sent TwiML response for message: {message[:50]}...")
            
        except Exception as e:
            logger.error(f"Error handling TwiML request: {e}")
            self.send_error(500, str(e))
    
    def _generate_twiml(self, message: str) -> bytes:
        """Generate TwiML XML response.
        
        Args:
            message: Message to speak
            
        Returns:
            XML bytes for TwiML response
        """
        root = ET.Element('Response')
        
        # Say the message
        say1 = ET.SubElement(root, 'Say', {'voice': 'alice', 'language': 'en-US'})
        say1.text = message
        
        # Pause briefly
        ET.SubElement(root, 'Pause', {'length': '2'})
        
        # Say goodbye
        say2 = ET.SubElement(root, 'Say', {'voice': 'alice', 'language': 'en-US'})
        say2.text = 'Thank you, goodbye.'
        
        # Convert to string then bytes
        twiml_str = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root)
        return twiml_str
    
    def log_message(self, format, *args):
        """Override to use our logger instead of print."""
        logger.debug("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))


class TwiMLServer:
    """Simple TwiML server for development/testing."""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        """Initialize TwiML server.
        
        Args:
            host: Host address to bind to
            port: Port to bind to
        """
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
    
    def start(self):
        """Start the TwiML server."""
        self.server = HTTPServer((self.host, self.port), TwiMLHandler)
        logger.info(f"TwiML server started on http://{self.host}:{self.port}")
        
        # Run in background thread if needed
        # For now, just start it
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("TwiML server stopping...")
            self.stop()
    
    def stop(self):
        """Stop the TwiML server."""
        if self.server:
            self.server.shutdown()
            logger.info("TwiML server stopped")
    
    def get_url(self) -> str:
        """Get the URL for TwiML endpoint.
        
        Returns:
            URL string
        """
        return f"http://{self.host}:{self.port}/twiml"

