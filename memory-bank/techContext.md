# Technical Context

## Technology Stack
- **Language**: Python 3.8+
- **Excel Processing**: openpyxl or pandas
- **Google Voice**: twilio (primary) or pygooglevoice
- **Scheduling**: schedule library or APScheduler
- **Configuration**: configparser or YAML

## Dependencies
- pandas (Excel file reading)
- openpyxl (Excel file support)
- twilio or googlevoice (voice calling)
- schedule or APScheduler (task scheduling)
- python-dotenv (environment variables)

## Development Setup
1. Python 3.8 or higher required
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Google Voice credentials
4. Prepare Excel files in correct format

## Technical Constraints
- Must handle Excel file formats (.xls, .xlsx)
- Google Voice API limitations and rate limits
- Phone number format validation
- Time zone handling for appointments

## File Structure
```
Appointment_Reminder/
├── config/
│   └── settings.yaml
├── data/
│   └── (input Excel files)
├── logs/
│   └── (log files)
├── src/
│   ├── data_processor.py
│   ├── caller.py
│   ├── scheduler.py
│   └── app.py
├── requirements.txt
├── .env.example
└── README.md
```

