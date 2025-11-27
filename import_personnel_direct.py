"""Import personnel data directly without loading all routes"""
from flask import Flask
from extensions import mongo
from config import Config
from datetime import datetime
import pandas as pd
import os

# Create minimal app
app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

def import_from_excel(file_path, rank, gender=None):
    """Import personnel data from Excel file"""
    if not os.path.exists(file_path):
        print(f"   ⚠ File not found: {file_path}")
        return 0
    
    try:
        df = pd.read_excel(file_path)
        print(f"\n   Found {len(df)} records in {os.path.basename(file_path)}")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                person = {
                    'rank': rank,
                    'gender': gender if gender else row.get('Gender', 'Male'),
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow(),
                    'status': 'Active',
                    'department': 'Operations'
                }
                
                # Extract name
                if 'Name' in df.columns:
                    person['name'] = str(row['Name']).strip()
                elif 'name' in df.columns:
                    person['name'] = str(row['name']).strip()
                else:
                    person['name'] = f"{rank} {idx+1}"
                
                # Extract EIN
                if 'EIN' in df.columns:
                    person['ein'] = str(row['EIN']).strip()
                elif 'ein' in df.columns:
                    person['ein'] = str(row['ein']).strip()
                else:
                    prefix = rank[:3].upper().replace(' ', '')
                    person['ein'] = f"{prefix}{imported+1:04d}"
                
                # Extract mobile
                if 'Mobile' in df.columns and pd.notna(row['Mobile']):
                    person['mobile'] = str(row['Mobile']).strip()
                
                # Extract station
                if 'Station' in df.columns and pd.notna(row['Station']):
                    person['station'] = str(row['Station']).strip()
                
                person['date_of_joining'] = datetime(2015, 1, 1)
                
                # Insert into MongoDB
                result = mongo.db.personnel.update_one(
                    {'ein': person['ein']},
                    {'$set': person},
                    upsert=True
                )
                
                if result.upserted_id or result.modified_count > 0:
                    imported += 1
                    
                    if imported % 100 == 0:
                        print(f"   Progress: {imported}/{len(df)}")
                
            except Exception as e:
                print(f"   Error importing row {idx+1}: {str(e)}")
                continue
        
        print(f"   ✓ Imported {imported} records")
        return imported
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return 0


with app.app_context():
    print("="*70)
    print("PERSONNEL DATA IMPORT")
    print("="*70)
    
    # Check existing data
    existing = mongo.db.personnel.count_documents({})
    print(f"\nCurrent personnel in database: {existing}")
    
    if existing > 0:
        response = input("\nDelete existing data and re-import? (yes/no): ")
        if response.lower() == 'yes':
            mongo.db.personnel.delete_many({})
            print(f"✓ Deleted {existing} records")
        else:
            print("Import cancelled")
            exit(0)
    
    total = 0
    
    # Import from Excel files
    excel_files = [
        ('sub_inspt male.xlsx', 'Sub-Inspector', 'Male'),
        ('sub_inspt women.xlsx', 'Sub-Inspector', 'Female'),
        ('ASI male.xlsx', 'ASI', 'Male'),
        ('ASI women.xlsx', 'ASI', 'Female'),
        ('head constable male.xlsx', 'Head Constable', 'Male'),
        ('head constable women.xlsx', 'Head Constable', 'Female'),
        ('constable male.xlsx', 'Constable', 'Male'),
        ('constable women.xlsx', 'Constable', 'Female'),
        ('driver contsable.xlsx', 'Driver Constable', 'Male'),
    ]
    
    for idx, (filename, rank, gender) in enumerate(excel_files, 1):
        print(f"\n{idx}. Importing {filename}...")
        filepath = os.path.join(os.path.dirname(__file__), filename)
        count = import_from_excel(filepath, rank, gender)
        total += count
    
    print("\n" + "="*70)
    print(f"IMPORT COMPLETED - Total: {total} records")
    print("="*70)
    
    # Show summary
    print("\nSummary by Rank:")
    ranks = mongo.db.personnel.aggregate([
        {"$group": {"_id": "$rank", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    for rank in ranks:
        print(f"  {rank['_id']:20} : {rank['count']:4} personnel")
