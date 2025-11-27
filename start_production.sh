#!/bin/bash
# Production startup script for E-HRMS

echo "🚀 Starting E-HRMS Production Server..."

# Activate virtual environment
source venv/bin/activate

# Check if database exists
if [ ! -f ehrms_production.db ]; then
    echo "📊 Initializing production database..."
    python init_db_fresh.py
fi

# Create logs directory
mkdir -p logs

# Create uploads directory
mkdir -p uploads/photos

# Set permissions
chmod 755 uploads
chmod 755 uploads/photos

# Start Gunicorn with 4 workers
echo "✅ Starting Gunicorn server..."
gunicorn -w 4 \
    -b 0.0.0.0:5000 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --timeout 120 \
    --keep-alive 5 \
    "app:create_app()"
