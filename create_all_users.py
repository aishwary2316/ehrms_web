"""Create user accounts for ALL personnel in the database"""
from flask import Flask
from extensions import mongo
from config import Config
from werkzeug.security import generate_password_hash
from datetime import datetime
import re

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

def extract_first_name(full_name):
    """Extract first name from full name"""
    if not full_name:
        return "password"
    
    # Clean up the name
    name = full_name.strip().upper()
    parts = name.split()
    
    if len(parts) == 0:
        return "password"
    
    # For names like "LONGJAM JOYKUMAR SINGH", "M. ANITA DEVI"
    # Get the middle part or second-to-last part
    if len(parts) >= 3:
        # If last part is SINGH/DEVI/KUMAR, take second-to-last
        if parts[-1] in ['SINGH', 'DEVI', 'KUMAR']:
            return parts[-2].lower()
        else:
            # Take the middle name
            return parts[-2].lower() if len(parts) > 2 else parts[-1].lower()
    elif len(parts) == 2:
        # For "NAME SINGH" or "NAME DEVI"
        if parts[-1] in ['SINGH', 'DEVI', 'KUMAR']:
            return parts[0].lower()
        else:
            return parts[-1].lower()
    else:
        return parts[0].lower()

def get_role_from_rank(rank):
    """Determine role based on rank"""
    rank_upper = rank.upper()
    
    if 'SP' in rank_upper and 'ASP' not in rank_upper and 'DSP' not in rank_upper and 'DY' not in rank_upper:
        return 'sp'
    elif 'ASP' in rank_upper:
        return 'asp'
    elif 'DY' in rank_upper or 'DYSP' in rank_upper or 'DSP' in rank_upper:
        return 'sdpo'
    elif 'INSPECTOR' in rank_upper or 'INSPE' in rank_upper:
        return 'inspector'
    elif 'SUB-INSPECTOR' in rank_upper or 'SI' == rank_upper:
        return 'si'
    elif 'ASI' in rank_upper:
        return 'asi'
    elif 'HEAD CONSTABLE' in rank_upper or 'HC' == rank_upper:
        return 'head_constable'
    elif 'DRIVER' in rank_upper:
        return 'driver'
    elif 'CONSTABLE' in rank_upper:
        return 'constable'
    else:
        return 'personnel'

def create_username(ein, name):
    """Create username from EIN or name"""
    if ein and ein.strip():
        # Use EIN as username (lowercase)
        return ein.strip().lower()
    else:
        # Fallback: use first part of name + random number
        parts = name.strip().split()
        if parts:
            return parts[0].lower() + str(hash(name) % 10000)
        return "user" + str(hash(name) % 10000)

with app.app_context():
    print("="*70)
    print("CREATING USER ACCOUNTS FOR ALL PERSONNEL")
    print("="*70)
    
    # Get all personnel
    total_personnel = mongo.db.personnel.count_documents({})
    print(f"\nTotal personnel in database: {total_personnel}")
    
    # Get existing users
    existing_users = set()
    for user in mongo.db.users.find({}, {'username': 1}):
        existing_users.add(user['username'])
    
    print(f"Existing user accounts: {len(existing_users)}")
    
    # Process in batches
    batch_size = 100
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    print("\nProcessing personnel...")
    print("-" * 70)
    
    personnel_cursor = mongo.db.personnel.find({})
    batch = []
    
    for idx, person in enumerate(personnel_cursor, 1):
        try:
            ein = person.get('ein', '')
            name = person.get('name', '')
            rank = person.get('rank', '')
            
            if not ein and not name:
                error_count += 1
                continue
            
            # Create username
            username = create_username(ein, name)
            
            # Skip if user already exists
            if username in existing_users:
                skipped_count += 1
                continue
            
            # Extract password (first name)
            password = extract_first_name(name)
            
            # Determine role
            role = get_role_from_rank(rank)
            
            # Create email
            email = f"{username}@police.gov.in"
            
            # Prepare user data
            user_data = {
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'role': role,
                'rank': rank,
                'station_id': person.get('station_id'),
                'personnel_id': str(person['_id']),
                'is_active': True,
                'created_at': datetime.utcnow(),
                'last_login': None
            }
            
            batch.append(user_data)
            existing_users.add(username)
            
            # Insert batch when it reaches batch_size
            if len(batch) >= batch_size:
                mongo.db.users.insert_many(batch)
                created_count += len(batch)
                print(f"  Progress: {idx}/{total_personnel} | Created: {created_count} | Skipped: {skipped_count}")
                batch = []
        
        except Exception as e:
            error_count += 1
            if error_count <= 10:  # Only print first 10 errors
                print(f"  Error processing {person.get('name', 'Unknown')}: {str(e)}")
            continue
    
    # Insert remaining batch
    if batch:
        mongo.db.users.insert_many(batch)
        created_count += len(batch)
    
    print("-" * 70)
    print("\n" + "="*70)
    print("USER ACCOUNT CREATION COMPLETED")
    print("="*70)
    print(f"Personnel processed: {total_personnel}")
    print(f"New users created: {created_count}")
    print(f"Existing users (skipped): {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"\nTotal users in database: {mongo.db.users.count_documents({})}")
    
    # Show statistics by role
    print("\n" + "="*70)
    print("USER ACCOUNTS BY ROLE")
    print("="*70)
    roles = mongo.db.users.aggregate([
        {"$group": {"_id": "$role", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    
    for role in roles:
        print(f"  {role['_id']:20} : {role['count']:5} users")
    
    # Show sample credentials by rank
    print("\n" + "="*70)
    print("SAMPLE LOGIN CREDENTIALS (username / password)")
    print("="*70)
    
    sample_ranks = ['SP', 'ASP', 'Dy.SP', 'Inspector', 'Sub-Inspector', 'ASI', 
                    'Head Constable', 'Constable', 'Driver Constable']
    
    for rank in sample_ranks:
        # Find personnel with this rank
        personnel_sample = list(mongo.db.personnel.find({'rank': rank}).limit(3))
        if personnel_sample:
            print(f"\n{rank}:")
            for person in personnel_sample:
                username = create_username(person.get('ein', ''), person.get('name', ''))
                password = extract_first_name(person.get('name', ''))
                print(f"  {username:20} / {password:15} ({person.get('name', 'Unknown')})")
    
    print("\n" + "="*70)
    print("All personnel now have login credentials!")
    print("Username: EIN (lowercase)")
    print("Password: First name (lowercase)")
    print("="*70)
