"""
Migration script to add photo_path column to users table
"""
import sqlite3
from app import create_app

def add_photo_column():
    app = create_app()
    with app.app_context():
        # Connect to database
        conn = sqlite3.connect('ehrms.db')
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'photo_path' not in columns:
            print("Adding photo_path column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN photo_path VARCHAR(255)")
            conn.commit()
            print("✓ Column added successfully!")
        else:
            print("✓ Column already exists!")
        
        conn.close()

if __name__ == '__main__':
    add_photo_column()
