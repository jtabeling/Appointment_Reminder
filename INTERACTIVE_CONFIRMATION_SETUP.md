# Interactive Appointment Confirmation Setup

## Overview

The appointment reminder system now supports **interactive confirmation** where recipients can press **1** to confirm their appointment or **2** to cancel/reschedule.

## How It Works

1. **Call is placed** with appointment reminder message
2. **After the message**, system prompts: "Press 1 to confirm your appointment, or press 2 to cancel or reschedule"
3. **User presses 1 or 2** on their phone keypad
4. **System responds** with confirmation or cancellation message
5. **Response is logged** in batch call results CSV

## Setup Instructions

### Option 1: Local Testing with ngrok (Recommended for Testing)

1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

2. **Start the webhook server** (in one terminal):
   ```bash
   python src/webhook_server.py
   ```
   Server will start on `http://localhost:5000`

3. **Set up ngrok** (in another terminal):
   ```bash
   ngrok http 5000
   ```
   Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

4. **Update config/settings.yaml**:
   ```yaml
   calling:
     webhook_url: "https://abc123.ngrok.io"
   ```

5. **Run the app**:
   ```bash
   python src/app.py data/ready_to_test.xlsx
   ```

### Option 2: Deploy to Production Server

1. **Deploy webhook_server.py** to your server (PythonAnywhere, Heroku, AWS, etc.)
2. **Update config/settings.yaml** with your server URL:
   ```yaml
   calling:
     webhook_url: "https://your-server.com"
   ```

3. **Run the app** as normal

### Option 3: Use Existing Twilio Function (Non-Interactive)

If you don't set `webhook_url`, the system falls back to your existing Twilio Function endpoint (non-interactive mode).

## Configuration

In `config/settings.yaml`:

```yaml
calling:
  # Webhook URL for interactive appointment confirmation (optional)
  # Set up Flask webhook server (see src/webhook_server.py) and use ngrok or deploy
  # Example: "https://abc123.ngrok.io" (will automatically use /voice endpoint)
  # If set, enables interactive prompts: Press 1 to confirm, 2 to cancel/reschedule
  webhook_url: null
```

## Features

### Interactive Prompts
- **Press 1**: Confirms appointment
  - System responds: "Thank you. Your appointment is confirmed. We look forward to seeing you. Goodbye."
- **Press 2**: Cancels/reschedules
  - System responds: "Your appointment has been cancelled. Please contact us to reschedule if needed. Thank you. Goodbye."

### Response Tracking
- User responses are logged in `logs/batch_call_results.csv`
- New column: `user_response`
  - `confirmed` - User pressed 1
  - `cancelled` - User pressed 2
  - Empty - No response or call not answered

### Fallback Handling
- If user doesn't press a key: "We didn't receive a response. Please contact us if you need to confirm or reschedule your appointment. Goodbye."
- If invalid key pressed: System reprompts for input
- If webhook not available: Falls back to non-interactive mode

## Testing

1. Set up webhook server with ngrok (see Option 1 above)
2. Update settings.yaml with ngrok URL
3. Run test:
   ```bash
   python src/app.py data/ready_to_test.xlsx
   ```
4. Answer the call when it comes in
5. Listen to the message
6. Press **1** or **2** when prompted
7. Check `logs/batch_call_results.csv` for `user_response` column

## Troubleshooting

### "Could not fetch user response"
- Webhook server might not be running
- Check that webhook_url in settings.yaml matches your ngrok/server URL
- Verify webhook server is accessible (test the URL in browser)

### User response not appearing in CSV
- Wait a few seconds after call completes for response to be logged
- Check webhook server logs for errors
- Verify call_id is being passed correctly

### Webhook server errors
- Check that Flask is installed: `pip install flask`
- Ensure port 5000 is not in use
- Review webhook server logs for detailed error messages

## Files Created/Modified

### New Files
- `src/webhook_server.py` - Flask server with Gather support
- `INTERACTIVE_CONFIRMATION_SETUP.md` - This file

### Modified Files
- `src/caller.py` - Added webhook_url support
- `src/app.py` - Fetches user responses from webhook
- `src/batch_logger.py` - Added user_response column
- `config/settings.yaml` - Added webhook_url configuration
- `requirements.txt` - Added flask dependency

## API Endpoints

### `/voice` (GET/POST)
- Main webhook endpoint for Twilio
- Handles initial message and Gather input
- Receives user keypad input (1 or 2)
- Returns TwiML responses

### `/status` (POST)
- Optional status callback endpoint
- Receives call status updates from Twilio

## Next Steps

1. Set up webhook server with ngrok or deploy to production
2. Update `config/settings.yaml` with webhook URL
3. Test with a real call
4. Monitor CSV logs for user responses

