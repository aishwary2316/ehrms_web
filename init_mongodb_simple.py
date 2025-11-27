"""Simple MongoDB initialization without loading all routes"""
from flask import Flask
from extensions import mongo, login_manager, jwt
from config import Config
from models import User
from datetime import datetime

# Create minimal app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
mongo.init_app(app)
login_manager.init_app(app)
jwt.init_app(app)

with app.app_context():
    print("="*70)
    print("MONGODB INITIALIZATION")
    print("="*70)
    
    # Test connection
    try:
        mongo.db.command('ping')
        print("✓ MongoDB connection successful!")
        print(f"  Database: {app.config['MONGO_DBNAME']}")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        exit(1)
    
    # Create indexes
    print("\nCreating indexes...")
    mongo.db.users.create_index('username', unique=True)
    mongo.db.users.create_index('email', unique=True)
    mongo.db.personnel.create_index('ein', unique=True)
    mongo.db.personnel.create_index('name')
    mongo.db.personnel.create_index('rank')
    mongo.db.stations.create_index('name')
    mongo.db.leaves.create_index([('personnel_id', 1), ('status', 1)])
    mongo.db.transfers.create_index('personnel_id')
    mongo.db.duties.create_index([('personnel_id', 1), ('duty_date', 1)])
    mongo.db.grievances.create_index([('personnel_id', 1), ('status', 1)])
    mongo.db.notifications.create_index([('user_id', 1), ('is_read', 1)])
    mongo.db.attendance.create_index([('personnel_id', 1), ('date', 1)], unique=True)
    mongo.db.assets.create_index('station_id')
    mongo.db.audit_logs.create_index([('user_id', 1), ('timestamp', -1)])
    print("✓ Indexes created successfully")
    
    # Check existing users
    existing_users = mongo.db.users.count_documents({})
    print(f"\nCurrent users in database: {existing_users}")
    
    if existing_users > 0:
        print("\nDatabase already initialized. Existing users:")
        users = mongo.db.users.find()
        for user in users:
            print(f"  - {user['username']} ({user['role']})")
    else:
        print("\nCreating default users...")
        
        default_users = [
            {
                'username': 'sp_admin',
                'email': 'sp@police.gov.in',
                'password': 'sp@123',
                'role': 'sp',
                'rank': 'SP'
            },
            {
                'username': 'asp_admin',
                'email': 'asp@police.gov.in',
                'password': 'asp@123',
                'role': 'asp',
                'rank': 'ASP'
            },
            {
                'username': 'sdpo_admin',
                'email': 'sdpo@police.gov.in',
                'password': 'sdpo@123',
                'role': 'sdpo',
                'rank': 'SDPO'
            },
            {
                'username': 'inspector',
                'email': 'inspector@police.gov.in',
                'password': 'inspector@123',
                'role': 'inspector',
                'rank': 'Inspector'
            },
            {
                'username': 'personnel',
                'email': 'personnel@police.gov.in',
                'password': 'personnel@123',
                'role': 'personnel',
                'rank': 'Constable'
            }
        ]
        
        for user_data in default_users:
            password = user_data.pop('password')
            user = User.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password,
                role=user_data['role'],
                rank=user_data['rank'],
                station_id=None
            )
            print(f"  ✓ Created: {user_data['username']}")
        
        print("\n" + "="*70)
        print("DEFAULT LOGIN CREDENTIALS")
        print("="*70)
        print("Role          | Username       | Password")
        print("-" * 70)
        print("SP            | sp_admin       | sp@123")
        print("ASP           | asp_admin      | asp@123")
        print("SDPO          | sdpo_admin     | sdpo@123")
        print("Inspector     | inspector      | inspector@123")
        print("Personnel     | personnel      | personnel@123")
        print("="*70)
    
    print("\n✓ MongoDB initialization completed successfully!")
