"""
Import detailed personnel data from Excel files
Files: ASI male.xlsx, ASI women.xlsx, constable male.xlsx, constable women.xlsx,
       head constable male.xlsx, head constable women.xlsx, driver contsable.xlsx,
       sub_inspt male.xlsx, sub_inspt women.xlsx
"""
import pandas as pd
from extensions import mongo
from app import app
from datetime import datetime
import re

def parse_date(date_str):
    """Parse various date formats"""
    if pd.isna(date_str) or not str(date_str).strip():
        return None
    
    date_str = str(date_str).strip()
    
    # Try various date formats
    formats = [
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d-%m-%y',
        '%d/%m/%y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    return None

def extract_phone(phone_str):
    """Extract phone number from string"""
    if pd.isna(phone_str):
        return None
    
    phone_str = str(phone_str).strip()
    # Extract numbers
    numbers = re.findall(r'\d+', phone_str)
    if numbers:
        phone = ''.join(numbers)
        # Take first 10 digits
        if len(phone) >= 10:
            return phone[:10]
    return None

def import_excel_file(file_path, rank_name):
    """Import personnel data from an Excel file"""
    print(f"\nProcessing {file_path}...")
    print("-" * 70)
    
    try:
        # Read Excel file with header in row 2 (index 1)
        df = pd.read_excel(file_path, header=1)
        
        print(f"Found {len(df)} records")
        
        imported = 0
        updated = 0
        skipped = 0
        
        for idx, row in df.iterrows():
            try:
                # Extract EIN (Employee Identification Number)
                ein = row.get('EIN')
                if pd.isna(ein):
                    skipped += 1
                    continue
                
                ein = str(int(float(ein))) if pd.notna(ein) else None
                if not ein:
                    skipped += 1
                    continue
                
                # Extract other fields
                name = row.get('Name')
                if pd.isna(name) or not str(name).strip():
                    skipped += 1
                    continue
                
                name = str(name).strip()
                
                # Build personnel document
                personnel_data = {
                    'ein': ein.upper(),
                    'name': name,
                    'rank': rank_name,
                    'old_constable_nos': str(row.get('Old  Constable  Nos', '')).strip() if pd.notna(row.get('Old  Constable  Nos')) else None,
                    'father_name': str(row.get('Fathers Name ', '')).strip() if pd.notna(row.get('Fathers Name ')) else None,
                    'date_of_birth': parse_date(row.get('DOB')),
                    'educational_qualification': str(row.get('Edn. Qfn.', '')).strip() if pd.notna(row.get('Edn. Qfn.')) else None,
                    'address': str(row.get('Home address', '')).strip() if pd.notna(row.get('Home address')) else None,
                    'date_of_joining': str(row.get('Date of  Joining the Deptt.', '')).strip() if pd.notna(row.get('Date of  Joining the Deptt.')) else None,
                    'date_of_posting': str(row.get('Date of joining the current place of posting ', '')).strip() if pd.notna(row.get('Date of joining the current place of posting ')) else None,
                    'class_composition_community': str(row.get('Class composition community', '')).strip() if pd.notna(row.get('Class composition community')) else None,
                    'ps_op': str(row.get('PS/OP', '')).strip() if pd.notna(row.get('PS/OP')) else None,
                    'present_duty_location': str(row.get('Present duty  location', '')).strip() if pd.notna(row.get('Present duty  location')) else None,
                    'attached_to_dist': str(row.get('Attached  to Dist.', '')).strip() if pd.notna(row.get('Attached  to Dist.')) else None,
                    'attached_from_dist': str(row.get('Attached from Dist.', '')).strip() if pd.notna(row.get('Attached from Dist.')) else None,
                    'phone': extract_phone(row.get('Mobiles  Nos.')),
                    'updated_at': datetime.utcnow()
                }
                
                # Remove None values
                personnel_data = {k: v for k, v in personnel_data.items() if v not in [None, '', 'nan']}
                
                # Check if personnel already exists
                existing = mongo.db.personnel.find_one({'ein': ein.upper()})
                
                if existing:
                    # Update existing record
                    mongo.db.personnel.update_one(
                        {'_id': existing['_id']},
                        {'$set': personnel_data}
                    )
                    updated += 1
                else:
                    # Insert new record
                    personnel_data['created_at'] = datetime.utcnow()
                    mongo.db.personnel.insert_one(personnel_data)
                    imported += 1
                
                if (imported + updated) % 50 == 0:
                    print(f"  Processed {imported + updated} records...")
                    
            except Exception as e:
                print(f"  Error processing row {idx}: {e}")
                skipped += 1
                continue
        
        print(f"  Imported: {imported}, Updated: {updated}, Skipped: {skipped}")
        return imported, updated, skipped
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0, 0, 0

def main():
    """Import all detailed personnel data"""
    with app.app_context():
        print("=" * 70)
        print("IMPORTING DETAILED PERSONNEL DATA FROM EXCEL FILES")
        print("=" * 70)
        
        files_to_import = [
            ('ASI male.xlsx', 'ASI (Male)'),
            ('ASI women.xlsx', 'ASI (Female)'),
            ('head constable male.xlsx', 'HC (Male)'),
            ('head constable women.xlsx', 'HC (Female)'),
            ('constable male.xlsx', 'Constable (Male)'),
            ('constable women.xlsx', 'Constable (Female)'),
            ('driver contsable.xlsx', 'Driver Constable'),
            ('sub_inspt male.xlsx', 'SI (Male)'),
            ('sub_inspt women.xlsx', 'SI (Female)'),
        ]
        
        total_imported = 0
        total_updated = 0
        total_skipped = 0
        
        for filename, rank in files_to_import:
            file_path = f'C:\\Users\\Asus\\Downloads\\EHRMS_NEW\\{filename}'
            imported, updated, skipped = import_excel_file(file_path, rank)
            total_imported += imported
            total_updated += updated
            total_skipped += skipped
        
        print("\n" + "=" * 70)
        print("IMPORT SUMMARY")
        print("=" * 70)
        print(f"Total Imported: {total_imported}")
        print(f"Total Updated: {total_updated}")
        print(f"Total Skipped: {total_skipped}")
        print(f"Total Processed: {total_imported + total_updated + total_skipped}")
        
        print("\n" + "=" * 70)
        print("Personnel collection statistics:")
        print("-" * 70)
        
        # Show statistics by rank
        ranks = mongo.db.personnel.distinct('rank')
        for rank in sorted(ranks):
            count = mongo.db.personnel.count_documents({'rank': rank})
            print(f"  {rank:25s}: {count:4d} records")
        
        total = mongo.db.personnel.count_documents({})
        print(f"\n  Total personnel: {total}")

if __name__ == '__main__':
    main()
