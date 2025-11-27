"""
Create properly working MongoDB route files
"""
import os
import shutil

routes_dir = r'c:\Users\Asus\Downloads\EHRMS_NEW\routes'

# List of files that were auto-converted but need proper fixes
files_to_restore = [
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
print("RESTORING BACKUP FILES")
print("="*70)

for filename in files_to_restore:
    original_path = os.path.join(routes_dir, filename)
    backup_path = os.path.join(routes_dir, filename.replace('.py', '_sqlalchemy_backup.py'))
    
    if os.path.exists(backup_path):
        shutil.copy(backup_path, original_path)
        print(f"✓ Restored: {filename}")
    else:
        print(f"✗ Backup not found: {filename}")

print("\n" + "="*70)
print("FILES RESTORED TO SQLALCHEMY VERSION")
print("="*70)
print("\nNow creating proper MongoDB versions...")
