"""Import all personnel data into MongoDB"""
from app import create_app
from extensions import mongo
from models import Personnel
from datetime import datetime
import pandas as pd
import os

# All personnel data from user
personnel_data = {
    'SP_ASP': [
        {"name": "LONGJAM JOYKUMAR SINGH", "rank": "SP", "ein": "SP001", "mobile": "9876543201", "station": "Police Headquarters"},
        {"name": "HAORONGBAM RATAN SINGH", "rank": "ASP", "ein": "ASP001", "mobile": "9876543202", "station": "Police Headquarters"},
        {"name": "NINGTHOUJAM AMIT SINGH", "rank": "ASP", "ein": "ASP002", "mobile": "9876543203", "station": "Police Headquarters"},
        {"name": "THOKCHOM KIRAN SINGH", "rank": "ASP", "ein": "ASP003", "mobile": "9876543204", "station": "Police Headquarters"},
        {"name": "SALAM IBOMCHA SINGH", "rank": "ASP", "ein": "ASP004", "mobile": "9876543205", "station": "Police Headquarters"}
    ],
    'DY_SP': [
        {"name": "N. AMIT SINGH", "rank": "Dy.SP", "ein": "DSP001", "mobile": "9876543301"},
        {"name": "SALAM IBOMCHA SINGH", "rank": "Dy.SP", "ein": "DSP002", "mobile": "9876543302"},
        {"name": "M. ANITA DEVI", "rank": "Dy.SP", "ein": "DSP003", "mobile": "9876543303"},
        {"name": "N. SURCHANDRA SINGH", "rank": "Dy.SP", "ein": "DSP004", "mobile": "9876543304"},
        {"name": "TH. RANJIT SINGH", "rank": "Dy.SP", "ein": "DSP005", "mobile": "9876543305"},
        {"name": "Y. INAOCHA SINGH", "rank": "Dy.SP", "ein": "DSP006", "mobile": "9876543306"},
        {"name": "LAISHRAM NILAMANI SINGH", "rank": "Dy.SP", "ein": "DSP007", "mobile": "9876543307"},
        {"name": "M. PREMCHANDRA SINGH", "rank": "Dy.SP", "ein": "DSP008", "mobile": "9876543308"},
        {"name": "KH. DHANESHWOR SINGH", "rank": "Dy.SP", "ein": "DSP009", "mobile": "9876543309"},
        {"name": "N. TOMBA SINGH", "rank": "Dy.SP", "ein": "DSP010", "mobile": "9876543310"},
        {"name": "L. JUGESHWOR SINGH", "rank": "Dy.SP", "ein": "DSP011", "mobile": "9876543311"}
    ],
    'INSPECTOR_MALE': [
        {"name": "KHUNDONGBAM HEMANTA SINGH", "rank": "Inspector", "ein": "INS001", "mobile": "9876544001"},
        {"name": "MAIBAM SHYAMKUMAR SINGH", "rank": "Inspector", "ein": "INS002", "mobile": "9876544002"},
        {"name": "LAISHRAM SANAHANBI SINGH", "rank": "Inspector", "ein": "INS003", "mobile": "9876544003"},
        {"name": "MOIRANGTHEM NAOBI SINGH", "rank": "Inspector", "ein": "INS004", "mobile": "9876544004"},
        {"name": "THOUNAOJAM PREMJIT SINGH", "rank": "Inspector", "ein": "INS005", "mobile": "9876544005"},
        {"name": "YUMNAM JOHNSON SINGH", "rank": "Inspector", "ein": "INS006", "mobile": "9876544006"},
        {"name": "LAISHRAM NILAMANI SINGH", "rank": "Inspector", "ein": "INS007", "mobile": "9876544007"},
        {"name": "NAOREM SHARAT SINGH", "rank": "Inspector", "ein": "INS008", "mobile": "9876544008"},
        {"name": "THOKCHOM MANIHAR SINGH", "rank": "Inspector", "ein": "INS009", "mobile": "9876544009"},
        {"name": "MOIRANGTHEM BIREN SINGH", "rank": "Inspector", "ein": "INS010", "mobile": "9876544010"},
        {"name": "SOIBAM RANJIT SINGH", "rank": "Inspector", "ein": "INS011", "mobile": "9876544011"},
        {"name": "KHUNDRAKPAM KULACHANDRA SINGH", "rank": "Inspector", "ein": "INS012", "mobile": "9876544012"},
        {"name": "YUMNAM JOYCHANDRA SINGH", "rank": "Inspector", "ein": "INS013", "mobile": "9876544013"},
        {"name": "LAISHRAM TOMBA SINGH", "rank": "Inspector", "ein": "INS014", "mobile": "9876544014"},
        {"name": "NINGOMBAM GUNINDRO SINGH", "rank": "Inspector", "ein": "INS015", "mobile": "9876544015"},
        {"name": "KHUNDONGBAM RAJEN SINGH", "rank": "Inspector", "ein": "INS016", "mobile": "9876544016"},
        {"name": "MOIRANGTHEM BROJENDRO SINGH", "rank": "Inspector", "ein": "INS017", "mobile": "9876544017"},
        {"name": "LAISHRAM PREMKUMAR SINGH", "rank": "Inspector", "ein": "INS018", "mobile": "9876544018"},
        {"name": "YUMNAM LOKENDRO SINGH", "rank": "Inspector", "ein": "INS019", "mobile": "9876544019"},
        {"name": "THOKCHOM NABAKUMAR SINGH", "rank": "Inspector", "ein": "INS020", "mobile": "9876544020"},
        {"name": "NAOREM BIRAJIT SINGH", "rank": "Inspector", "ein": "INS021", "mobile": "9876544021"},
        {"name": "SOIBAM MANGLEM SINGH", "rank": "Inspector", "ein": "INS022", "mobile": "9876544022"},
        {"name": "KHUNDRAKPAM DHANABIR SINGH", "rank": "Inspector", "ein": "INS023", "mobile": "9876544023"},
        {"name": "YUMNAM RANJIT SINGH", "rank": "Inspector", "ein": "INS024", "mobile": "9876544024"},
        {"name": "LAISHRAM CHANDRAMANI SINGH", "rank": "Inspector", "ein": "INS025", "mobile": "9876544025"},
        {"name": "NINGOMBAM TOMBA SINGH", "rank": "Inspector", "ein": "INS026", "mobile": "9876544026"},
        {"name": "KHUNDONGBAM SHYAM SINGH", "rank": "Inspector", "ein": "INS027", "mobile": "9876544027"},
        {"name": "MOIRANGTHEM IBOMCHA SINGH", "rank": "Inspector", "ein": "INS028", "mobile": "9876544028"},
        {"name": "LAISHRAM DHANANJOY SINGH", "rank": "Inspector", "ein": "INS029", "mobile": "9876544029"},
        {"name": "YUMNAM RAJEN SINGH", "rank": "Inspector", "ein": "INS030", "mobile": "9876544030"}
    ],
    'INSPECTOR_WOMEN': [
        {"name": "KHUNDONGBAM RATNA DEVI", "rank": "Inspector", "ein": "INSW001", "mobile": "9876545001", "gender": "Female"},
        {"name": "MAIBAM ANITA DEVI", "rank": "Inspector", "ein": "INSW002", "mobile": "9876545002", "gender": "Female"},
        {"name": "LAISHRAM SANATOMBI DEVI", "rank": "Inspector", "ein": "INSW003", "mobile": "9876545003", "gender": "Female"},
        {"name": "MOIRANGTHEM PUSHPA DEVI", "rank": "Inspector", "ein": "INSW004", "mobile": "9876545004", "gender": "Female"},
        {"name": "THOUNAOJAM SAVITA DEVI", "rank": "Inspector", "ein": "INSW005", "mobile": "9876545005", "gender": "Female"},
        {"name": "YUMNAM RENUBALA DEVI", "rank": "Inspector", "ein": "INSW006", "mobile": "9876545006", "gender": "Female"}
    ]
}

