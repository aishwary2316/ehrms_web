#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to check database connection and collections
"""

from pymongo import MongoClient
from config import Config

def main():
    print("="*80)
    print("DATABASE CONNECTION CHECK")
    print("="*80)
    
    try:
        # Connect to MongoDB
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB")
        
        # Get database
        db = client.get_database('ehrms_db')
        print(f"✓ Using database: ehrms_db")
        
        # List all collections
        collections = db.list_collection_names()
        print(f"\n✓ Found {len(collections)} collections:")
        for col in collections:
            print(f"  - {col}")
        
        # Check users collection
        print("\n" + "="*80)
        print("USERS COLLECTION CHECK")
        print("="*80)
        
        if 'users' in collections:
            users_collection = db.users
            total_users = users_collection.count_documents({})
            print(f"Total users: {total_users}")
            
            if total_users > 0:
                print("\nFirst 5 users:")
                for i, user in enumerate(users_collection.find().limit(5), 1):
                    print(f"\n{i}. User:")
                    print(f"   Name: {user.get('name', 'N/A')}")
                    print(f"   Username: {user.get('username', 'N/A')}")
                    print(f"   Employee ID: {user.get('employee_id', 'N/A')}")
                    print(f"   Rank: {user.get('rank', 'N/A')}")
                    print(f"   Role: {user.get('role', 'N/A')}")
                    print(f"   Station: {user.get('station_name', 'N/A')}")
                    print(f"   Has Password: {'Yes' if user.get('password') else 'No'}")
                    
                # Check for test accounts
                print("\n" + "="*80)
                print("CHECKING FOR COMMON TEST ACCOUNTS")
                print("="*80)
                
                test_usernames = ['sp001', 'sdpo001', 'ins001', 'ins016', 'const001', 'admin']
                for username in test_usernames:
                    user = users_collection.find_one({'username': username})
                    if user:
                        print(f"\n✓ Found: {username}")
                        print(f"  Name: {user.get('name', 'N/A')}")
                        print(f"  Rank: {user.get('rank', 'N/A')}")
                        print(f"  Role: {user.get('role', 'N/A')}")
                        print(f"  Has Password: {'Yes' if user.get('password') else 'No'}")
                    else:
                        print(f"✗ Not found: {username}")
            else:
                print("\n⚠️ Users collection is EMPTY!")
        else:
            print("✗ 'users' collection does not exist!")
        
        # Check leaves collection
        print("\n" + "="*80)
        print("LEAVES COLLECTION CHECK")
        print("="*80)
        
        if 'leaves' in collections:
            leaves_collection = db.leaves
            total_leaves = leaves_collection.count_documents({})
            print(f"Total leave applications: {total_leaves}")
            
            if total_leaves > 0:
                print("\nFirst 3 leaves:")
                for i, leave in enumerate(leaves_collection.find().limit(3), 1):
                    print(f"\n{i}. Leave:")
                    print(f"   Status: {leave.get('status', 'N/A')}")
                    print(f"   Type: {leave.get('leave_type', 'N/A')}")
                    print(f"   Days: {leave.get('num_days', 'N/A')}")
                    print(f"   Signed: {leave.get('is_signed', False)}")
        else:
            print("✗ 'leaves' collection does not exist!")
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
