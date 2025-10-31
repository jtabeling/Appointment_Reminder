# System Patterns

## Architecture Overview
The system follows a modular architecture with clear separation of concerns:

1. **Data Processor**: Handles Excel file reading and validation
2. **Caller**: Manages Twilio integration and call placement
3. **Batch Logger**: Logs all call results to CSV
4. **Application**: Main entry point and orchestration

## Design Patterns

### Data Flow
```
Excel File (with location) → Data Processor → Appointments (with location) → Immediate Call (message includes location) → TwiML Function → Twilio → Phone → CSV Log (includes location)
```

### Error Handling
- Try-catch blocks around critical operations
- Graceful degradation on non-critical failures
- Comprehensive logging of all errors
- Retry logic for transient failures

### Configuration Management
- Environment variables for sensitive data (API keys)
- YAML/INI config files for user settings
- Default values for optional parameters

### Logging Pattern
- Separate log files for different components
- Timestamped entries with severity levels
- Rotating logs to prevent disk space issues
- Batch CSV export with full call details

## Key Components

### DataProcessor Class
- Reads Excel files
- Validates required columns (name, phone_number, email, appointment_date)
- Optional location column support
- Parses dates and times
- Returns structured appointment data with location

### Caller Class
- Authenticates with Twilio API
- Places phone calls via Twilio
- Uses TwiML Function for dynamic messages
- Handles call outcomes (answered, voicemail, failed)
- Retries on transient errors
- Supports immediate call mode only
- Optional status callback support

### BatchLogger Class
- Logs all call results to CSV
- Includes location data in CSV output
- Tracks call outcomes (answered, duration, status)
- Formatted output for easy analysis
- Timestamp and batch tracking

### App Class
- Coordinates all components
- Loads configuration
- Initializes modules
- Places all calls immediately on launch
- Provides CLI interface
- Exports batch results to CSV

