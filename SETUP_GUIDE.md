# Setup Guide

Complete step-by-step guide to set up and run the Appointment Reminder System.

## Step 1: Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

## Step 2: Set Up Twilio Account

### 2.1 Create Twilio Account

1. Go to https://www.twilio.com
2. Sign up for a free trial account
3. Verify your email and phone number

### 2.2 Get Your Credentials

1. Log into Twilio Console
2. Copy your **Account SID** and **Auth Token**
3. Purchase a phone number (or configure Google Voice)

### 2.3 Configure Environment

1. Create a `.env` file in the project root:
```bash
cp env_example.txt .env
```

2. Edit `.env` with your credentials:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

## Step 3: Set Up TwiML Endpoint (IMPORTANT)

Twilio needs a public URL to fetch call instructions. Choose one option:

### Option A: Use ngrok (Quick Testing)

1. Install ngrok:
```bash
# Download from https://ngrok.com
# Or install via package manager
```

2. Start the TwiML server:
```bash
python -c "from src.twiml_server import TwiMLServer; s = TwiMLServer(); s.start()"
```

3. In another terminal, expose it with ngrok:
```bash
ngrok http 8000
```

4. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. Update `src/caller.py` line ~221:
```python
return "https://abc123.ngrok.io/twiml"  # Your ngrok URL
```

### Option B: Host on Your Server (Production)

1. Deploy `src/twiml_server.py` to your server
2. Make it accessible via public URL
3. Update `src/caller.py` with your URL

### Option C: Use Twilio Functions (Recommended for Production)

1. In Twilio Console, go to Functions
2. Create a new function with this code:
```javascript
exports.handler = function(context, event, callback) {
    const twiml = new Twilio.twiml.VoiceResponse();
    const message = event.message || 'This is your appointment reminder.';
    twiml.say({
        voice: 'alice',
        language: 'en-US'
    }, message);
    callback(null, twiml);
};
```

3. Deploy the function and copy its URL
4. Update `src/caller.py` to call your function URL

## Step 4: Prepare Your Excel File

### Create Sample Data (Optional)

```bash
python create_sample_excel.py
```

This creates `data/sample_appointments.xlsx` with test data.

### Excel Format Requirements

Required columns (case-insensitive):
- `name` - Patient/taxpayer name
- `phone_number` - Contact number
- `email` - Email address
- `appointment_date` - Date and time

### Date Formats Supported

- `%Y-%m-%d %H:%M` (e.g., "2025-11-01 14:30")
- `%m/%d/%Y %H:%M` (e.g., "11/01/2025 02:30 PM")
- Excel datetime format

## Step 5: Run the Application

### First Run

```bash
python src/app.py data/sample_appointments.xlsx
```

### Check the Output

You should see:
```
============================================================
APPOINTMENT REMINDER SYSTEM - STATUS
============================================================
Total Scheduled Calls: 3

Next 5 Scheduled Calls:
  • John Doe: 2025-10-31 09:20
  • Jane Smith: 2025-11-01 09:20
  • Bob Johnson: 2025-11-02 09:20
============================================================
```

### Monitor Logs

Watch the log file for activity:
```bash
tail -f logs/appointment_reminder.log
```

## Step 6: Verify It Works

### Test With a Real Number

1. Update sample Excel with your phone number
2. Set appointment time to 5 minutes from now
3. Set `reminder_hours_before: 0` in `config/settings.yaml`
4. Run the application
5. You should receive a call!

## Troubleshooting

### "No module named 'twilio'"

```bash
python -m pip install -r requirements.txt
```

### "Missing Twilio credentials"

- Check that `.env` file exists in project root
- Verify credentials are correct
- No extra spaces or quotes

### "TwiML URL returned invalid XML"

- Ensure TwiML endpoint is publicly accessible
- Test URL in browser - should return XML
- Check ngrok URL is correct

### "Could not normalize phone number"

- Phone number format issues
- Add country code (e.g., +1 for US)
- Check Excel file has valid numbers

### "No calls being placed"

- Check appointment dates are in future
- Verify `reminder_hours_before` setting
- Review logs for errors

## Next Steps

1. Customize the message in `config/settings.yaml`
2. Adjust reminder timing to your needs
3. Set up the application to run as a service
4. Schedule periodic Excel file processing

## Production Deployment

For production use:

1. Use Twilio Functions for TwiML (Option C above)
2. Set up cron job to process Excel files regularly
3. Configure log rotation
4. Set up monitoring/alerting
5. Review Twilio rate limits and pricing
6. Ensure compliance with TCPA regulations

## Support

- Check logs: `logs/appointment_reminder.log`
- Review config: `config/settings.yaml`
- Twilio status: https://status.twilio.com
- Twilio docs: https://www.twilio.com/docs

