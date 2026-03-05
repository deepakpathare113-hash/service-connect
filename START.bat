@echo off
REM Service Connect - Startup Script for Windows
REM This script sets up and runs the Service Connect application

echo.
echo ====================================================
echo   SERVICE CONNECT - LOCAL STARTUP
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [✓] Python detected
echo.

REM Navigate to backend directory (path contains space, so use quotes)
cd "back end"

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo [*] Creating Python virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
)

echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [✓] Virtual environment activated
echo.

REM Install/Update requirements
echo [*] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [✓] Dependencies installed
echo.

echo ====================================================
echo [✓] SETUP COMPLETE!
echo ====================================================
echo.
echo Starting Flask Backend Server...
echo.
echo [✓] Server will run at: http://localhost:5000
echo [✓] Open your browser and go to: http://localhost:5000
echo.
echo [!] To stop the server, press Ctrl+C
echo.

REM Run the Flask app
python app.py

pause
