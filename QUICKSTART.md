# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies (1 min)

```bash
python -m pip install -r requirements.txt
```

## Step 2: Configure Twilio (2 min)

1. Get your Twilio credentials from https://www.twilio.com/console
2. Create `.env` file:
```bash
echo "TWILIO_ACCOUNT_SID=your_sid_here" > .env
echo "TWILIO_AUTH_TOKEN=your_token_here" >> .env
echo "TWILIO_PHONE_NUMBER=+1234567890" >> .env
```

## Step 3: Quick Test (2 min)

```bash
# Create sample data
python create_sample_excel.py

# Run the app
python src/app.py data/sample_appointments.xlsx
```

⚠️ **Note**: For actual calling, you must set up a TwiML endpoint first! See SETUP_GUIDE.md.

---

## What's Happening?

The app will:
1. Read appointments from Excel
2. Schedule reminder calls (24h before each appointment)
3. Wait and automatically place calls when due
4. Log everything to `logs/appointment_reminder.log`

---

## Next Steps

For production use:
1. Set up TwiML endpoint (see SETUP_GUIDE.md)
2. Create your real Excel file
3. Test with your phone number
4. Deploy!

---

**Detailed Setup**: See `SETUP_GUIDE.md` for comprehensive instructions.

