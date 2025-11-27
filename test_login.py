from extensions import db
from app import create_app
from models import User

app = create_app()
app.app_context().push()

# Test SP001
user = User.query.filter_by(employee_id='SP001').first()
if user:
    print(f"User found: {user.name}")
    print(f"Employee ID: {user.employee_id}")
    print(f"Has password hash: {bool(user.password_hash)}")
    print(f"Password hash starts with: {user.password_hash[:20]}...")
    print(f"Password 'password123' check: {user.check_password('password123')}")
    print(f"Is active: {user.is_active}")
else:
    print("User SP001 not found!")

# List first 3 users
print("\nFirst 3 users:")
users = User.query.limit(3).all()
for u in users:
    print(f"  {u.employee_id}: {u.name} ({u.rank})")
