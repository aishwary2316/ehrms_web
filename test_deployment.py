"""
Test Script to Verify Deployment
Run this after deploying to check all endpoints
"""

import requests
import sys

def test_endpoint(url, endpoint, expected_status=200):
    """Test a single endpoint."""
    full_url = f"{url}{endpoint}"
    print(f"\n🔍 Testing: {full_url}")
    
    try:
        response = requests.get(full_url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ SUCCESS - Status: {response.status_code}")
            if endpoint in ['/health', '/ping']:
                print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT - Request took too long")
        return False
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
        return False

def main():
    """Main test function."""
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <your-app-url>")
        print("Example: python test_deployment.py https://my-app.onrender.com")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')
    
    print("="*60)
    print("🚀 E-HRMS Deployment Test")
    print("="*60)
    print(f"Testing: {url}")
    
    tests = [
        ('/ping', 200, 'Keep-Alive Ping'),
        ('/health', 200, 'Health Check'),
        ('/', 200, 'Home Page'),
        ('/auth/login', 200, 'Login Page'),
    ]
    
    results = []
    
    for endpoint, expected_status, description in tests:
        print(f"\n📋 Test: {description}")
        success = test_endpoint(url, endpoint, expected_status)
        results.append((description, success))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Your deployment is working correctly!")
        print("\n📝 Next steps:")
        print("   1. Login at: " + url + "/auth/login")
        print("   2. Default credentials: SP001 / password123")
        print("   3. IMPORTANT: Change the default password!")
        print("   4. Configure keep-alive service (UptimeRobot/Cron-Job)")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        print("   - Verify the app is fully deployed")
        print("   - Check Render logs for errors")
        print("   - Ensure database is initialized")
        return 1

if __name__ == '__main__':
    sys.exit(main())
