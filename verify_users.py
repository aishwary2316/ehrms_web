"""Verify user accounts"""
from flask import Flask
from extensions import mongo
from config import Config
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

with app.app_context():
    print("="*70)
    print("USER ACCOUNT VERIFICATION")
    print("="*70)
    
    # Test some accounts
    test_users = [
        ('sp001', 'joykumar'),
        ('asp001', 'ratan'),
        ('dsp001', 'amit'),
        ('ins001', 'hemanta'),
        ('sp_admin', 'sp@123')
    ]
    
    print("\nTesting Login Credentials:")
    print("-" * 70)
    
    for username, password in test_users:
        user = mongo.db.users.find_one({'username': username})
        if user:
            password_valid = check_password_hash(user['password_hash'], password)
            status = "✓ VALID" if password_valid else "✗ INVALID"
            print(f"{status} | {username:15} / {password:15} | Role: {user['role']}")
        else:
            print(f"✗ NOT FOUND | {username}")
    
    print("-" * 70)
    
    # Statistics
    total_users = mongo.db.users.count_documents({})
    total_personnel = mongo.db.personnel.count_documents({})
    
    print(f"\nTotal Users: {total_users}")
    print(f"Total Personnel: {total_personnel}")
    print(f"Coverage: {(total_users/total_personnel)*100:.1f}%")
    
    print("\n" + "="*70)
