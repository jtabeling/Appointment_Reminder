@echo off
echo ============================================================
echo Push Appointment_Reminder to GitHub
echo ============================================================
echo.
echo Your code is ready to push! Follow these steps:
echo.
echo 1. Create repository on GitHub:
echo    https://github.com/new
echo    Name: Appointment_Reminder
echo    Description: Automated appointment reminder system using Twilio
echo    DO NOT initialize with README
echo.
echo 2. Copy your GitHub username
echo.
set /p USERNAME="Enter your GitHub username: "
echo.
echo 3. Adding remote repository...
git remote add origin https://github.com/%USERNAME%/Appointment_Reminder.git
echo.
echo 4. Renaming branch to main...
git branch -M main
echo.
echo 5. Pushing to GitHub...
git push -u origin main
echo.
echo ============================================================
echo Complete! Your repository is now on GitHub!
echo https://github.com/%USERNAME%/Appointment_Reminder
echo ============================================================
pause

