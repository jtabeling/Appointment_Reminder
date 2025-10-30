@echo off
echo ============================================================
echo APPOINTMENT REMINDER SYSTEM - TEST RUN
echo ============================================================
echo.
echo Running test with ready_to_test.xlsx...
echo.
python src/app.py data/ready_to_test.xlsx
echo.
echo ============================================================
echo Test complete! Check logs/appointment_reminder.log for details
echo ============================================================
pause

