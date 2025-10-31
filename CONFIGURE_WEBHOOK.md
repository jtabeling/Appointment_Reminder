# How to Configure the Webhook URL

## Quick Overview

The webhook URL allows Twilio to send interactive confirmation prompts to your Flask server. You need:
1. **Flask webhook server running** (receives Twilio callbacks)
2. **ngrok running** (exposes local server to internet)
3. **URL in settings.yaml** (tells app where webhook is)

## Step-by-Step Instructions

### Step 1: Start the Webhook Server

Open **PowerShell Terminal 1**:

```bash
cd h:\Cursor\Appointment_Reminder
python src/webhook_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://[::]:5000
```

**Keep this terminal open!** The server must stay running.

### Step 2: Install/Start ngrok

**If you don't have ngrok:**

1. Download from: https://ngrok.com/download
2. Extract the `.exe` file
3. Add to PATH or use full path

**Start ngrok** - Open **PowerShell Terminal 2** (new terminal):

```bash
ngrok http 5000
```

You'll see output like:
```
ngrok                                                                 

Session Status                online
Account                       (your account)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123-def456.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the HTTPS forwarding URL** (e.g., `https://abc123-def456.ngrok-free.app`)

**Keep this terminal open too!** ngrok must stay running while testing.

### Step 3: Update settings.yaml

Edit `config/settings.yaml`:

**Find this line** (around line 20):
```yaml
  webhook_url: null
```

**Change it to** (use your ngrok URL):
```yaml
  webhook_url: "https://abc123-def456.ngrok-free.app"
```

**Save the file.**

### Step 4: Verify Configuration

The app will automatically use the `/voice` endpoint, so you can use just the base ngrok URL.

Your `config/settings.yaml` should look like:
```yaml
calling:
  # ... other settings ...
  webhook_url: "https://your-ngrok-url.ngrok-free.app"
```

### Step 5: Test It

Now run the app:
```bash
python src/app.py data/ready_to_test.xlsx
```

When you receive the call:
- ✅ You'll hear the appointment message
- ✅ You'll hear: "Press 1 to confirm your appointment, or press 2 to cancel or reschedule"
- ✅ Press 1 or 2 on your phone
- ✅ You'll hear the confirmation or cancellation message

Check `logs/batch_call_results.csv` - the `user_response` column will show:
- `confirmed` - if you pressed 1
- `cancelled` - if you pressed 2

## Troubleshooting

### "Cannot connect to webhook"
- ✅ Make sure webhook server is running (Terminal 1)
- ✅ Make sure ngrok is running (Terminal 2)
- ✅ Check ngrok URL matches exactly in settings.yaml
- ✅ Verify ngrok shows "Session Status: online"

### "Webhook not responding"
- Check webhook server terminal for errors
- Test webhook directly: Open browser to `https://your-ngrok-url.ngrok-free.app/voice`
- Should see TwiML XML (this is normal)

### "ngrok not working"
- Make sure port 5000 is not blocked by firewall
- Try stopping and restarting ngrok
- Check ngrok web interface: http://127.0.0.1:4040

### "user_response is empty"
- Wait 10-15 seconds after call completes
- Check webhook server logs for errors
- Verify call was answered (not voicemail)

## Alternative: Deploy to Production Server

Instead of ngrok, you can deploy `src/webhook_server.py` to:
- **Heroku** (free tier available)
- **PythonAnywhere** (free tier available)
- **AWS Lambda**
- **Google Cloud Run**
- **Your own server**

Then use your production URL in `settings.yaml`:
```yaml
webhook_url: "https://your-production-server.com"
```

## What Gets Configured

When you set `webhook_url`:

1. **App uses your Flask server** instead of Twilio Function
2. **Flask server receives calls** from Twilio
3. **Interactive prompts enabled** - Press 1 or 2
4. **Responses logged** to CSV file

When `webhook_url` is `null`:

1. **App uses Twilio Function** (existing endpoint)
2. **No interactive prompts** - just plays message
3. **user_response column empty** - no interaction tracked

## Quick Reference

```bash
# Terminal 1: Webhook Server
python src/webhook_server.py

# Terminal 2: ngrok
ngrok http 5000

# Terminal 3: Run App
python src/app.py data/ready_to_test.xlsx
```

**Settings file:**
- File: `config/settings.yaml`
- Line: ~20
- Format: `webhook_url: "https://your-url.ngrok-free.app"`

