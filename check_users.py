from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['ehrms']

print("=" * 80)
print("FINDING REAL USERS FOR LEAVE APPROVAL WORKFLOW")
print("=" * 80)

# Find real Inspector
print("\n1. INSPECTORS (for OC approval):")
inspectors = list(db.users.find({'rank': 'Inspector'}).limit(5))
if inspectors:
    for idx, inspector in enumerate(inspectors, 1):
        print(f"\n   Inspector {idx}:")
        print(f"   Username: {inspector.get('username', 'N/A')}")
        print(f"   Name: {inspector.get('name', 'N/A')}")
        print(f"   Employee ID: {inspector.get('employee_id', 'N/A')}")
        print(f"   Station: {inspector.get('current_station_id', 'N/A')}")
else:
    print("   No Inspectors found!")

# Find real SDPO
print("\n2. SDPOs (for SDPO approval):")
sdpos = list(db.users.find({'rank': 'SDPO'}).limit(5))
if sdpos:
    for idx, sdpo in enumerate(sdpos, 1):
        print(f"\n   SDPO {idx}:")
        print(f"   Username: {sdpo.get('username', 'N/A')}")
        print(f"   Name: {sdpo.get('name', 'N/A')}")
        print(f"   Employee ID: {sdpo.get('employee_id', 'N/A')}")
        print(f"   Station: {sdpo.get('current_station_id', 'N/A')}")
else:
    print("   No SDPOs found!")

# Find real SP
print("\n3. SPs (for final approval):")
sps = list(db.users.find({'rank': 'SP'}).limit(5))
if sps:
    for idx, sp in enumerate(sps, 1):
        print(f"\n   SP {idx}:")
        print(f"   Username: {sp.get('username', 'N/A')}")
        print(f"   Name: {sp.get('name', 'N/A')}")
        print(f"   Employee ID: {sp.get('employee_id', 'N/A')}")
        print(f"   Station: {sp.get('current_station_id', 'N/A')}")
else:
    print("   No SPs found!")

# Find real Constables
print("\n4. CONSTABLES (to apply for leave):")
constables = list(db.users.find({'rank': 'C'}).limit(5))
if constables:
    for idx, constable in enumerate(constables, 1):
        print(f"\n   Constable {idx}:")
        print(f"   Username: {constable.get('username', 'N/A')}")
        print(f"   Name: {constable.get('name', 'N/A')}")
        print(f"   Employee ID: {constable.get('employee_id', 'N/A')}")
        print(f"   Station: {constable.get('current_station_id', 'N/A')}")
else:
    print("   No Constables found!")

# Check if any users have passwords set
print("\n" + "=" * 80)
print("PASSWORD CHECK:")
print("=" * 80)

# Check admin user
admin = db.users.find_one({'username': 'admin01'})
if admin:
    print(f"\n✅ Admin user exists: admin01")
    print(f"   Has password: {'Yes' if admin.get('password') else 'No'}")

# Check sp001
sp001 = db.users.find_one({'username': 'sp001'})
if sp001:
    print(f"\n✅ SP user exists: sp001")
    print(f"   Has password: {'Yes' if sp001.get('password') else 'No'}")
    print(f"   Rank: {sp001.get('rank', 'N/A')}")

# Check ins001
ins001 = db.users.find_one({'username': 'ins001'})
if ins001:
    print(f"\n✅ Inspector user exists: ins001")
    print(f"   Has password: {'Yes' if ins001.get('password') else 'No'}")
    print(f"   Rank: {ins001.get('rank', 'N/A')}")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print(f"Total Inspectors: {db.users.count_documents({'rank': 'Inspector'})}")
print(f"Total SDPOs: {db.users.count_documents({'rank': 'SDPO'})}")
print(f"Total SPs: {db.users.count_documents({'rank': 'SP'})}")
print(f"Total Constables: {db.users.count_documents({'rank': 'C'})}")
print(f"Total Users: {db.users.count_documents({})}")

print("\n" + "=" * 80)
print("RECOMMENDED TEST CREDENTIALS:")
print("=" * 80)

if inspectors:
    print(f"\n✅ Inspector: {inspectors[0].get('username', 'N/A')} / ins@123")
if sdpos:
    print(f"✅ SDPO: {sdpos[0].get('username', 'N/A')} / sdpo@123")
elif not sdpos:
    print(f"⚠️ SDPO: No SDPO found - you may need to create one")
if sps:
    print(f"✅ SP: {sps[0].get('username', 'N/A')} / joykumar")
if constables:
    print(f"✅ Constable: {constables[0].get('username', 'N/A')} / constable@123")

client.close()
