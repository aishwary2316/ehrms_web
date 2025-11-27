@echo off
echo ================================================
echo E-HRMS - Imphal West District Police
echo Electronic Human Resource Management System
echo ================================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if database exists
if not exist "ehrms.db" (
    echo.
    echo Database not found. Initializing...
    python init_db.py
)

echo.
echo ================================================
echo Starting Flask Application...
echo Access at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Run the application
python app.py

pause
