# Product Context: Appointment Reminder System

## Problem Being Solved
Tax offices need to reduce no-shows by sending automated appointment reminders to taxpayers. Manual reminders are time-consuming and error-prone. This system automates the process.

## Target Users
- Tax office staff who schedule appointments
- Administrative personnel managing appointment reminders

## User Experience Goals
1. Simple: Drop in an Excel file and let it run
2. Reliable: Calls are placed consistently without human intervention
3. Transparent: Clear logs showing what calls were made and results
4. Configurable: Adjust timing and other parameters as needed

## Key Features
- Bulk processing of appointments from Excel
- Automated scheduling of reminder calls
- Twilio/Voice integration for placing calls
- Custom TwiML messages with appointment details
- Immediate call mode for instant reminders
- Detailed logging and reporting
- Error recovery and retry logic
- Production ready deployment

## Workflow
1. User prepares Excel file with appointments
2. User runs the application
3. Application reads appointments and schedules calls
4. Calls are placed automatically (immediate or scheduled)
5. Custom messages delivered via TwiML Function
6. Results are logged for review
7. GitHub repository for version control and collaboration

