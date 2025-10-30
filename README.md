# Appointment Reminder System

Automated appointment reminder system that calls taxpayers to remind them of their scheduled appointments using a Google Voice number via Twilio.

## Features

- **Excel Integration**: Reads appointments from Excel files (.xls/.xlsx)
- **Automated Calling**: Places reminder calls via Twilio/Google Voice
- **Smart Scheduling**: Configurable reminder timing (default: 24 hours before)
- **Comprehensive Logging**: Detailed logs of all operations
- **Error Handling**: Robust error handling and retry logic
- **Phone Validation**: Automatic phone number normalization

## Prerequisites

- Python 3.8 or higher
- Twilio account with a phone number (Google Voice integration)
- Excel files with appointment data

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

3. Configure your environment:
   - Copy `env_example.txt` to `.env`
   - Fill in your Twilio credentials:
```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

4. Update configuration (optional):
   - Edit `config/settings.yaml` to adjust settings

## Excel File Format

Your Excel file must contain the following columns:
- **name**: Taxpayer/patient name
- **phone_number**: Contact phone number
- **email**: Email address
- **appointment_date**: Date and time of appointment

Example:

| name          | phone_number | email              | appointment_date     |
|---------------|--------------|--------------------|---------------------|
| John Doe      | 555-123-4567 | john@example.com   | 2025-11-01 14:30    |
| Jane Smith    | 555-987-6543 | jane@example.com   | 2025-11-02 10:00    |

## Usage

### Basic Usage

Run the application with an Excel file:
```bash
python src/app.py path/to/appointments.xlsx
```

### Running as Service

Start the application without an Excel file (will process previously scheduled appointments):
```bash
python src/app.py
```

### Configuration

Edit `config/settings.yaml` to customize:

**Scheduling:**
```yaml
scheduling:
  reminder_hours_before: 24  # Hours before appointment to call
  timezone: "America/New_York"
```

**Calling:**
```yaml
calling:
  max_retries: 3              # Retry attempts
  retry_delay_seconds: 300    # Seconds between retries
```

**Message Template:**
```yaml
message:
  message_template: "Hello {name}, this is an automated reminder that you have an appointment scheduled for {appointment_date} at {appointment_time}..."
```

## Project Structure

```
Appointment_Reminder/
├── config/
│   └── settings.yaml          # Configuration file
├── data/                      # Input Excel files (create as needed)
├── logs/                      # Log files (auto-generated)
├── memory-bank/               # Project documentation
├── src/
│   ├── app.py                # Main application
│   ├── caller.py             # Twilio calling logic
│   ├── config_loader.py      # Configuration management
│   ├── data_processor.py     # Excel file processing
│   ├── logger.py             # Logging setup
│   ├── scheduler.py          # Call scheduling
│   └── twiml_server.py       # TwiML endpoint (optional)
├── requirements.txt           # Python dependencies
├── env_example.txt           # Environment template
└── README.md                  # This file
```

## Twilio Setup

### Getting Started with Twilio

1. Create a Twilio account at https://www.twilio.com
2. Get your Account SID and Auth Token from the dashboard
3. Purchase a phone number or use your Google Voice number
4. Add credentials to `.env` file

### TwiML Endpoint

The application needs a TwiML endpoint that Twilio can call. You have several options:

**Option 1: Use ngrok for local testing**
```bash
pip install pyngrok
# Run ngrok to expose local server
# Update caller.py with your ngrok URL
```

**Option 2: Host your own endpoint**
- Deploy the `twiml_server.py` to a public server
- Update `_generate_twiml_url()` in `src/caller.py`

**Option 3: Use Twilio Functions**
- Create a Twilio Function with TwiML
- Update `_generate_twiml_url()` with your function URL

## Logging

Logs are written to `logs/appointment_reminder.log` with rotation enabled.

Log levels:
- INFO: General operations
- DEBUG: Detailed debugging
- WARNING: Non-critical issues
- ERROR: Errors requiring attention

## Error Handling

- Invalid Excel files: Logged and skipped
- Missing columns: Raised immediately
- Failed calls: Retried up to 3 times
- Invalid phone numbers: Logged as warnings
- Past appointments: Skipped automatically

## Troubleshooting

**No calls being placed**
- Check Twilio credentials in `.env`
- Verify TwiML endpoint is accessible
- Check logs for error messages

**Excel file not loading**
- Verify column names match exactly
- Check date format matches config
- Ensure file is not open in another program

**Calls failing**
- Verify Twilio account has credits
- Check phone number format
- Review Twilio dashboard for error details

## Contributing

This is a standalone application. To extend functionality:
1. Review `memory-bank/` for architecture
2. Follow existing patterns in `src/`
3. Update configuration as needed

## License

This project is provided as-is for internal use.

## Support

For issues or questions:
1. Check logs in `logs/appointment_reminder.log`
2. Review configuration in `config/settings.yaml`
3. Verify Twilio credentials and account status

## Notes

- Appointments in the past are automatically skipped
- Phone numbers are automatically normalized to E.164 format
- The scheduler checks for due calls every 60 minutes (configurable)
- All operations are logged for audit purposes

