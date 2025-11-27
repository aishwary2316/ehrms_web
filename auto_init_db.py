"""
Alternative: Initialize database automatically on first app startup
This will create tables and default users for all ranks when the app starts
"""
import os
from flask import Flask
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

def init_db_on_startup(app):
    """Initialize database on first startup if tables don't exist."""
    with app.app_context():
        try:
            # Check if tables exist by trying to query User
            User.query.first()
            print("✅ Database tables already exist")
        except Exception as e:
            print(f"📦 Database tables don't exist, creating them...")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created")
        
        # Create default users for each rank if they don't exist
        default_users = [
            {
                'employee_id': 'SP001',
                'name': 'Superintendent of Police',
                'email': 'sp@police.gov.in',
                'phone': '9999999999',
                'rank': 'SP',
                'password': 'sp123'
            },
            {
                'employee_id': 'ASP001',
                'name': 'Additional SP',
                'email': 'asp@police.gov.in',
                'phone': '9999999998',
                'rank': 'ASP',
                'password': 'asp123'
            },
            {
                'employee_id': 'SDPO001',
                'name': 'Sub-Divisional Police Officer',
                'email': 'sdpo@police.gov.in',
                'phone': '9999999997',
                'rank': 'SDPO',
                'password': 'sdpo123'
            },
            {
                'employee_id': 'INS001',
                'name': 'Inspector (OIC)',
                'email': 'inspector@police.gov.in',
                'phone': '9999999996',
                'rank': 'Inspector',
                'password': 'ins123'
            },
            {
                'employee_id': 'SI001',
                'name': 'Sub-Inspector',
                'email': 'si@police.gov.in',
                'phone': '9999999995',
                'rank': 'SI',
                'password': 'si123'
            },
            {
                'employee_id': 'ASI001',
                'name': 'Assistant Sub-Inspector',
                'email': 'asi@police.gov.in',
                'phone': '9999999994',
                'rank': 'ASI',
                'password': 'asi123'
            },
            {
                'employee_id': 'HC001',
                'name': 'Head Constable',
                'email': 'hc@police.gov.in',
                'phone': '9999999993',
                'rank': 'HC',
                'password': 'hc123'
            },
            {
                'employee_id': 'C001',
                'name': 'Constable',
                'email': 'constable@police.gov.in',
                'phone': '9999999992',
                'rank': 'C',
                'password': 'c123'
            }
        ]
        
        print("\n👥 Creating default users for all ranks...")
        created_count = 0
        
        for user_data in default_users:
            existing_user = User.query.filter_by(employee_id=user_data['employee_id']).first()
            
            if not existing_user:
                new_user = User(
                    employee_id=user_data['employee_id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    rank=user_data['rank'],
                    current_station_id=None,
                    password_hash=generate_password_hash(user_data['password']),
                    is_active=True,
                    earned_leave_balance=30,
                    casual_leave_balance=15,
                    medical_leave_balance=12
                )
                db.session.add(new_user)
                created_count += 1
                print(f"  ✅ Created {user_data['rank']}: {user_data['employee_id']} / {user_data['password']}")
        
        if created_count > 0:
            db.session.commit()
            print(f"\n🎉 {created_count} default users created successfully!")
            print("\n📋 Default Login Credentials:")
            print("="*60)
            for user_data in default_users:
                print(f"  {user_data['rank']:10} → {user_data['employee_id']:10} / {user_data['password']}")
            print("="*60)
            print("\n⚠️  IMPORTANT: Change these passwords after first login!")
        else:
            print("✅ All default users already exist")
