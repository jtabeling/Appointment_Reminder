# Testing Interactive Confirmation

## ✅ Current Status: App Working in Non-Interactive Mode

Your app just successfully placed 2 calls using the existing Twilio Function endpoint.

## To Test Interactive Confirmation (Press 1 or 2)

### Option 1: Quick Test with ngrok (Recommended)

**Step 1: Start Webhook Server**
Open PowerShell/Terminal 1:
```bash
cd h:\Cursor\Appointment_Reminder
python src/webhook_server.py
```
You should see: `* Running on http://127.0.0.1:5000`

**Step 2: Start ngrok**
Open PowerShell/Terminal 2:
```bash
ngrok http 5000
```
Copy the HTTPS URL shown (e.g., `https://abc123-def456.ngrok.io`)

**Step 3: Update Settings**
Edit `config/settings.yaml`:
```yaml
calling:
  webhook_url: "https://abc123-def456.ngrok.io"  # Your ngrok URL
```

**Step 4: Run the App**
In Terminal 3:
```bash
python src/app.py data/ready_to_test.xlsx
```

**Step 5: Answer & Test**
- Answer the call
- Listen to the appointment message
- When prompted, **press 1** or **2** on your phone
- Check `logs/batch_call_results.csv` - you should see `confirmed` or `cancelled` in the `user_response` column

### Option 2: Test Webhook Locally (No Calls)

Just test the webhook endpoints:
```bash
# Terminal 1
python src/webhook_server.py

# Terminal 2
python test_webhook_server.py
```

## Expected Behavior

**Without webhook_url** (current):
- ✅ Calls placed successfully
- ✅ Message plays via Twilio Function
- ✅ No interactive prompts
- ✅ `user_response` column empty

**With webhook_url set**:
- ✅ Calls placed successfully
- ✅ Message plays
- ✅ **Prompt**: "Press 1 to confirm, 2 to cancel/reschedule"
- ✅ User presses key
- ✅ Confirmation message plays
- ✅ `user_response` column shows: `confirmed` or `cancelled`

## Current Test Results

App is working perfectly! Latest batch:
- 2 calls placed successfully
- Both calls reached "in-progress" or "ringing" status
- Results logged to CSV

Ready to test interactive mode when you:
1. Set up ngrok
2. Update `webhook_url` in settings.yaml

