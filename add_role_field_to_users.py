"""
Migration script to add 'role' field to all existing users
Sets role='user' for all users except admin01 which should be 'admin'
"""

from extensions import mongo
from app import create_app

def add_role_field():
    """Add role field to all users who don't have it."""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ADDING ROLE FIELD TO USERS")
        print("=" * 60)
        
        # Count users without role field
        users_without_role = mongo.db.users.count_documents({'role': {'$exists': False}})
        
        print(f"\n✓ Found {users_without_role} users without role field")
        
        if users_without_role == 0:
            print("\n✓ All users already have role field!")
            return
        
        # Update all users without role to have role='user' (default)
        result = mongo.db.users.update_many(
            {'role': {'$exists': False}},
            {'$set': {'role': 'user'}}
        )
        
        print(f"✓ Updated {result.modified_count} users with role='user'")
        
        # Verify admin01 has admin role
        admin_user = mongo.db.users.find_one({'username': 'admin01'})
        if admin_user:
            if admin_user.get('role') != 'admin':
                mongo.db.users.update_one(
                    {'username': 'admin01'},
                    {'$set': {'role': 'admin'}}
                )
                print("✓ Updated admin01 to have role='admin'")
            else:
                print("✓ admin01 already has role='admin'")
        else:
            print("⚠ admin01 user not found")
        
        print("\n" + "=" * 60)
        print("SUMMARY:")
        total_users = mongo.db.users.count_documents({})
        admin_count = mongo.db.users.count_documents({'role': 'admin'})
        user_count = mongo.db.users.count_documents({'role': 'user'})
        print(f"  Total users: {total_users}")
        print(f"  Admin users: {admin_count}")
        print(f"  Regular users: {user_count}")
        print("=" * 60)
        
        print("\n✓ Role field migration completed successfully!")

if __name__ == '__main__':
    add_role_field()
