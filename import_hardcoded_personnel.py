"""Import hardcoded personnel data and create user accounts"""
from flask import Flask
from extensions import mongo
from config import Config
from models import User
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

# Hardcoded personnel data from user
hardcoded_personnel = {
    'SP_ASP': [
        {"name": "LONGJAM JOYKUMAR SINGH", "rank": "SP", "ein": "SP001", "mobile": "9876543201", "station": "Police Headquarters", "gender": "Male"},
        {"name": "HAORONGBAM RATAN SINGH", "rank": "ASP", "ein": "ASP001", "mobile": "9876543202", "station": "Police Headquarters", "gender": "Male"},
        {"name": "NINGTHOUJAM AMIT SINGH", "rank": "ASP", "ein": "ASP002", "mobile": "9876543203", "station": "Police Headquarters", "gender": "Male"},
        {"name": "THOKCHOM KIRAN SINGH", "rank": "ASP", "ein": "ASP003", "mobile": "9876543204", "station": "Police Headquarters", "gender": "Male"},
        {"name": "SALAM IBOMCHA SINGH", "rank": "ASP", "ein": "ASP004", "mobile": "9876543205", "station": "Police Headquarters", "gender": "Male"}
    ],
    'DY_SP': [
        {"name": "N. AMIT SINGH", "rank": "Dy.SP", "ein": "DSP001", "mobile": "9876543301", "gender": "Male"},
        {"name": "SALAM IBOMCHA SINGH", "rank": "Dy.SP", "ein": "DSP002", "mobile": "9876543302", "gender": "Male"},
        {"name": "M. ANITA DEVI", "rank": "Dy.SP", "ein": "DSP003", "mobile": "9876543303", "gender": "Female"},
        {"name": "N. SURCHANDRA SINGH", "rank": "Dy.SP", "ein": "DSP004", "mobile": "9876543304", "gender": "Male"},
        {"name": "TH. RANJIT SINGH", "rank": "Dy.SP", "ein": "DSP005", "mobile": "9876543305", "gender": "Male"},
        {"name": "Y. INAOCHA SINGH", "rank": "Dy.SP", "ein": "DSP006", "mobile": "9876543306", "gender": "Male"},
        {"name": "LAISHRAM NILAMANI SINGH", "rank": "Dy.SP", "ein": "DSP007", "mobile": "9876543307", "gender": "Male"},
        {"name": "M. PREMCHANDRA SINGH", "rank": "Dy.SP", "ein": "DSP008", "mobile": "9876543308", "gender": "Male"},
        {"name": "KH. DHANESHWOR SINGH", "rank": "Dy.SP", "ein": "DSP009", "mobile": "9876543309", "gender": "Male"},
        {"name": "N. TOMBA SINGH", "rank": "Dy.SP", "ein": "DSP010", "mobile": "9876543310", "gender": "Male"},
        {"name": "L. JUGESHWOR SINGH", "rank": "Dy.SP", "ein": "DSP011", "mobile": "9876543311", "gender": "Male"}
    ],
    'INSPECTOR_MALE': [
        {"name": "KHUNDONGBAM HEMANTA SINGH", "rank": "Inspector", "ein": "INS001", "mobile": "9876544001", "gender": "Male"},
        {"name": "MAIBAM SHYAMKUMAR SINGH", "rank": "Inspector", "ein": "INS002", "mobile": "9876544002", "gender": "Male"},
        {"name": "LAISHRAM SANAHANBI SINGH", "rank": "Inspector", "ein": "INS003", "mobile": "9876544003", "gender": "Male"},
        {"name": "MOIRANGTHEM NAOBI SINGH", "rank": "Inspector", "ein": "INS004", "mobile": "9876544004", "gender": "Male"},
        {"name": "THOUNAOJAM PREMJIT SINGH", "rank": "Inspector", "ein": "INS005", "mobile": "9876544005", "gender": "Male"},
        {"name": "YUMNAM JOHNSON SINGH", "rank": "Inspector", "ein": "INS006", "mobile": "9876544006", "gender": "Male"},
        {"name": "LAISHRAM NILAMANI SINGH", "rank": "Inspector", "ein": "INS007", "mobile": "9876544007", "gender": "Male"},
        {"name": "NAOREM SHARAT SINGH", "rank": "Inspector", "ein": "INS008", "mobile": "9876544008", "gender": "Male"},
        {"name": "THOKCHOM MANIHAR SINGH", "rank": "Inspector", "ein": "INS009", "mobile": "9876544009", "gender": "Male"},
        {"name": "MOIRANGTHEM BIREN SINGH", "rank": "Inspector", "ein": "INS010", "mobile": "9876544010", "gender": "Male"},
        {"name": "SOIBAM RANJIT SINGH", "rank": "Inspector", "ein": "INS011", "mobile": "9876544011", "gender": "Male"},
        {"name": "KHUNDRAKPAM KULACHANDRA SINGH", "rank": "Inspector", "ein": "INS012", "mobile": "9876544012", "gender": "Male"},
        {"name": "YUMNAM JOYCHANDRA SINGH", "rank": "Inspector", "ein": "INS013", "mobile": "9876544013", "gender": "Male"},
        {"name": "LAISHRAM TOMBA SINGH", "rank": "Inspector", "ein": "INS014", "mobile": "9876544014", "gender": "Male"},
        {"name": "NINGOMBAM GUNINDRO SINGH", "rank": "Inspector", "ein": "INS015", "mobile": "9876544015", "gender": "Male"},
        {"name": "KHUNDONGBAM RAJEN SINGH", "rank": "Inspector", "ein": "INS016", "mobile": "9876544016", "gender": "Male"},
        {"name": "MOIRANGTHEM BROJENDRO SINGH", "rank": "Inspector", "ein": "INS017", "mobile": "9876544017", "gender": "Male"},
        {"name": "LAISHRAM PREMKUMAR SINGH", "rank": "Inspector", "ein": "INS018", "mobile": "9876544018", "gender": "Male"},
        {"name": "YUMNAM LOKENDRO SINGH", "rank": "Inspector", "ein": "INS019", "mobile": "9876544019", "gender": "Male"},
        {"name": "THOKCHOM NABAKUMAR SINGH", "rank": "Inspector", "ein": "INS020", "mobile": "9876544020", "gender": "Male"},
        {"name": "NAOREM BIRAJIT SINGH", "rank": "Inspector", "ein": "INS021", "mobile": "9876544021", "gender": "Male"},
        {"name": "SOIBAM MANGLEM SINGH", "rank": "Inspector", "ein": "INS022", "mobile": "9876544022", "gender": "Male"},
        {"name": "KHUNDRAKPAM DHANABIR SINGH", "rank": "Inspector", "ein": "INS023", "mobile": "9876544023", "gender": "Male"},
        {"name": "YUMNAM RANJIT SINGH", "rank": "Inspector", "ein": "INS024", "mobile": "9876544024", "gender": "Male"},
        {"name": "LAISHRAM CHANDRAMANI SINGH", "rank": "Inspector", "ein": "INS025", "mobile": "9876544025", "gender": "Male"},
        {"name": "NINGOMBAM TOMBA SINGH", "rank": "Inspector", "ein": "INS026", "mobile": "9876544026", "gender": "Male"},
        {"name": "KHUNDONGBAM SHYAM SINGH", "rank": "Inspector", "ein": "INS027", "mobile": "9876544027", "gender": "Male"},
        {"name": "MOIRANGTHEM IBOMCHA SINGH", "rank": "Inspector", "ein": "INS028", "mobile": "9876544028", "gender": "Male"},
        {"name": "LAISHRAM DHANANJOY SINGH", "rank": "Inspector", "ein": "INS029", "mobile": "9876544029", "gender": "Male"},
        {"name": "YUMNAM RAJEN SINGH", "rank": "Inspector", "ein": "INS030", "mobile": "9876544030", "gender": "Male"}
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

def extract_first_name(full_name):
    """Extract first name from full name"""
    parts = full_name.strip().split()
    if len(parts) > 0:
        # Get the last part which is usually the first name in Indian naming
        # For names like "LONGJAM JOYKUMAR SINGH", take "JOYKUMAR"
        if len(parts) >= 2:
            # If last part is SINGH/DEVI, take the second-to-last
            if parts[-1].upper() in ['SINGH', 'DEVI']:
                return parts[-2].lower()
            else:
                return parts[-1].lower()
        return parts[0].lower()
    return "password"

def create_username(ein, name):
    """Create username from EIN"""
    return ein.lower()

with app.app_context():
    print("="*70)
    print("IMPORTING HARDCODED PERSONNEL & CREATING USER ACCOUNTS")
    print("="*70)
    
    total_personnel = 0
    total_users = 0
    
    # Combine all hardcoded data
    all_personnel = []
    for category, people in hardcoded_personnel.items():
        all_personnel.extend(people)
    
    print(f"\nTotal personnel to import: {len(all_personnel)}")
    
    for person in all_personnel:
        try:
            # Add metadata
            person['created_at'] = datetime.utcnow()
            person['updated_at'] = datetime.utcnow()
            person['status'] = 'Active'
            person['department'] = 'Administration'
            person['date_of_joining'] = datetime(2010, 1, 1)
            
            # Insert or update personnel record
            result = mongo.db.personnel.update_one(
                {'ein': person['ein']},
                {'$set': person},
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                total_personnel += 1
                print(f"✓ Personnel: {person['name']} ({person['ein']})")
                
                # Create user account
                username = create_username(person['ein'], person['name'])
                email = f"{username}@police.gov.in"
                password = extract_first_name(person['name'])
                
                # Determine role based on rank
                if person['rank'] == 'SP':
                    role = 'sp'
                elif person['rank'] == 'ASP':
                    role = 'asp'
                elif person['rank'] == 'Dy.SP':
                    role = 'sdpo'
                elif person['rank'] == 'Inspector':
                    role = 'inspector'
                else:
                    role = 'personnel'
                
                # Check if user already exists
                existing_user = mongo.db.users.find_one({'username': username})
                
                if not existing_user:
                    # Create user account
                    user_data = {
                        'username': username,
                        'email': email,
                        'password_hash': generate_password_hash(password),
                        'role': role,
                        'rank': person['rank'],
                        'station_id': None,
                        'personnel_id': str(result.upserted_id) if result.upserted_id else None,
                        'is_active': True,
                        'created_at': datetime.utcnow(),
                        'last_login': None
                    }
                    mongo.db.users.insert_one(user_data)
                    total_users += 1
                    print(f"  → User: {username} / {password}")
                else:
                    print(f"  → User exists: {username}")
            
        except Exception as e:
            print(f"✗ Error importing {person.get('name', 'Unknown')}: {str(e)}")
            continue
    
    print("\n" + "="*70)
    print(f"IMPORT COMPLETED")
    print("="*70)
    print(f"Personnel imported/updated: {total_personnel}")
    print(f"User accounts created: {total_users}")
    
    # Show summary by rank
    print("\nPersonnel Summary:")
    ranks = mongo.db.personnel.aggregate([
        {"$group": {"_id": "$rank", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    for rank in ranks:
        print(f"  {rank['_id']:20} : {rank['count']:4} personnel")
    
    print(f"\nTotal Personnel in Database: {mongo.db.personnel.count_documents({})}")
    print(f"Total Users in Database: {mongo.db.users.count_documents({})}")
    
    # Show sample login credentials
    print("\n" + "="*70)
    print("SAMPLE LOGIN CREDENTIALS (username / password)")
    print("="*70)
    print("\nSP Level:")
    sp_users = mongo.db.users.find({'role': 'sp'}).limit(5)
    for user in sp_users:
        personnel = mongo.db.personnel.find_one({'ein': user['username'].upper()})
        if personnel:
            pwd = extract_first_name(personnel['name'])
            print(f"  {user['username']:15} / {pwd}")
    
    print("\nASP Level:")
    asp_users = mongo.db.users.find({'role': 'asp'}).limit(5)
    for user in asp_users:
        personnel = mongo.db.personnel.find_one({'ein': user['username'].upper()})
        if personnel:
            pwd = extract_first_name(personnel['name'])
            print(f"  {user['username']:15} / {pwd}")
    
    print("\nInspector Level:")
    inspector_users = mongo.db.users.find({'role': 'inspector'}).limit(5)
    for user in inspector_users:
        personnel = mongo.db.personnel.find_one({'ein': user['username'].upper()})
        if personnel:
            pwd = extract_first_name(personnel['name'])
            print(f"  {user['username']:15} / {pwd}")
    
    print("\n" + "="*70)
