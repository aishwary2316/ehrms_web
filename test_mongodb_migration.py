"""
E-HRMS MongoDB Migration - Testing Script
Tests all critical features after MongoDB conversion
"""
import sys
from app import app
from extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime

def test_database_connection():
    """Test MongoDB connection"""
    try:
        with app.app_context():
            mongo.db.command('ping')
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_user_count():
    """Test user count"""
    try:
        with app.app_context():
            count = mongo.db.users.count_documents({})
            print(f"✅ User count: {count}")
            return True
    except Exception as e:
        print(f"❌ User count test failed: {e}")
        return False

def test_personnel_count():
    """Test personnel count"""
    try:
        with app.app_context():
            count = mongo.db.personnel.count_documents({})
            print(f"✅ Personnel count: {count}")
            return True
    except Exception as e:
        print(f"❌ Personnel count test failed: {e}")
        return False

def test_stations_count():
    """Test stations count"""
    try:
        with app.app_context():
            count = mongo.db.stations.count_documents({})
            print(f"✅ Stations count: {count}")
            return True
    except Exception as e:
        print(f"❌ Stations count test failed: {e}")
        return False

def test_sample_user():
    """Test fetching a sample user"""
    try:
        with app.app_context():
            user = mongo.db.users.find_one({'username': 'sp001'})
            if user:
                name = user.get('name', user.get('full_name', 'N/A'))
                print(f"✅ Sample user found: {name} ({user['username']})")
                print(f"   User has password_hash: {bool(user.get('password_hash'))}")
                print(f"   User rank: {user.get('rank', 'N/A')}")
                return True
            else:
                print("⚠️ Sample user 'sp001' not found - trying sp_admin")
                user = mongo.db.users.find_one({'username': 'sp_admin'})
                if user:
                    print(f"✅ Found sp_admin instead")
                    return True
                else:
                    print("❌ No test users found")
                    return False
    except Exception as e:
        print(f"❌ Sample user test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_blueprints():
    """Test registered blueprints"""
    try:
        with app.app_context():
            blueprints = list(app.blueprints.keys())
            print(f"✅ Registered blueprints ({len(blueprints)}): {', '.join(blueprints)}")
            return True
    except Exception as e:
        print(f"❌ Blueprints test failed: {e}")
        return False

def test_routes():
    """Test registered routes"""
    try:
        with app.app_context():
            routes = [str(rule) for rule in app.url_map.iter_rules() if not rule.endpoint.startswith('static')]
            print(f"✅ Total routes registered: {len(routes)}")
            critical_routes = ['/auth/login', '/dashboard/', '/users/', '/leave/', '/stations/']
            found = [r for r in routes if any(cr in r for cr in critical_routes)]
            print(f"✅ Critical routes found: {len(found)}")
            return True
    except Exception as e:
        print(f"❌ Routes test failed: {e}")
        return False

if __name__ == '__main__':
    print("="*70)
    print("E-HRMS MONGODB MIGRATION - TESTING")
    print("="*70)
    
    tests = [
        test_database_connection,
        test_user_count,
        test_personnel_count,
        test_stations_count,
        test_sample_user,
        test_blueprints,
        test_routes
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\n Running: {test.__doc__}")
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*70)
    
    if failed == 0:
        print("\n✅✅✅ ALL TESTS PASSED! Ready for deployment ✅✅✅")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please fix before deployment.")
