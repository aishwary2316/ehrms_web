"""
Script to convert all route files from SQLAlchemy to MongoDB
This will create backup files and update all routes systematically
"""

import os
import re

# Mapping of common SQLAlchemy patterns to MongoDB equivalents
conversions = [
    # Import statements
    (r'from extensions import db', 'from extensions import mongo'),
    (r'from sqlalchemy import.*\n', ''),
    
    # Query patterns - Simple
    (r'User\.query\.get_or_404\(([^)]+)\)', r'User.get_by_id(\1) or abort(404)'),
    (r'User\.query\.get\(([^)]+)\)', r'User.get_by_id(\1)'),
    (r'Station\.query\.get_or_404\(([^)]+)\)', r'Station.get_by_id(\1) or abort(404)'),
    (r'Station\.query\.get\(([^)]+)\)', r'Station.get_by_id(\1)'),
    
    # Count queries
    (r'\.query\.count\(\)', r'.count_documents({})'),
    (r'\.count\(\)', r'.count_documents({})'),
    
    # Session operations
    (r'db\.session\.add\(([^)]+)\)', r'# MongoDB insert handled by model methods'),
    (r'db\.session\.commit\(\)', r'# MongoDB commits automatically'),
    (r'db\.session\.rollback\(\)', r'# MongoDB rollback not needed'),
    (r'db\.session\.delete\(([^)]+)\)', r'# MongoDB delete handled by model methods'),
    
    # Filter operations
    (r'\.query\.filter_by\(', r'.find({'),
    (r'\.filter_by\(', r'.find({'),
    (r'\.query\.filter\(', r'.find({'),
    (r'\.filter\(', r'.find({'),
    
    # Order by
    (r'\.order_by\(([^)]+)\.desc\(\)\)', r'.sort(\1, -1)'),
    (r'\.order_by\(([^)]+)\)', r'.sort(\1, 1)'),
    
    # Limit
    (r'\.limit\(([^)]+)\)', r'.limit(\1)'),
    
    # All/First
    (r'\.all\(\)', r'list()'),
    (r'\.first\(\)', r'find_one()'),
]

def backup_file(filepath):
    """Create a backup of the file"""
    backup_path = filepath.replace('.py', '_sqlalchemy_backup.py')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Backup created: {os.path.basename(backup_path)}")

def convert_file(filepath):
    """Convert a single file from SQLAlchemy to MongoDB"""
    print(f"\nProcessing: {os.path.basename(filepath)}")
    
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply conversions
    for pattern, replacement in conversions:
        content = re.sub(pattern, replacement, content)
    
    # Check if anything changed
    if content != original_content:
        # Create backup
        backup_file(filepath)
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated successfully")
        return True
    else:
        print(f"  - No changes needed")
        return False

# Files to convert
routes_dir = r'c:\Users\Asus\Downloads\EHRMS_NEW\routes'
route_files = [
    'users.py',
    'stations.py',
    'leave.py',
    'transfer.py',
    'duty.py',
    'attendance.py',
    'grievance.py',
    'reports.py',
    'notifications.py',
    'profile.py',
    'assets.py',
    'payslip.py',
    'kanglasha.py'
]

print("="*70)
print("CONVERTING ROUTE FILES FROM SQLALCHEMY TO MONGODB")
print("="*70)

converted_count = 0
for filename in route_files:
    filepath = os.path.join(routes_dir, filename)
    if os.path.exists(filepath):
        if convert_file(filepath):
            converted_count += 1
    else:
        print(f"\n⚠ File not found: {filename}")

print("\n" + "="*70)
print(f"CONVERSION COMPLETED: {converted_count} files updated")
print("="*70)
print("\nNote: These are automatic conversions.")
print("Manual review and testing is required for complex queries.")
print("\nBackup files created with '_sqlalchemy_backup.py' suffix")
