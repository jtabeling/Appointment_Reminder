# Batch Call Logging Feature

## Overview

Added comprehensive batch call logging to track every call made with detailed results.

## What Was Added

### New Module: `src/batch_logger.py`

A dedicated batch logger that:
- Creates CSV logs of all calls
- Tracks call results per batch
- Records detailed information for each call
- Provides formatted, human-readable output

### CSV Log File Format

**Location**: `logs/batch_call_results.csv`

**Columns**:
1. `batch_id` - Unique identifier for each batch (timestamp-based)
2. `timestamp` - When the batch was processed
3. `name` - Person's name
4. `phone_number` - Phone number called
5. `appointment_date` - Appointment date/time
6. `call_answered` - Yes/No indicating if call was answered
7. `call_status` - Twilio call status (queued, ringing, completed, etc.)
8. `call_duration_seconds` - Duration in seconds
9. `call_duration_formatted` - Human-readable duration (e.g., "2m 15s")
10. `call_id` - Twilio call ID for reference
11. `error_message` - Error message if call failed

## Configuration

Added to `config/settings.yaml`:

```yaml
logging:
  # Batch call results log file
  batch_log_file: "logs/batch_call_results.csv"
```

## Usage

### Automatic Logging

Logging happens automatically when running in **immediate mode**:

```bash
python src/app.py data/your_appointments.xlsx
```

After the batch completes, results are automatically logged to the CSV file.

### Example Log Entry

```csv
batch_id,timestamp,name,phone_number,appointment_date,call_answered,call_status,call_duration_seconds,call_duration_formatted,call_id,error_message
20241030_140530,2024-10-30 14:05:30,John Doe,443-506-3813,2024-10-31T14:00:00,Yes,completed,125,2m 5s,CAxxxxxx,,
20241030_140530,2024-10-30 14:05:30,Jane Smith,555-987-6543,2024-11-01T10:00:00,No,no-answer,0,0s,CAyyyyyy,,
```

## Features

### 1. Call Status Detection

The system automatically determines if a call was answered based on Twilio status:
- `completed` - Call completed successfully ✅
- `answered` - Call was answered ✅
- `in-progress` - Call is in progress ✅
- `no-answer` - Call not answered ❌
- `busy` - Line was busy ❌
- `failed` - Call failed ❌

### 2. Duration Formatting

Durations are stored both ways:
- Raw seconds for calculations
- Formatted for readability (e.g., "5m 30s")

### 3. Batch Tracking

Each batch gets a unique ID based on timestamp (`YYYYMMDD_HHMMSS`), making it easy to:
- Track all calls from a single run
- Review historical batches
- Generate reports

### 4. Error Tracking

Failed calls are logged with:
- Error status
- Error message
- Duration set to 0

## Integration

### App Integration

The batch logger is automatically initialized and used in `src/app.py`:

```python
# Initialize batch logger
def _init_batch_logger(self):
    batch_log_file = self.config.get('logging.batch_log_file', 'logs/batch_call_results.csv')
    self.batch_logger = BatchLogger(log_file=batch_log_file)

# Log results after batch completes
if call_immediately and batch_results:
    self.batch_logger.log_batch(batch_id, batch_results)
```

### Result Collection

Results are collected during call processing:

```python
batch_results.append({
    'name': apt.name,
    'phone_number': apt.phone_number,
    'appointment_date': apt.appointment_datetime.isoformat(),
    'answered': self._is_call_answered(result.status),
    'status': result.status,
    'duration': result.duration,
    'call_id': result.call_id,
    'error': result.error
})
```

## Benefits

1. **Complete Audit Trail** - Every call is logged with full details
2. **Easy Reporting** - CSV format works with Excel, Google Sheets, etc.
3. **Compliance** - Detailed records for regulatory requirements
4. **Analytics** - Calculate call success rates, duration averages, etc.
5. **Troubleshooting** - Track call IDs for Twilio support
6. **Historical Data** - Keep permanent records of all calls

## Testing

Run the test script:

```bash
python test_batch_logging.py
python src/app.py data/batch_test.xlsx
```

Then check: `logs/batch_call_results.csv`

## Future Enhancements

Potential additions:
- Email reports of batch results
- Automatic export to Google Sheets
- Dashboard with visualization
- Alert on high failure rates
- Monthly/annual summaries

## Files Modified/Created

**Created**:
- `src/batch_logger.py` - Batch logging module
- `test_batch_logging.py` - Test script
- `BATCH_LOGGING_FEATURE.md` - This documentation

**Modified**:
- `src/app.py` - Integrated batch logger
- `config/settings.yaml` - Added batch log configuration

---

**Status**: ✅ Complete and ready to use!

