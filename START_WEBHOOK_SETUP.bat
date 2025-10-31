@echo off
echo ========================================
echo Flask Webhook Server Startup
echo ========================================
echo.
echo This will start the Flask webhook server on port 5000
echo.
echo IMPORTANT: Keep this window open while testing!
echo.
echo After this starts, you'll need to:
echo 1. Start ngrok in another terminal: C:\ngrok.exe http 5000
echo 2. Copy the ngrok HTTPS URL
echo 3. Update config/settings.yaml with the URL
echo.
pause
echo.
echo Starting webhook server...
python src/webhook_server.py

