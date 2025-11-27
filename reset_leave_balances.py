"""
Reset all personnel leave balances to maximum (unused)
"""

from extensions import mongo
from config import Config
from flask import Flask

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

def reset_all_leave_balances():
    """Reset leave balances for all users to maximum"""
    
    # Default maximum balances
    max_balances = {
        'earned_leave_balance': 30,
        'casual_leave_balance': 15,
        'medical_leave_balance': 12,
        'maternity_leave_balance': 180,  # For female personnel
        'paternity_leave_balance': 15    # For male personnel
    }
    
    with app.app_context():
        print("\n" + "="*60)
        print("RESETTING LEAVE BALANCES TO MAXIMUM")
        print("="*60)
        
        # Get all active users
        users = list(mongo.db.users.find({'is_active': True}))
        
        print(f"\nFound {len(users)} active users")
        print("\nUpdating leave balances...")
        
        updated_count = 0
        
        for user in users:
            user_id = user['_id']
            name = user.get('name', 'Unknown')
            
            # Update leave balances
            result = mongo.db.users.update_one(
                {'_id': user_id},
                {'$set': max_balances}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"  ✓ Updated: {name} ({user.get('employee_id', 'N/A')})")
        
        print("\n" + "="*60)
        print(f"SUMMARY:")
        print(f"  Total users: {len(users)}")
        print(f"  Updated: {updated_count}")
        print("="*60)
        print("\nLeave balances reset successfully!")
        print("All personnel now have:")
        print("  - Earned Leave: 30 days")
        print("  - Casual Leave: 15 days")
        print("  - Medical Leave: 12 days")
        print("  - Maternity Leave: 180 days")
        print("  - Paternity Leave: 15 days")
        print("="*60 + "\n")

if __name__ == '__main__':
    confirm = input("Are you sure you want to reset ALL leave balances? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        reset_all_leave_balances()
    else:
        print("\nOperation cancelled.")
