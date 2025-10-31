# Where to Find Call Results Logs

## Main Log Files

### 1. Batch Call Results (CSV) - **PRIMARY LOG**
**Location:** `logs/batch_call_results.csv`

**What it contains:**
- Every call placed
- Call status (answered, ringing, completed, etc.)
- Duration
- User responses (if using Flask webhook)
- Location information
- Call IDs for Twilio tracking

**Columns:**
- `batch_id` - Unique batch identifier
- `timestamp` - When the call was processed
- `name` - Person called
- `phone_number` - Number called
- `appointment_date` - Appointment date/time
- `location` - Appointment location
- `call_answered` - Yes/No
- `call_status` - Twilio status
- `call_duration_seconds` - Duration in seconds
- `call_duration_formatted` - Human-readable duration
- `call_id` - Twilio call ID
- `user_response` - confirmed/cancelled (if using Flask webhook)
- `error_message` - Any errors

**How to view:**
1. **Open in Excel:** Double-click `logs/batch_call_results.csv`
2. **Use view script:** `python view_call_results.py`
3. **View all:** `python view_call_results.py` (no limit)
4. **View last 10:** `python view_call_results.py --limit 10`

### 2. Detailed Application Log
**Location:** `logs/appointment_reminder.log`

**What it contains:**
- Detailed application logs
- Debug information
- Error messages
- Call placement details
- Status updates

**How to view:**
- Open in any text editor
- Or use: `tail -f logs/appointment_reminder.log` (Linux/Mac)
- Or view in PowerShell: `Get-Content logs/appointment_reminder.log -Tail 50`

## Quick View Commands

### View Latest Results (Python script)
```bash
python view_call_results.py --limit 10
```

### View All Results
```bash
python view_call_results.py
```

### Open in Excel
Just double-click: `logs/batch_call_results.csv`

### Filter Specific Batch
Open CSV in Excel and filter by `batch_id` column

## Understanding the Logs

### Call Status Values
- `completed` - Call finished successfully
- `in-progress` - Call is currently active
- `ringing` - Phone is ringing
- `queued` - Call waiting to be placed
- `no-answer` - Call wasn't answered
- `busy` - Line was busy
- `failed` - Call failed

### User Response Values (Flask Webhook only)
- `confirmed` - User pressed 1
- `cancelled` - User pressed 2
- Empty - No response or not using Flask webhook

### Call Answered
- `Yes` - Call was answered
- `No` - Call wasn't answered

## File Locations Summary

```
Appointment_Reminder/
├── logs/
│   ├── batch_call_results.csv    ← MAIN CALL RESULTS LOG (THIS IS WHAT YOU WANT!)
│   └── appointment_reminder.log  ← Detailed application log
└── view_call_results.py          ← Script to view results nicely
```

## Example: Latest Test Results

The latest batch shows:
- **Batch ID:** 20251031_091726
- **Calls:** 2 placed
- **Status:** Both calls initiated successfully
- **Location:** Main Office and Downtown Branch included

To see your latest results:
```bash
python view_call_results.py --limit 5
```

