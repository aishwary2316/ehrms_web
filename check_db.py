import sqlite3

# Check raw database
conn = sqlite3.connect('ehrms.db')
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f"Tables in database: {tables}")

# Check users
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]
print(f"Total users (raw SQL): {count}")

cursor.execute("SELECT employee_id, name, rank FROM users LIMIT 5")
users = cursor.fetchall()
print("\nFirst 5 users:")
for user in users:
    print(f"  {user[0]}: {user[1]} ({user[2]})")

conn.close()

# Now check with SQLAlchemy
print("\n" + "="*50)
print("Checking with SQLAlchemy:")
print("="*50)

from extensions import db
from app import create_app
from models import User

app = create_app()
with app.app_context():
    count = User.query.count()
    print(f"Total users (SQLAlchemy): {count}")
    
    if count > 0:
        users = User.query.limit(5).all()
        print("\nFirst 5 users:")
        for user in users:
            print(f"  {user.employee_id}: {user.name} ({user.rank})")
    else:
        print("\nNo users found via SQLAlchemy!")
        print("This indicates a database binding issue.")
