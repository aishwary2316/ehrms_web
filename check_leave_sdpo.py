#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check why SDPO can't see leave applications
"""

from pymongo import MongoClient
from bson import ObjectId
from config import Config

def main():
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database('ehrms_db')
    
    print("="*80)
    print("CHECKING SDPO LEAVE APPLICATION VISIBILITY")
    print("="*80)
    
    # Get SDPO user
    sdpo = db.users.find_one({'username': 'sdpo001'})
    if not sdpo:
        print("✗ SDPO user not found!")
        return
    
    print(f"\n✓ SDPO User Found:")
    print(f"   ID: {sdpo['_id']}")
    print(f"   Name: {sdpo.get('name', 'N/A')}")
    print(f"   Rank: {sdpo.get('rank', 'N/A')}")
    print(f"   Station ID: {sdpo.get('current_station_id', 'NO STATION')}")
    
    # Check stations with this SDPO
    print("\n" + "="*80)
    print("STATIONS UNDER THIS SDPO")
    print("="*80)
    
    stations = list(db.stations.find({'sdpo_id': str(sdpo['_id'])}))
    print(f"\nFound {len(stations)} stations with sdpo_id = '{sdpo['_id']}'")
    
    if len(stations) == 0:
        # Try other patterns
        print("\nTrying other sdpo_id patterns...")
        stations_alt1 = list(db.stations.find({'sdpo_id': sdpo.get('employee_id')}))
        print(f"  By employee_id: {len(stations_alt1)} stations")
        
        stations_alt2 = list(db.stations.find({'sdpo_id': sdpo.get('username')}))
        print(f"  By username: {len(stations_alt2)} stations")
        
        # Check what sdpo_id values exist
        print("\n" + "="*80)
        print("ALL STATIONS AND THEIR SDPO_ID")
        print("="*80)
        all_stations = list(db.stations.find().limit(5))
        for i, station in enumerate(all_stations, 1):
            print(f"\n{i}. {station.get('name', 'N/A')}")
            print(f"   ID: {station['_id']}")
            print(f"   SDPO ID: {station.get('sdpo_id', 'NO SDPO_ID')}")
            print(f"   OC ID: {station.get('oc_id', 'NO OC_ID')}")
    
    # Check all leave applications
    print("\n" + "="*80)
    print("ALL LEAVE APPLICATIONS")
    print("="*80)
    
    leaves = list(db.leaves.find())
    print(f"\nTotal leave applications: {len(leaves)}")
    
    for i, leave in enumerate(leaves, 1):
        user = db.users.find_one({'_id': ObjectId(leave['user_id'])})
        print(f"\n{i}. Leave Application:")
        print(f"   ID: {leave['_id']}")
        print(f"   Status: {leave.get('status', 'N/A')}")
        print(f"   Type: {leave.get('leave_type', 'N/A')}")
        print(f"   Days: {leave.get('num_days', 'N/A')}")
        print(f"   Applicant: {user.get('name', 'N/A') if user else 'USER NOT FOUND'}")
        print(f"   Applicant Station: {user.get('current_station_id', 'NO STATION') if user else 'N/A'}")
        print(f"   Applicant Rank: {user.get('rank', 'N/A') if user else 'N/A'}")
    
    # Check what statuses should be visible to SDPO
    print("\n" + "="*80)
    print("LEAVES WITH STATUS = 'Approved_OC' OR 'Approved_SDPO'")
    print("="*80)
    
    sdpo_visible_leaves = list(db.leaves.find({'status': {'$in': ['Approved_OC', 'Approved_SDPO']}}))
    print(f"\nFound {len(sdpo_visible_leaves)} leaves with these statuses")
    
    for leave in sdpo_visible_leaves:
        user = db.users.find_one({'_id': ObjectId(leave['user_id'])})
        print(f"\n  • Status: {leave.get('status')}")
        print(f"    Applicant: {user.get('name') if user else 'N/A'}")
        print(f"    User ID: {leave['user_id']}")
        print(f"    User Station: {user.get('current_station_id') if user else 'N/A'}")
    
    print("\n" + "="*80)
    print("RECOMMENDATION")
    print("="*80)
    print("\nThe issue is likely one of these:")
    print("1. No stations have sdpo_id matching SDPO user")
    print("2. Leave applications don't have status 'Approved_OC'")
    print("3. Users who applied for leave don't have current_station_id")
    print("\nSolution: Either:")
    print("- Assign SDPO to stations in database")
    print("- Change SDPO query to show ALL 'Approved_OC' leaves")
    print("- Update existing leaves to 'Approved_OC' status for testing")

if __name__ == '__main__':
    main()
