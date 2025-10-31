# Quick Test: Interactive Confirmation

## Prerequisites

✅ Flask installed (check: `pip list | grep flask`)  
✅ ngrok installed (download from https://ngrok.com/download if needed)

## Step 1: Start Webhook Server

Open **Terminal 1**:

```bash
cd h:\Cursor\Appointment_Reminder
python src/webhook_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Keep this terminal open!**

## Step 2: Start ngrok

Open **Terminal 2** (new terminal):

```bash
ngrok http 5000
```

You should see something like:
```
Forwarding  https://abc123-def456.ngrok.io -> http://localhost:5000
```

**Copy the HTTPS URL** (e.g., `https://abc123-def456.ngrok.io`)  
**Keep this terminal open!**

## Step 3: Update Configuration

Edit `config/settings.yaml`:

```yaml
calling:
  webhook_url: "https://abc123-def456.ngrok.io"  # Your ngrok URL
```

## Step 4: Test the Webhook (Optional)

Open **Terminal 3** (optional - just to verify webhook works):

```bash
cd h:\Cursor\Appointment_Reminder
python test_webhook_server.py
```

This will test the webhook endpoints locally.

## Step 5: Run the App

In Terminal 3 (or a new terminal):

```bash
cd h:\Cursor\Appointment_Reminder
python src/app.py data/ready_to_test.xlsx
```

## Step 6: Answer the Call

When you receive the call:

1. **Listen** to the appointment reminder message
2. **Wait** for the prompt: "Press 1 to confirm your appointment, or press 2 to cancel or reschedule"
3. **Press 1** or **2** on your phone keypad
4. **Listen** to the confirmation or cancellation message

## Step 7: Check Results

After the call completes, check `logs/batch_call_results.csv`:

```bash
cat logs/batch_call_results.csv | tail -2
```

Look for the `user_response` column:
- `confirmed` - if you pressed 1
- `cancelled` - if you pressed 2
- Empty - if no response

## Troubleshooting

### "Cannot connect to webhook"
- Make sure webhook server is running (Terminal 1)
- Check ngrok is running (Terminal 2)
- Verify URL in settings.yaml matches ngrok URL exactly

### "Could not fetch user response"
- Wait a few seconds after call completes
- Check webhook server logs in Terminal 1
- Verify call_id is being passed correctly

### User response not in CSV
- Check that webhook_url is set in settings.yaml
- Verify ngrok is forwarding correctly
- Check webhook server received the request (look at Terminal 1)

## What to Expect

✅ **Call is placed** - You receive the call  
✅ **Message plays** - Appointment reminder with location  
✅ **Prompt appears** - "Press 1 to confirm..."  
✅ **You press 1 or 2** - On phone keypad  
✅ **Confirmation plays** - "Thank you. Your appointment is confirmed..."  
✅ **CSV updated** - `user_response` column shows 'confirmed' or 'cancelled'

## Testing Without ngrok (Local Only)

If you just want to test the webhook server code (not actual calls):

```bash
# Terminal 1
python src/webhook_server.py

# Terminal 2
python test_webhook_server.py
```

This will test the endpoints locally without needing ngrok or actual phone calls.

