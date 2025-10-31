# Testing Instructions for Interactive Webhook

## Current Status

Based on the webhook output you provided:
- ✅ **Flask server is running** and receiving requests
- ✅ **Initial call (GET)** received at 09:39:41
- ⚠️ **POST request** received at 09:40:03 but **no `Digits` parameter**

## What This Means

The POST request without `Digits` indicates:
- The Gather verb timed out (after 10 seconds)
- User did not press 1 or 2 within the 10-second window
- OR user hung up before responding

## Next Test Steps

### 1. Run App Again
```bash
python src/app.py data/ready_to_test.xlsx
```

### 2. Watch Flask Server Terminal

You should see logs like:
```
[GET] /voice - CallSid: CA...
  Request keys: ['message', 'CallSid', 'From', ...]
Initial call received: CA..., message length: 123
```

When user presses 1 or 2, you should see:
```
[POST] /voice - CallSid: CA...
  Request keys: ['Digits', 'CallSid', ...]
✓ Received digit input: '1' from call CA...
Call CA...: Appointment confirmed
```

### 3. Check Response Storage

After call completes, run:
```bash
python test_webhook_responses.py
```

You should see stored responses if user pressed 1 or 2.

### 4. Verify CSV Logging

```bash
python view_call_results.py --limit 3
```

Look for `user_response` column showing `confirmed` or `cancelled`.

## Troubleshooting

### If No Digits Logged

**Possible causes:**
1. User hung up before prompt played
2. User didn't hear/understand the prompt
3. Gather timeout too short (currently 10 seconds)

**Solutions:**
- Increase Gather timeout in `webhook_server.py` (line ~120):
  ```python
  timeout=15  # Increase from 10 to 15 seconds
  ```
- Make prompt clearer/more explicit
- Test with your own phone number first

### If Digits Received But Not Stored

Check Flask server logs for errors. The updated code now:
- Logs all request parameters
- Stores invalid digits for debugging
- Stores timeout responses

### If Stored But Not in CSV

The app waits 30 seconds then fetches responses. Check `logs/appointment_reminder.log` for:
```
INFO - ✓ Updated {name} user response: confirmed
```

## Expected Complete Flow

1. **App places call** → Twilio calls Flask webhook
2. **Flask plays message** → "Hello Mary Smith..."
3. **Flask prompts** → "Press 1 to confirm..."
4. **User presses 1 or 2** → Flask logs and stores response
5. **App fetches response** → After 30 seconds, queries Flask server
6. **CSV updated** → Shows `confirmed` or `cancelled`

## Quick Test

To verify everything works:
1. Call your test number
2. Listen to full message
3. **Immediately press 1** (don't wait)
4. Check Flask server terminal for "✓ Received digit input: '1'"
5. Run `python test_webhook_responses.py` - should show response
6. Run `python view_call_results.py` - CSV should show `confirmed`

