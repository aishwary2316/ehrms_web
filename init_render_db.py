"""
Initialize PostgreSQL database for E-HRMS on Render
This script creates all tables and adds the default admin user
"""
import os
from app import app, db
from models import User, Station
from werkzeug.security import generate_password_hash

def init_render_db():
    """Initialize database for production on Render."""
    with app.app_context():
        print("🔄 Dropping all existing tables...")
        db.drop_all()
        
        print("🔄 Creating all tables...")
        db.create_all()
        
        print("✅ Tables created successfully!")
        
        # Create default SP (Admin) user
        print("\n🔄 Creating default SP (Admin) user...")
        sp_user = User(
            employee_id='SP001',
            name='Superintendent of Police',
            email='sp@police.gov.in',
            phone='9999999999',
            rank='SP',
            current_station_id=None,
            password_hash=generate_password_hash('password123'),
            is_active=True,
            earned_leave_balance=30,
            casual_leave_balance=10,
            medical_leave_balance=15
        )
        db.session.add(sp_user)
        db.session.commit()
        print(f"✅ SP user created: {sp_user.employee_id}")
        
        print("\n" + "="*60)
        print("🎉 DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        print("\n📋 Default Admin Credentials:")
        print("   User ID: SP001")
        print("   Password: password123")
        print("\n⚠️  IMPORTANT: Change this password immediately after first login!")
        print("\n📝 Next Steps:")
        print("   1. Login to the application with the credentials above")
        print("   2. Change the SP001 password")
        print("   3. Add police stations from the Stations menu")
        print("   4. Add SDPO users for each district")
        print("   5. Add Inspectors (OICs) for each station")
        print("   6. Add ASP and other personnel")
        print("="*60)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("E-HRMS Database Initialization for Render")
    print("="*60)
    
    # Check if DATABASE_URL is set
    db_url = os.environ.get('DATABASE_URL')
    if not db_url or 'postgresql' not in db_url:
        print("\n❌ ERROR: DATABASE_URL environment variable not set or not PostgreSQL!")
        print("   Current DATABASE_URL:", db_url)
        print("\n   Make sure you have set DATABASE_URL in Render environment variables.")
        exit(1)
    
    print(f"\n✅ Using PostgreSQL database")
    print(f"   Host: {db_url.split('@')[1].split('/')[0]}")
    
    # Confirm before proceeding
    response = input("\n⚠️  This will DROP all existing tables and create new ones. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("\n❌ Database initialization cancelled.")
        exit(0)
    
    try:
        init_render_db()
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
