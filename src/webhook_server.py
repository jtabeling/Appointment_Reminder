"""
Flask webhook server for Twilio callbacks with interactive appointment confirmation.
Handles TwiML generation with Gather verb for user input (1=confirm, 2=cancel/reschedule).
"""

import logging
import json
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from urllib.parse import unquote
import os
from pathlib import Path

logger = logging.getLogger(__name__)

app = Flask(__name__)

# File-based storage for responses (shared between Flask server and app)
RESPONSES_FILE = Path(__file__).parent.parent / 'logs' / 'webhook_responses.json'

def _load_responses():
    """Load responses from file."""
    if RESPONSES_FILE.exists():
        try:
            with open(RESPONSES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading responses: {e}")
    return {}

def _save_responses(responses):
    """Save responses to file."""
    try:
        RESPONSES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(RESPONSES_FILE, 'w') as f:
            json.dump(responses, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving responses: {e}")

# Load existing responses on startup
appointment_responses = _load_responses()


@app.route('/voice', methods=['GET', 'POST'])
def voice():
    """
    Main webhook endpoint for Twilio calls.
    Handles initial message and Gather input.
    """
    resp = VoiceResponse()
    
    try:
        # Log all incoming requests for debugging
        call_sid = request.values.get('CallSid', 'unknown')
        method = request.method
        all_keys = list(request.values.keys())
        logger.info(f"[{method}] /voice - CallSid: {call_sid}")
        logger.info(f"  Request keys: {all_keys}")
        
        # Check if this is a response to Gather (user pressed a key)
        if 'Digits' in request.values:
            choice = request.values.get('Digits', '')
            caller_name = request.values.get('CallerName', '')
            
            logger.info(f"✓ Received digit input: '{choice}' from call {call_sid}")
            
            if choice == '1':
                # User confirmed appointment
                resp.say(
                    "Thank you. Your appointment is confirmed. We look forward to seeing you. Goodbye.",
                    voice='alice',
                    language='en-US'
                )
                
                # Store response
                if call_sid in appointment_responses:
                    appointment_responses[call_sid]['response'] = 'confirmed'
                else:
                    appointment_responses[call_sid] = {'name': caller_name, 'response': 'confirmed'}
                _save_responses(appointment_responses)
                
                logger.info(f"Call {call_sid}: Appointment confirmed")
                
            elif choice == '2':
                # User wants to cancel/reschedule
                resp.say(
                    "Your appointment has been cancelled. Please contact us to reschedule if needed. Thank you. Goodbye.",
                    voice='alice',
                    language='en-US'
                )
                
                # Store response
                if call_sid in appointment_responses:
                    appointment_responses[call_sid]['response'] = 'cancelled'
                else:
                    appointment_responses[call_sid] = {'name': caller_name, 'response': 'cancelled'}
                _save_responses(appointment_responses)
                
                logger.info(f"Call {call_sid}: Appointment cancelled")
                
            else:
                # Invalid input - reprompt
                logger.warning(f"Call {call_sid}: Invalid digit received: '{choice}'")
                # Still store it for debugging
                appointment_responses[call_sid] = {'name': caller_name, 'response': f'invalid_{choice}'}
                _save_responses(appointment_responses)
                resp.say(
                    "Sorry, I didn't understand that choice.",
                    voice='alice',
                    language='en-US'
                )
                
                # Reprompt with Gather
                gather = Gather(
                    num_digits=1,
                    timeout=10,
                    action='/voice',  # Post back to same endpoint
                    method='POST'
                )
                gather.say(
                    "Press 1 to confirm your appointment, or press 2 to cancel or reschedule.",
                    voice='alice',
                    language='en-US'
                )
                resp.append(gather)
                
                # If user doesn't respond, end call
                resp.say(
                    "We didn't receive a response. Please contact us if you need to confirm or reschedule your appointment. Goodbye.",
                    voice='alice',
                    language='en-US'
                )
        else:
            # Initial call or Gather timeout (no Digits)
            if method == 'POST' and 'Digits' not in request.values:
                logger.info(f"POST without Digits - likely Gather timeout for call {call_sid}")
                # Store timeout response
                appointment_responses[call_sid] = {'name': request.values.get('CallerName', ''), 'response': 'timeout'}
                _save_responses(appointment_responses)
                resp.say(
                    "We didn't receive a response. Please contact us if you need to confirm or reschedule your appointment. Goodbye.",
                    voice='alice',
                    language='en-US'
                )
                return str(resp), 200, {'Content-Type': 'text/xml'}
            
            # Initial call - get message from query parameter
            message = request.values.get('message', '')
            
            # URL decode the message if needed
            if message:
                message = unquote(message)
            
            logger.info(f"Initial call received: {call_sid}, message length: {len(message)}")
            
            # Say the appointment reminder message
            if message:
                resp.say(message, voice='alice', language='en-US')
            
            # Pause briefly
            resp.pause(length=1)
            
            # Gather user input
            gather = Gather(
                num_digits=1,
                timeout=10,  # Wait up to 10 seconds for input
                action='/voice',  # Post back to same endpoint when digit is pressed
                method='POST'
            )
            gather.say(
                "Press 1 to confirm your appointment, or press 2 to cancel or reschedule.",
                voice='alice',
                language='en-US'
            )
            resp.append(gather)
            
            # Fallback if no input received
            resp.say(
                "We didn't receive a response. Please contact us if you need to confirm or reschedule your appointment. Goodbye.",
                voice='alice',
                language='en-US'
            )
        
        return str(resp), 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        logger.error(f"Error in voice webhook: {e}", exc_info=True)
        # Return error response
        resp = VoiceResponse()
        resp.say(
            "We're sorry, there was an error processing your request. Please contact us directly. Goodbye.",
            voice='alice',
            language='en-US'
        )
        return str(resp), 200, {'Content-Type': 'text/xml'}


@app.route('/status', methods=['POST'])
def status():
    """
    Optional status callback endpoint.
    Receives call status updates from Twilio.
    """
    try:
        call_sid = request.values.get('CallSid', 'unknown')
        call_status = request.values.get('CallStatus', 'unknown')
        logger.debug(f"Call status update: {call_sid} = {call_status}")
    except Exception as e:
        logger.error(f"Error in status callback: {e}")
    
    return '', 200


def get_appointment_response(call_sid: str):
    """
    Get the user's response for a specific call.
    
    Args:
        call_sid: Twilio Call SID
        
    Returns:
        Response dict with 'response' key ('confirmed', 'cancelled', or None)
    """
    # Always load fresh from file to get latest data
    responses = _load_responses()
    return responses.get(call_sid)


def clear_responses():
    """Clear all stored responses (useful for testing)."""
    global appointment_responses
    appointment_responses.clear()
    _save_responses({})
    logger.info("Cleared all appointment responses")


if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

