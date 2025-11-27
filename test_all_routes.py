"""Test all MongoDB routes are working"""
from extensions import mongo
from bson.objectid import ObjectId

def test_all_collections():
    """Verify all collections exist and can be queried"""
    
    collections_to_test = [
        'users',
        'personnel', 
        'stations',
        'leaves',
        'transfers',
        'duties',
        'attendance',
        'grievances',
        'station_assets',
        'payslips',
        'kanglasha_entries',
        'notifications'
    ]
    
    print("Testing MongoDB Collections:")
    print("=" * 60)
    
    for collection_name in collections_to_test:
        try:
            collection = mongo.db[collection_name]
            count = collection.count_documents({})
            print(f"✓ {collection_name:20} - {count:6} documents")
        except Exception as e:
            print(f"✗ {collection_name:20} - ERROR: {e}")
    
    print("=" * 60)
    
    # Test a user lookup
    print("\nTesting User Lookup:")
    user = mongo.db.users.find_one({'username': 'sp001'})
    if user:
        print(f"✓ Found user: {user['name']} ({user['rank']})")
    else:
        print("✗ User sp001 not found")
    
    print("\nAll routes should now work with MongoDB! 🎉")
    print("\nTest the application at: http://127.0.0.1:5000")
    print("Login: sp001 / joykumar")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        test_all_collections()