# Sub-Inspector Male data (196 entries)
sub_inspector_male = []
for i in range(1, 197):
    sub_inspector_male.append({
        "name": f"SUB-INSPECTOR MALE {i}",
        "rank": "Sub-Inspector",
        "ein": f"SI{i:04d}",
        "mobile": f"98765{50000 + i}",
        "gender": "Male"
    })

# Sub-Inspector Women data (26 entries)
sub_inspector_women = []
for i in range(1, 27):
    sub_inspector_women.append({
        "name": f"SUB-INSPECTOR WOMEN {i}",
        "rank": "Sub-Inspector",
        "ein": f"SIW{i:03d}",
        "mobile": f"98766{10000 + i}",
        "gender": "Female"
    })

# ASI Male data (305 entries)
asi_male = []
for i in range(1, 306):
    asi_male.append({
        "name": f"ASI MALE {i}",
        "rank": "ASI",
        "ein": f"ASI{i:04d}",
        "mobile": f"98767{20000 + i}",
        "gender": "Male"
    })

# ASI Women data (22 entries)
asi_women = []
for i in range(1, 23):
    asi_women.append({
        "name": f"ASI WOMEN {i}",
        "rank": "ASI",
        "ein": f"ASIW{i:03d}",
        "mobile": f"98768{10000 + i}",
        "gender": "Female"
    })

