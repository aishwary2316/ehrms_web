#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to create a SDPO user for testing leave approval workflow
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from config import Config

def create_sdpo_user():
    """Create a SDPO user with proper credentials"""
    
    print("="*80)
    print("CREATING SDPO USER")
    print("="*80)
    
    try:
        # Connect to MongoDB
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client.get_database('ehrms_db')
        users_collection = db.users
        
        # Check if SDPO user already exists
        existing_user = users_collection.find_one({'username': 'sdpo001'})
        if existing_user:
            print("\n⚠️  User 'sdpo001' already exists!")
            print(f"   Name: {existing_user.get('name', 'N/A')}")
            print(f"   Rank: {existing_user.get('rank', 'N/A')}")
            print("\nDo you want to update the password? (y/n): ", end='')
            choice = input().strip().lower()
            if choice != 'y':
                print("Aborted.")
                return
            
            # Update existing user
            password_hash = generate_password_hash('sdpo123')
            users_collection.update_one(
                {'username': 'sdpo001'},
                {'$set': {
                    'password_hash': password_hash,
                    'rank': 'SDPO',
                    'role': 'sdpo',
                    'updated_at': datetime.utcnow()
                }}
            )
            print("\n✓ Password updated for existing SDPO user!")
        else:
            # Create new SDPO user
            sdpo_user = {
                'username': 'sdpo001',
                'password_hash': generate_password_hash('sdpo123'),
                'employee_id': 'SDPO001',
                'name': 'TEST SDPO OFFICER',
                'rank': 'SDPO',
                'role': 'sdpo',
                'designation': 'Sub-Divisional Police Officer',
                'email': 'sdpo001@police.gov.in',
                'phone': '9876543210',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = users_collection.insert_one(sdpo_user)
            print(f"\n✓ Successfully created SDPO user!")
            print(f"   ID: {result.inserted_id}")
        
        # Display credentials
        print("\n" + "="*80)
        print("SDPO USER CREDENTIALS")
        print("="*80)
        print("\n   Username: sdpo001")
        print("   Password: sdpo123")
        print("   Employee ID: SDPO001")
        print("   Name: TEST SDPO OFFICER")
        print("   Rank: SDPO")
        print("   Role: sdpo")
        
        print("\n" + "="*80)
        print("COMPLETE TEST WORKFLOW")
        print("="*80)
        print("\n1. Login as Inspector (ins016 / ins16)")
        print("   - Approve pending leave application")
        print("\n2. Login as SDPO (sdpo001 / sdpo123)")
        print("   - Approve the leave (status: Approved_OC → Approved_SDPO)")
        print("\n3. Login as SP (sp001 / sp123)")
        print("   - Final approval → PDF auto-generates")
        print("   - Notification sent to applicant")
        print("   - Signed PDF available for download")
        
        print("\n" + "="*80)
        print("✓ SDPO user ready for testing!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_sdpo_user()
