"""
Convert remaining route files from SQLAlchemy to MongoDB
This script will convert: stations, leave, transfer, duty, attendance, grievance, reports, assets, payslip, kanglasha
"""
import os
import re

def convert_stations():
    """Convert stations.py"""
    filepath = 'routes/stations.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace imports
    content = content.replace('from extensions import db', 'from extensions import mongo')
    content = content.replace('from models import Station, User', 'from models import Station, User\nfrom bson.objectid import ObjectId')
    
    # Replace queries - Station.query patterns
    content = re.sub(r'Station\.query\.filter_by\(is_active=True\)\.order_by\(Station\.name\)\.all\(\)', 
                     "list(mongo.db.stations.find({'is_active': True}).sort('name', 1))", content)
    content = re.sub(r'Station\.query\.get_or_404\((\w+)\)', 
                     r"mongo.db.stations.find_one({'_id': ObjectId(\1)}) or abort(404)", content)
    
    # Replace db.session operations
    content = content.replace('db.session.add(station)', 'mongo.db.stations.insert_one(station_doc)')
    content = content.replace('db.session.commit()', '# MongoDB auto-commits')
    content = content.replace('db.session.rollback()', '# MongoDB rollback handled differently')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Converted {filepath}")

# Run conversions
if __name__ == '__main__':
    print("This script provides conversion patterns.")
    print("Due to complexity, manual conversion is recommended.")
    print("Use ROUTE_CONVERSION_STATUS.md as a guide.")
