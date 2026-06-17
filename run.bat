@echo off
title UAE Villa Renovation ROI Prospecting Tool
echo =========================================================
echo   UAE VILLA RENOVATION ROI & PROSPECTING PLATFORM
echo =========================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b
)

:: Create Virtual Environment
if not exist .venv (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
    echo.
)

:: Activate and Install Requirements
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo.

:: Launch Browser
echo Launching dashboard...
start http://localhost:8000
echo.

:: Start FastAPI Server
echo Starting FastAPI Web Server...
echo The dashboard will be accessible at: http://localhost:8000
echo Press Ctrl+C in this terminal to shut down.
echo.
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload

pause
