from extensions import mongo
from app import app

with app.app_context():
    # Check if sp001 exists
    user = mongo.db.users.find_one({'username': 'sp001'})
    print('User found:', user is not None)
    if user:
        print('Username:', user.get('username'))
        print('Employee ID:', user.get('employee_id'))
        print('Has password_hash:', 'password_hash' in user)
        print('Name:', user.get('name'))
    else:
        print('User not found!')
        
    # Check how many users exist
    total = mongo.db.users.count_documents({})
    print(f'\nTotal users in database: {total}')
    
    # Check some sample usernames
    print('\nChecking sample usernames:')
    for username in ['sp001', 'SP001', 'asp001', 'ins001']:
        exists = mongo.db.users.find_one({'username': username})
        print(f'  {username}: {"EXISTS" if exists else "NOT FOUND"}')
