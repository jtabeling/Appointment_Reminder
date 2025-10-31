@echo off
echo ========================================
echo ngrok Setup Helper
echo ========================================
echo.
echo This script will help you configure ngrok authentication.
echo.
echo Step 1: Sign up at https://dashboard.ngrok.com/signup
echo Step 2: Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
echo.
echo Enter your ngrok authtoken:
set /p authtoken="Authtoken: "

if "%authtoken%"=="" (
    echo.
    echo Error: Authtoken cannot be empty!
    pause
    exit /b 1
)

echo.
echo Looking for ngrok...
set NGROK_PATH=
where ngrok >nul 2>&1
if %errorlevel% equ 0 (
    set NGROK_PATH=ngrok
    echo Found ngrok in PATH
) else (
    REM Try common locations
    if exist "%LOCALAPPDATA%\ngrok\ngrok.exe" (
        set NGROK_PATH="%LOCALAPPDATA%\ngrok\ngrok.exe"
        echo Found ngrok at %NGROK_PATH%
    ) else if exist "%USERPROFILE%\Downloads\ngrok.exe" (
        set NGROK_PATH="%USERPROFILE%\Downloads\ngrok.exe"
        echo Found ngrok at %NGROK_PATH%
    ) else if exist "C:\ngrok.exe" (
        set NGROK_PATH="C:\ngrok.exe"
        echo Found ngrok at %NGROK_PATH%
    ) else (
        echo.
        echo ERROR: ngrok.exe not found!
        echo.
        echo Please either:
        echo 1. Download ngrok from https://ngrok.com/download
        echo 2. Place ngrok.exe in one of these locations:
        echo    - C:\
        echo    - %USERPROFILE%\Downloads\
        echo    - %LOCALAPPDATA%\ngrok\
        echo 3. Or add ngrok to your PATH
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Configuring ngrok with authtoken...
%NGROK_PATH% config add-authtoken %authtoken%

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! ngrok is now configured.
    echo ========================================
    echo.
    echo You can now run: ngrok http 5000
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Configuration failed
    echo ========================================
    echo.
    echo Please check:
    echo 1. Your authtoken is correct
    echo 2. ngrok is installed and in your PATH
    echo.
)

pause

