# Run E-HRMS Application
Write-Host "Starting E-HRMS Application..." -ForegroundColor Green
Write-Host "Electronic Human Resource Management System" -ForegroundColor Cyan
Write-Host "Imphal West District Police" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check if database exists
if (-not (Test-Path "ehrms.db")) {
    Write-Host ""
    Write-Host "Database not found. Initializing..." -ForegroundColor Yellow
    python init_db.py
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Starting Flask Application..." -ForegroundColor Green
Write-Host "Access at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# Run the application
python app.py
