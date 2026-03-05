#!/bin/bash

# Service Connect - Startup Script for Linux/Mac
# This script sets up and runs the Service Connect application

echo ""
echo "===================================================="
echo "  SERVICE CONNECT - LOCAL STARTUP"
echo "===================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[✓] Python detected"
echo ""

# Navigate to backend directory (path contains space, so use quotes)
cd "back end"

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv venv
    echo "[✓] Virtual environment created"
fi

echo ""
echo "[*] Activating virtual environment..."
source venv/bin/activate

echo "[✓] Virtual environment activated"
echo ""

# Install/Update requirements
echo "[*] Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[✓] Dependencies installed"
echo ""

echo "===================================================="
echo "[✓] SETUP COMPLETE!"
echo "===================================================="
echo ""
echo "Starting Flask Backend Server..."
echo ""
echo "[✓] Server will run at: http://localhost:5000"
echo "[✓] Open your browser and go to: http://localhost:5000"
echo ""
echo "[!] To stop the server, press Ctrl+C"
echo ""

# Run the Flask app
python3 app.py
