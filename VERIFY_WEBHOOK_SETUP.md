# Verify Flask Webhook Setup

## Current Configuration ✅

Your `config/settings.yaml` shows:
```yaml
webhook_url: "https://umbellated-subgelatinously-faith.ngrok-free.dev"
```

This is correctly configured!

## Required: Both Services Running

For user responses to be tracked in CSV, you need:

### 1. Flask Webhook Server Running
**Terminal 1** should show:
```
* Running on http://127.0.0.1:5000
```

If not running:
```bash
python src/webhook_server.py
```

### 2. ngrok Running
**Terminal 2** should show:
```
Forwarding  https://umbellated-subgelatinously-faith.ngrok-free.dev -> http://localhost:5000
```

If not running:
```bash
C:\ngrok.exe http 5000
```

## Verify Setup

### Check Webhook is Accessible

Open browser or run:
```bash
curl https://umbellated-subgelatinously-faith.ngrok-free.dev/voice
```

Should return TwiML XML (this is normal).

### Check App is Using Webhook

When you run the app, check the logs:
```bash
findstr "interactive webhook" logs\appointment_reminder.log
```

Should show: `Using interactive webhook: https://umbellated-subgelatinously-faith.ngrok-free.dev/voice`

## Expected Behavior

**With Flask webhook running:**
- ✅ App uses your Flask server (not Twilio Function)
- ✅ Interactive prompts work (Press 1/2)
- ✅ User responses logged to CSV (`confirmed` or `cancelled`)

**Without Flask webhook running:**
- ✅ App falls back to Twilio Function
- ✅ Interactive prompts still work (Press 1/2)
- ❌ User responses NOT logged to CSV (shows empty)

## Next Test

Make sure both services are running, then:
```bash
python src/app.py data/ready_to_test.xlsx
```

After answering and pressing 1 or 2:
```bash
python view_call_results.py --limit 3
```

You should see `confirmed` or `cancelled` in `user_response` column!

