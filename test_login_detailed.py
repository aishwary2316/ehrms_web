from extensions import db
from app import create_app
from models import User

app = create_app()

with app.app_context():
    # Test employee_id lookup
    test_ids = ['SP001', 'sp001', ' SP001 ', 'SP001 ']
    
    for test_id in test_ids:
        user = User.query.filter_by(employee_id=test_id).first()
        print(f"Testing '{test_id}': {'Found' if user else 'NOT FOUND'}")
    
    # Get actual user
    user = User.query.filter_by(employee_id='SP001').first()
    if user:
        print(f"\nActual user in DB:")
        print(f"  Employee ID: '{user.employee_id}'")
        print(f"  Name: {user.name}")
        print(f"  Email: {user.email}")
        print(f"  Is Active: {user.is_active}")
        print(f"  Password check for 'password123': {user.check_password('password123')}")
        print(f"  Password check for 'Password123': {user.check_password('Password123')}")
        print(f"  Password check for 'PASSWORD123': {user.check_password('PASSWORD123')}")
