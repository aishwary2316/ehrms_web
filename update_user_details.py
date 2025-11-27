"""Update user records with personnel details"""
from extensions import mongo
from bson.objectid import ObjectId
from app import app

def update_user_details():
    """Update all users with their personnel details"""
    with app.app_context():
        print("Updating user records with personnel details...")
        print("=" * 60)
        
        # Get all users
        users = list(mongo.db.users.find({}))
        print(f"Found {len(users)} users")
        
        updated_count = 0
        
        for user in users:
            update_fields = {}
            
            # If user has personnel_id, fetch personnel data
            if user.get('personnel_id'):
                personnel = mongo.db.personnel.find_one({'_id': ObjectId(user['personnel_id'])})
                
                if personnel:
                    # Update user fields from personnel if not already set
                    if not user.get('name') and personnel.get('name'):
                        update_fields['name'] = personnel['name']
                    
                    if not user.get('employee_id') and personnel.get('ein'):
                        update_fields['employee_id'] = personnel['ein']
                    
                    if not user.get('phone') and personnel.get('phone'):
                        update_fields['phone'] = personnel['phone']
                    
                    if not user.get('email') and personnel.get('email'):
                        update_fields['email'] = personnel['email']
                    
                    # Add other fields that might be useful
                    if personnel.get('date_of_birth'):
                        update_fields['date_of_birth'] = personnel['date_of_birth']
                    
                    if personnel.get('date_of_joining'):
                        update_fields['date_of_joining'] = personnel['date_of_joining']
                    
                    if personnel.get('current_station_id'):
                        update_fields['current_station_id'] = personnel['current_station_id']
            
            # Also try to match by ein/employee_id if personnel_id is not set
            elif user.get('employee_id') or user.get('username'):
                ein = user.get('employee_id') or user.get('username')
                personnel = mongo.db.personnel.find_one({'ein': ein.upper()})
                
                if personnel:
                    # Link the personnel record
                    update_fields['personnel_id'] = str(personnel['_id'])
                    
                    if not user.get('name') and personnel.get('name'):
                        update_fields['name'] = personnel['name']
                    
                    if not user.get('phone') and personnel.get('phone'):
                        update_fields['phone'] = personnel['phone']
                    
                    if not user.get('email') and personnel.get('email'):
                        update_fields['email'] = personnel['email']
                    
                    if personnel.get('date_of_birth'):
                        update_fields['date_of_birth'] = personnel['date_of_birth']
                    
                    if personnel.get('date_of_joining'):
                        update_fields['date_of_joining'] = personnel['date_of_joining']
                    
                    if personnel.get('current_station_id'):
                        update_fields['current_station_id'] = personnel['current_station_id']
            
            # Update if we have any fields to update
            if update_fields:
                mongo.db.users.update_one(
                    {'_id': user['_id']},
                    {'$set': update_fields}
                )
                updated_count += 1
                print(f"✓ Updated user {user.get('username', 'unknown')} with {len(update_fields)} fields: {list(update_fields.keys())}")
        
        print("=" * 60)
        print(f"Updated {updated_count} out of {len(users)} users")
        
        # Show sample of updated users
        print("\nSample of updated users:")
        sample_users = list(mongo.db.users.find({}).limit(5))
        for user in sample_users:
            print(f"  {user.get('username', 'N/A'):10} | {user.get('name', 'N/A'):25} | {user.get('phone', 'N/A'):15} | {user.get('email', 'N/A')}")

if __name__ == '__main__':
    update_user_details()
