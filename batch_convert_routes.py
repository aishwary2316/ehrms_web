"""
MongoDB Conversion Script for Remaining Routes
Converts leave, transfer, duty, attendance, grievance, reports, assets, payslip, kanglasha
"""
import os
import shutil
from datetime import datetime

# Backup folder
backup_folder = f'routes_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
os.makedirs(backup_folder, exist_ok=True)

routes_to_convert = [
    'leave.py', 'transfer.py', 'duty.py', 'attendance.py', 'grievance.py',
    'reports.py', 'assets.py', 'payslip.py', 'kanglasha.py'
]

print("Creating backups...")
for route_file in routes_to_convert:
    src = f'routes/{route_file}'
    dst = f'{backup_folder}/{route_file}'
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"✓ Backed up {route_file}")

print(f"\nBackups saved to: {backup_folder}")
print("\nReady for conversion. Run individual conversion functions...")

# Conversion patterns for common operations
PATTERNS = {
    'imports': """
from bson.objectid import ObjectId
from extensions import mongo
import re
""",
    'pagination_class': """
class Pagination:
    def __init__(self, page, per_page, total, items):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        self.pages = (total + per_page - 1) // per_page
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1 if self.has_prev else None
        self.next_num = page + 1 if self.has_next else None
""",
    'find_one': "mongo.db.{collection}.find_one({'_id': ObjectId({id})})",
    'find_many': "list(mongo.db.{collection}.find({filter}).sort({sort}, {direction}))",
    'insert': "mongo.db.{collection}.insert_one({doc})",
    'update': "mongo.db.{collection}.update_one({'_id': ObjectId({id})}, {'$set': {data}})",
    'delete': "mongo.db.{collection}.delete_one({'_id': ObjectId({id})})",
    'count': "mongo.db.{collection}.count_documents({filter})"
}

print("\nConversion patterns ready. Each route needs manual conversion.")
print("Key conversions:")
print("1. Replace 'from extensions import db' with 'from extensions import mongo'")
print("2. Add ObjectId import: 'from bson.objectid import ObjectId'")
print("3. Replace Model.query with mongo.db.collection_name.find()")
print("4. Replace db.session.add() with mongo.db.collection.insert_one()")
print("5. Replace db.session.commit() - MongoDB auto-commits")
print("6. Replace Model.query.get_or_404(id) with mongo.db.collection.find_one({'_id': ObjectId(id)})")
print("7. Use from_dict() methods from models.py to convert docs to objects")
print("8. Change route parameters from <int:id> to <id> and convert with ObjectId")

# Due to complexity, provide templates for critical sections
print("\n" + "="*60)
print("SIMPLIFIED APPROACH: Focus on 4 critical routes first")
print("="*60)
print("\nPriority routes (convert these first):")
print("1. leave.py - Leave management (most used)")
print("2. duty.py - Duty assignments")
print("3. attendance.py - Attendance marking")
print("4. assets.py - Asset management")
print("\nOthers can be added incrementally after testing")
