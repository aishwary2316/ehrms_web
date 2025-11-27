from extensions import mongo
from app import app
from pprint import pprint

with app.app_context():
    # Get sp001 user and print full document
    user = mongo.db.users.find_one({'username': 'sp001'})
    print('Full user document for sp001:')
    pprint(user)
    
    print('\n' + '='*60)
    
    # Test password verification
    from werkzeug.security import check_password_hash
    if user and 'password_hash' in user:
        test_passwords = ['joykumar', 'Joykumar', 'JOYKUMAR']
        for pwd in test_passwords:
            result = check_password_hash(user['password_hash'], pwd)
            print(f'Password "{pwd}": {"✓ VALID" if result else "✗ INVALID"}')
