# Step-by-Step: Setup Flask Webhook to Track User Responses

## Goal
Enable CSV tracking of user responses (Press 1 = confirmed, Press 2 = cancelled)

## Prerequisites
✅ ngrok configured (you already did this!)
✅ Flask installed (already in requirements.txt)

## Step 1: Start Webhook Server

**Open Terminal 1 (PowerShell):**

```bash
cd h:\Cursor\Appointment_Reminder
python src/webhook_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://[::]:5000
```

**Keep this terminal open!** Don't close it.

**Or use the batch file:**
```bash
START_WEBHOOK_SETUP.bat
```

## Step 2: Start ngrok

**Open Terminal 2 (new PowerShell window):**

```bash
C:\ngrok.exe http 5000
```

You'll see output like:
```
Forwarding  https://abc123-def456.ngrok-free.app -> http://localhost:5000
```

**Copy the HTTPS URL** (the `https://abc123-def456.ngrok-free.app` part)

**Keep this terminal open too!**

## Step 3: Update settings.yaml

**Edit:** `config/settings.yaml`

**Find line 20:**
```yaml
webhook_url: null
```

**Change to** (use your ngrok URL):
```yaml
webhook_url: "https://abc123-def456.ngrok-free.app"
```

**Save the file.**

## Step 4: Test

**Open Terminal 3 (or use existing):**

```bash
python src/app.py data/ready_to_test.xlsx
```

## Step 5: Answer and Test

When you receive the call:
1. Listen to appointment message
2. Press **1** or **2** when prompted
3. Wait for confirmation message

## Step 6: Check CSV Log

After the call, check `logs/batch_call_results.csv`:

```bash
python view_call_results.py --limit 3
```

You should now see in the `user_response` column:
- `confirmed` - if you pressed 1
- `cancelled` - if you pressed 2

## Important Notes

### Keep Both Running
- **Terminal 1**: Webhook server must stay running
- **Terminal 2**: ngrok must stay running
- **Terminal 3**: Run the app

### ngrok URL Changes
⚠️ **Warning**: ngrok free URLs change each time you restart ngrok!

If you restart ngrok:
1. Get new URL
2. Update `config/settings.yaml` again
3. Restart webhook server if needed

### Port 5000
Make sure port 5000 isn't blocked by firewall or in use by another app.

## Troubleshooting

### "Cannot connect to webhook"
- ✅ Check webhook server is running (Terminal 1)
- ✅ Check ngrok is running (Terminal 2)
- ✅ Verify URL in settings.yaml matches ngrok exactly
- ✅ Test webhook directly: Open browser to `https://your-ngrok-url.ngrok-free.app/voice`

### "user_response still empty"
- Wait 10-15 seconds after call completes
- Check webhook server terminal for errors
- Verify call was answered (not voicemail)
- Check that webhook_url is set (not null) in settings.yaml

### Webhook server errors
- Check Flask is installed: `pip install flask`
- Check port 5000 is available
- Look at webhook server terminal for error messages

## What Changes

**Before (Twilio Function):**
- ✅ Interactive prompts work (Press 1/2)
- ❌ User responses NOT tracked in CSV

**After (Flask Webhook):**
- ✅ Interactive prompts work (Press 1/2)
- ✅ User responses tracked in CSV (`confirmed` or `cancelled`)

## Quick Command Reference

```bash
# Terminal 1: Webhook Server
python src/webhook_server.py

# Terminal 2: ngrok
C:\ngrok.exe http 5000

# Terminal 3: Run App
python src/app.py data/ready_to_test.xlsx

# View Results
python view_call_results.py --limit 5
```

## Verification

After setup, when you check the CSV:
- `user_response` column will show: `confirmed` or `cancelled`
- Not empty like before!