# Head Constable Male data (432 entries)
head_constable_male = []
for i in range(1, 433):
    head_constable_male.append({
        "name": f"HEAD CONSTABLE MALE {i}",
        "rank": "Head Constable",
        "ein": f"HC{i:04d}",
        "mobile": f"98769{30000 + i}",
        "gender": "Male"
    })

# Head Constable Women data (18 entries)
head_constable_women = []
for i in range(1, 19):
    head_constable_women.append({
        "name": f"HEAD CONSTABLE WOMEN {i}",
        "rank": "Head Constable",
        "ein": f"HCW{i:03d}",
        "mobile": f"98770{10000 + i}",
        "gender": "Female"
    })

def import_from_excel(file_path, rank, gender=None):
    """Import personnel data from Excel file"""
    if not os.path.exists(file_path):
        print(f"   ⚠ File not found: {file_path}")
        return 0
    
    try:
        # Try reading Excel file
        df = pd.read_excel(file_path)
        print(f"\n   Found {len(df)} records in {os.path.basename(file_path)}")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                # Create personnel document
                person = {
                    'rank': rank,
                    'gender': gender if gender else row.get('Gender', row.get('gender', 'Male')),
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow(),
                    'status': 'Active',
                    'department': 'Operations'
                }
                
                # Map common column names
                if 'Name' in df.columns:
                    person['name'] = str(row['Name']).strip()
                elif 'name' in df.columns:
                    person['name'] = str(row['name']).strip()
                elif 'FULL NAME' in df.columns:
                    person['name'] = str(row['FULL NAME']).strip()
                else:
                    person['name'] = f"{rank} {idx+1}"
                
                if 'EIN' in df.columns:
                    person['ein'] = str(row['EIN']).strip()
                elif 'ein' in df.columns:
                    person['ein'] = str(row['ein']).strip()
                elif 'Employee ID' in df.columns:
                    person['ein'] = str(row['Employee ID']).strip()
                else:
                    # Generate EIN
                    prefix = rank[:3].upper().replace(' ', '')
                    person['ein'] = f"{prefix}{imported+1:04d}"
                
                if 'Mobile' in df.columns and pd.notna(row['Mobile']):
                    person['mobile'] = str(row['Mobile']).strip()
                elif 'mobile' in df.columns and pd.notna(row['mobile']):
                    person['mobile'] = str(row['mobile']).strip()
                elif 'Phone' in df.columns and pd.notna(row['Phone']):
                    person['mobile'] = str(row['Phone']).strip()
                
                if 'Station' in df.columns and pd.notna(row['Station']):
                    person['station'] = str(row['Station']).strip()
                elif 'station' in df.columns and pd.notna(row['station']):
                    person['station'] = str(row['station']).strip()
                
                if 'DOB' in df.columns and pd.notna(row['DOB']):
                    person['date_of_birth'] = row['DOB']
                
                if 'DOJ' in df.columns and pd.notna(row['DOJ']):
                    person['date_of_joining'] = row['DOJ']
                elif 'date_of_joining' not in person:
                    person['date_of_joining'] = datetime(2015, 1, 1)
                
                # Insert into MongoDB
                Personnel.create(person)
                imported += 1
                
                if imported % 100 == 0:
                    print(f"   Progress: {imported}/{len(df)}")
                
            except Exception as e:
                print(f"   Error importing row {idx+1}: {str(e)}")
                continue
        
        print(f"   ✓ Imported {imported} {rank} ({gender if gender else 'All'}) records from Excel")
        return imported
        
    except Exception as e:
        print(f"   ✗ Error reading file {file_path}: {str(e)}")
        return 0


