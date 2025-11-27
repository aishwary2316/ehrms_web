"""Initialize MongoDB with default users and collections"""
from app import create_app
from extensions import mongo
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_mongodb():
    """Initialize MongoDB with default data"""
    app = create_app()
    
    with app.app_context():
        print("Initializing MongoDB database...")
        
        # Create indexes
        print("Creating indexes...")
        mongo.db.users.create_index('username', unique=True)
        mongo.db.users.create_index('email', unique=True)
        mongo.db.users.create_index('role')
        
        mongo.db.personnel.create_index('ein', unique=True)
        mongo.db.personnel.create_index('name')
        mongo.db.personnel.create_index('rank')
        mongo.db.personnel.create_index('station_id')
        
        mongo.db.stations.create_index('name', unique=True)
        
        mongo.db.leaves.create_index('personnel_id')
        mongo.db.leaves.create_index('status')
        mongo.db.leaves.create_index('created_at')
        
        mongo.db.transfers.create_index('personnel_id')
        mongo.db.transfers.create_index('status')
        
        mongo.db.duties.create_index('personnel_id')
        mongo.db.duties.create_index('duty_date')
        
        mongo.db.grievances.create_index('personnel_id')
        mongo.db.grievances.create_index('status')
        
        mongo.db.notifications.create_index('user_id')
        mongo.db.notifications.create_index('is_read')
        
        mongo.db.attendance.create_index([('personnel_id', 1), ('date', 1)], unique=True)
        
        mongo.db.assets.create_index('station_id')
        
        print("Indexes created successfully.")
        
        # Check if users already exist
        existing_users = mongo.db.users.count_documents({})
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping initialization.")
            return
        
        # Create default users
        print("Creating default users...")
        
        default_users = [
            {
                'username': 'sp_admin',
                'email': 'sp@police.gov.in',
                'password': 'sp@123',
                'role': 'sp',
                'rank': 'SP',
                'station_id': None
            },
            {
                'username': 'asp_admin',
                'email': 'asp@police.gov.in',
                'password': 'asp@123',
                'role': 'asp',
                'rank': 'ASP',
                'station_id': None
            },
            {
                'username': 'sdpo_admin',
                'email': 'sdpo@police.gov.in',
                'password': 'sdpo@123',
                'role': 'sdpo',
                'rank': 'SDPO',
                'station_id': None
            },
            {
                'username': 'inspector',
                'email': 'inspector@police.gov.in',
                'password': 'inspector@123',
                'role': 'inspector',
                'rank': 'Inspector',
                'station_id': None
            },
            {
                'username': 'personnel',
                'email': 'personnel@police.gov.in',
                'password': 'personnel@123',
                'role': 'personnel',
                'rank': 'Constable',
                'station_id': None
            }
        ]
        
        for user_data in default_users:
            password = user_data.pop('password')
            User.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password,
                role=user_data['role'],
                rank=user_data['rank'],
                station_id=user_data['station_id']
            )
            print(f"Created user: {user_data['username']}")
        
        print("\n" + "="*60)
        print("MongoDB initialization completed successfully!")
        print("="*60)
        print("\nDefault Login Credentials:")
        print("-" * 60)
        for user_data in default_users:
            # Reconstruct password for display
            if 'sp' in user_data['username']:
                pwd = 'sp@123'
            elif 'asp' in user_data['username']:
                pwd = 'asp@123'
            elif 'sdpo' in user_data['username']:
                pwd = 'sdpo@123'
            elif 'inspector' in user_data['username']:
                pwd = 'inspector@123'
            else:
                pwd = 'personnel@123'
            
            print(f"Role: {user_data['role'].upper():12} | Username: {user_data['username']:15} | Password: {pwd}")
        
        print("-" * 60)

if __name__ == '__main__':
    init_mongodb()
