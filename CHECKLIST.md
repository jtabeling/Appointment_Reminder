# Pre-Launch Checklist

Use this checklist before running the Appointment Reminder System in production.

## Environment Setup

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Created `.env` file from `env_example.txt`
- [ ] Added Twilio Account SID to `.env`
- [ ] Added Twilio Auth Token to `.env`
- [ ] Added Twilio phone number to `.env`

## Twilio Configuration

- [ ] Twilio account created and verified
- [ ] Phone number purchased/configured in Twilio
- [ ] Twilio credentials tested in Twilio Console
- [ ] Account has sufficient credits for calls

## TwiML Endpoint (CRITICAL)

Choose and complete ONE option:

- [ ] **Option A**: ngrok set up and URL updated in `src/caller.py`
- [ ] **Option B**: TwiML server deployed and URL updated
- [ ] **Option C**: Twilio Function created and URL updated

⚠️ **Without a working TwiML endpoint, calls will fail!**

## Excel File

- [ ] Created Excel file with required columns:
  - [ ] name
  - [ ] phone_number
  - [ ] email
  - [ ] appointment_date
- [ ] Tested Excel file format
- [ ] Verified date format compatibility
- [ ] Checked phone numbers are valid

## Configuration

- [ ] Reviewed `config/settings.yaml`
- [ ] Set `reminder_hours_before` to desired value
- [ ] Customized message template
- [ ] Configured timezone if needed
- [ ] Set log level appropriately

## Testing

- [ ] Generated sample data: `python create_sample_excel.py`
- [ ] Ran test: `python src/app.py data/sample_appointments.xlsx`
- [ ] Verified no import errors
- [ ] Checked logs for issues
- [ ] Tested with your own phone number
- [ ] Verified call was placed successfully

## Production Readiness

- [ ] Reviewed compliance requirements (TCPA, etc.)
- [ ] Obtained necessary consent from taxpayers
- [ ] Set up log rotation monitoring
- [ ] Configured backup for logs
- [ ] Created Excel file processing workflow
- [ ] Set up monitoring/alerting (optional)

## Deployment

- [ ] Application runs on target server
- [ ] Environment variables configured on server
- [ ] Logs directory has write permissions
- [ ] Scheduled as service/daemon (if needed)
- [ ] Cron job configured (if automated processing)

## Documentation

- [ ] Read README.md
- [ ] Read SETUP_GUIDE.md
- [ ] Understand project structure
- [ ] Know how to check logs
- [ ] Know how to troubleshoot issues

## Go-Live

Once all items are checked, you're ready to launch!

---

**Quick Test Command:**
```bash
python src/app.py data/sample_appointments.xlsx
```

**Check Logs:**
```bash
tail -f logs/appointment_reminder.log
```

**Need Help?**
- Check `SETUP_GUIDE.md` for detailed instructions
- Review logs in `logs/appointment_reminder.log`
- See troubleshooting section in README