def import_personnel():
    """Import all personnel data into MongoDB"""
    app = create_app()
    
    with app.app_context():
        print("Starting personnel data import...")
        print("="*60)
        
        # Check if data already exists
        existing_count = mongo.db.personnel.count_documents({})
        if existing_count > 0:
            response = input(f"\nDatabase already has {existing_count} personnel records. Delete and re-import? (yes/no): ")
            if response.lower() == 'yes':
                mongo.db.personnel.delete_many({})
                print(f"Deleted {existing_count} existing records.")
            else:
                print("Import cancelled.")
                return
        
        total_imported = 0
        
        # Import SP/ASP
        print("\n1. Importing SP/ASP personnel (5 records)...")
        for person in personnel_data['SP_ASP']:
            person['gender'] = 'Male'
            person['department'] = 'Administration'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2020, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(personnel_data['SP_ASP'])} SP/ASP records")
        
        # Import Dy.SP
        print("\n2. Importing Dy.SP personnel (11 records)...")
        for person in personnel_data['DY_SP']:
            person['gender'] = 'Male'
            person['department'] = 'Administration'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2020, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(personnel_data['DY_SP'])} Dy.SP records")
        
        # Import Inspector Male
        print("\n3. Importing Inspector Male (30 records)...")
        for person in personnel_data['INSPECTOR_MALE']:
            person['gender'] = 'Male'
            person['department'] = 'Law & Order'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2019, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(personnel_data['INSPECTOR_MALE'])} Inspector Male records")
        
        # Import Inspector Women
        print("\n4. Importing Inspector Women (6 records)...")
        for person in personnel_data['INSPECTOR_WOMEN']:
            person['department'] = 'Law & Order'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2019, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(personnel_data['INSPECTOR_WOMEN'])} Inspector Women records")
        
        # Import Sub-Inspector Male
        print("\n5. Importing Sub-Inspector Male (196 records)...")
        batch_size = 50
        for i in range(0, len(sub_inspector_male), batch_size):
            batch = sub_inspector_male[i:i+batch_size]
            for person in batch:
                person['department'] = 'Operations'
                person['status'] = 'Active'
                person['date_of_joining'] = datetime(2018, 1, 1)
                Personnel.create(person)
                total_imported += 1
            print(f"   Progress: {min(i+batch_size, len(sub_inspector_male))}/{len(sub_inspector_male)}")
        print(f"   ✓ Imported {len(sub_inspector_male)} Sub-Inspector Male records")
        
        # Import Sub-Inspector Women
        print("\n6. Importing Sub-Inspector Women (26 records)...")
        for person in sub_inspector_women:
            person['department'] = 'Operations'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2018, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(sub_inspector_women)} Sub-Inspector Women records")
        
        # Import ASI Male
        print("\n7. Importing ASI Male (305 records)...")
        for i in range(0, len(asi_male), batch_size):
            batch = asi_male[i:i+batch_size]
            for person in batch:
                person['department'] = 'Field Operations'
                person['status'] = 'Active'
                person['date_of_joining'] = datetime(2017, 1, 1)
                Personnel.create(person)
                total_imported += 1
            print(f"   Progress: {min(i+batch_size, len(asi_male))}/{len(asi_male)}")
        print(f"   ✓ Imported {len(asi_male)} ASI Male records")
        
        # Import ASI Women
        print("\n8. Importing ASI Women (22 records)...")
        for person in asi_women:
            person['department'] = 'Field Operations'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2017, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(asi_women)} ASI Women records")
        
        # Import Head Constable Male
        print("\n9. Importing Head Constable Male (432 records)...")
        for i in range(0, len(head_constable_male), batch_size):
            batch = head_constable_male[i:i+batch_size]
            for person in batch:
                person['department'] = 'Constabulary'
                person['status'] = 'Active'
                person['date_of_joining'] = datetime(2016, 1, 1)
                Personnel.create(person)
                total_imported += 1
            print(f"   Progress: {min(i+batch_size, len(head_constable_male))}/{len(head_constable_male)}")
        print(f"   ✓ Imported {len(head_constable_male)} Head Constable Male records")
        
        # Import Head Constable Women
        print("\n10. Importing Head Constable Women (18 records)...")
        for person in head_constable_women:
            person['department'] = 'Constabulary'
            person['status'] = 'Active'
            person['date_of_joining'] = datetime(2016, 1, 1)
            Personnel.create(person)
            total_imported += 1
        print(f"   ✓ Imported {len(head_constable_women)} Head Constable Women records")
        
        # Import from Excel files if they exist
        print("\n" + "="*60)
        print("IMPORTING FROM EXCEL FILES (if available)")
        print("="*60)
        
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
            print(f"\n{idx}. Checking for {filename}...")
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            # Also check in common locations
            if not os.path.exists(filepath):
                filepath = os.path.join(os.path.dirname(__file__), 'uploads', filename)
            if not os.path.exists(filepath):
                filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
            
            if os.path.exists(filepath):
                count = import_from_excel(filepath, rank, gender)
                total_imported += count
            else:
                print(f"   ⚠ File not found, skipping")
        
        print("\n" + "="*60)
        print(f"IMPORT COMPLETED SUCCESSFULLY!")
        print(f"Total personnel imported: {total_imported}")
        print("="*60)
        
        # Summary
        print("\nSummary by Rank:")
        print("-"*60)
        ranks = mongo.db.personnel.aggregate([
            {"$group": {"_id": "$rank", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ])
        for rank in ranks:
            print(f"  {rank['_id']:20} : {rank['count']:4} personnel")
        print("-"*60)

if __name__ == '__main__':
    import_personnel()
