# System Patterns

## Architecture Overview
The system follows a modular architecture with clear separation of concerns:

1. **Data Processor**: Handles Excel file reading and validation
2. **Caller**: Manages Google Voice integration and call placement
3. **Scheduler**: Coordinates timing of reminder calls
4. **Application**: Main entry point and orchestration

## Design Patterns

### Data Flow
```
Excel File → Data Processor → Appointment Queue → (Immediate/Scheduled) → Caller → TwiML Function → Twilio → Phone
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

## Key Components

### DataProcessor Class
- Reads Excel files
- Validates required columns
- Parses dates and times
- Returns structured appointment data

### Caller Class
- Authenticates with Twilio API
- Places phone calls via Twilio
- Uses TwiML Function for dynamic messages
- Handles call outcomes (answered, voicemail, failed)
- Retries on transient errors
- Supports both immediate and scheduled modes

### Scheduler Class
- Manages call timing
- Calculates reminder times (e.g., 24h before appointment)
- Handles time zone conversions
- Queues calls for execution

### App Class
- Coordinates all components
- Loads configuration
- Initializes modules
- Provides CLI interface

