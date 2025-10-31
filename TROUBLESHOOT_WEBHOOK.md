# Troubleshooting Flask Webhook User Responses

## Current Status

✅ **Webhook URL configured**: `https://umbellated-subgelatinously-faith.ngrok-free.dev`  
✅ **App detects webhook**: Shows "webhook: enabled" and waits 30 seconds  
✅ **Flask server running**: You confirmed both Flask and ngrok are running  
❓ **User responses not appearing in CSV**: Still showing "None (not using Flask webhook)"

## How It Works

1. **App places call** → Uses webhook URL to generate TwiML
2. **Twilio calls webhook** → Flask server receives request with message
3. **User presses 1 or 2** → Flask server stores response in memory
4. **App fetches response** → After 30 seconds, app queries Flask server for response
5. **Response logged to CSV** → Should show "confirmed" or "cancelled"

## Debugging Steps

### Step 1: Verify Flask Server is Receiving Requests

Check Flask server terminal for logs like:
```
Initial call received: CA..., message length: 123
Received digit input: 1 from call CA...
Call CA...: Appointment confirmed
```

**If no logs**: ngrok tunnel may not be working. Test with:
```bash
curl https://umbellated-subgelatinously-faith.ngrok-free.dev/voice
```

### Step 2: Check if Responses Are Being Stored

After a call completes, run:
```bash
python test_webhook_responses.py
```

This shows all stored responses in the Flask server memory.

### Step 3: Verify App is Fetching Responses

Check `logs/appointment_reminder.log` for:
- `"Configured interactive webhook: https://..."`
- `"Webhook configured, attempting to fetch user response..."`
- `"✓ Updated {name} user response: confirmed"` (or cancelled)

### Step 4: Check Call SID Matching

The Flask server stores responses by `CallSid`. The app fetches using `call_id` from Twilio. These should match.

To verify a specific call:
```bash
python test_webhook_responses.py CAa31b67b413c4b6edc2dfffee4eb34046
```

## Common Issues

### Issue 1: Responses Not Stored

**Symptom**: Flask server shows "Received digit input" but test script shows no responses

**Cause**: Response storage code not executing

**Fix**: Check Flask server logs for errors

### Issue 2: App Can't Import webhook_server

**Symptom**: Log shows "Could not fetch user response: No module named 'webhook_server'"

**Cause**: Import path issue

**Fix**: Already fixed in latest code - import uses `sys.path.insert`

### Issue 3: Timing Issue

**Symptom**: User presses 1/2 but response not captured

**Cause**: App checks too early (before user responds)

**Fix**: Wait time increased to 30 seconds. User should respond within 10 seconds of prompt.

### Issue 4: Call SID Mismatch

**Symptom**: Response stored but app can't find it

**Cause**: Call SID from Twilio doesn't match CallSid from webhook

**Fix**: Both should use same identifier. Check logs to compare.

## Next Test

1. **Start Flask server** (if not running):
   ```bash
   python src/webhook_server.py
   ```

2. **Start ngrok** (if not running):
   ```bash
   ngrok http 5000
   ```

3. **Run app**:
   ```bash
   python src/app.py data/ready_to_test.xlsx
   ```

4. **Answer call and press 1 or 2**

5. **Check responses**:
   ```bash
   python test_webhook_responses.py
   ```

6. **Check CSV**:
   ```bash
   python view_call_results.py --limit 3
   ```

## Expected Log Output

```
INFO - Configured interactive webhook: https://umbellated-subgelatinously-faith.ngrok-free.dev
INFO - Waiting 30 seconds (webhook: enabled)
DEBUG - Webhook configured, attempting to fetch user response for Mary Smith (call_id: CA...)
INFO - ✓ Updated Mary Smith user response: confirmed
```

If you see this, it's working! 🎉

