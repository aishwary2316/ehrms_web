"""
Create or update admin user with admin role
This creates a superuser account with admin privileges
"""

from extensions import mongo
from config import Config
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

def create_admin_user():
    """Create or update admin user"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("ADMIN USER SETUP")
        print("="*60)
        
        # Check if admin01 exists
        admin_user = mongo.db.users.find_one({'employee_id': 'admin01'})
        
        if admin_user:
            print("\nAdmin user 'admin01' already exists.")
            print("Updating role to 'admin'...")
            
            # Update to admin role
            mongo.db.users.update_one(
                {'employee_id': 'admin01'},
                {'$set': {
                    'role': 'admin',
                    'updated_at': datetime.utcnow()
                }}
            )
            
            print("✓ User 'admin01' updated with admin role")
        else:
            print("\nCreating new admin user 'admin01'...")
            
            # Create new admin user
            admin_data = {
                'employee_id': 'admin01',
                'username': 'admin01',
                'password_hash': generate_password_hash('admin@123'),
                'name': 'System Administrator',
                'email': 'admin@ehrms.gov.in',
                'phone': '0000000000',
                'rank': 'SP',  # Has SP rank but admin role
                'designation': 'System Administrator',
                'role': 'admin',  # Special admin role
                'is_active': True,
                'earned_leave_balance': 30,
                'casual_leave_balance': 15,
                'medical_leave_balance': 12,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = mongo.db.users.insert_one(admin_data)
            print(f"✓ Admin user created with ID: {result.inserted_id}")
        
        print("\n" + "="*60)
        print("ADMIN CREDENTIALS:")
        print("  Username: admin01")
        print("  Password: admin@123")
        print("  Role: admin (superuser)")
        print("="*60)
        print("\nThis user has:")
        print("  ✓ Full access to Admin Panel")
        print("  ✓ Can manage all users")
        print("  ✓ Can assign stations to Inspectors")
        print("  ✓ Can modify leave balances")
        print("  ✓ Can view audit logs")
        print("  ✓ Can modify any user details")
        print("  ✓ Higher authority than SP")
        print("="*60 + "\n")

if __name__ == '__main__':
    create_admin_user()
