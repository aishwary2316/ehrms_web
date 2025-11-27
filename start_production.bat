@echo off
REM Production startup script for E-HRMS (Windows)

echo Starting E-HRMS Production Server...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if database exists
if not exist ehrms_production.db (
    echo Initializing production database...
    python init_db_fresh.py
)

REM Create logs directory
if not exist logs mkdir logs

REM Create uploads directory
if not exist uploads\photos mkdir uploads\photos

REM Start with waitress (Windows production server)
echo Starting Waitress server...
waitress-serve --host=0.0.0.0 --port=5000 --threads=4 --call app:create_app

pause
