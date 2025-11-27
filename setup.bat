@echo off
echo ================================================
echo E-HRMS Setup Script
echo ================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo Python is installed!
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed!

REM Initialize database
echo.
echo Initializing database...
python init_db.py

echo.
echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo To start the application, run: run.bat
echo Or manually:
echo   1. venv\Scripts\activate.bat
echo   2. python app.py
echo.
echo Access the application at: http://localhost:5000
echo Default login credentials are in README.md
echo.
pause
