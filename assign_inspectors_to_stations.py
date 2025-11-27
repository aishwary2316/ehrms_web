"""
Script to assign one Inspector/OC to each police station
"""

from extensions import mongo
from app import create_app
from bson.objectid import ObjectId

def assign_inspectors():
    """Assign one Inspector to each station that doesn't have one."""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ASSIGNING INSPECTORS TO STATIONS")
        print("=" * 60)
        
        # Get all stations
        stations = list(mongo.db.stations.find({'is_active': True}))
        
        # Get all Inspectors who are active
        inspectors = list(mongo.db.users.find({
            'rank': 'Inspector',
            'is_active': True
        }))
        
        if not inspectors:
            print("❌ No active Inspectors found in the system!")
            return
        
        print(f"\n✓ Found {len(stations)} active stations")
        print(f"✓ Found {len(inspectors)} active Inspectors\n")
        
        # Sort inspectors to distribute evenly
        inspectors_iter = iter(inspectors * 100)  # Repeat list to have enough
        
        assigned_count = 0
        skipped_count = 0
        
        for station in stations:
            station_id = station['_id']
            station_name = station.get('name', 'Unknown')
            
            # Check if station already has an OC assigned
            current_oc = station.get('officer_in_charge')
            
            if current_oc:
                # Verify OC exists and is valid
                oc_user = mongo.db.users.find_one({'_id': ObjectId(current_oc)})
                if oc_user and oc_user.get('is_active'):
                    print(f"⊗ {station_name}: Already has OC - {oc_user.get('name', 'Unknown')} (Skipped)")
                    skipped_count += 1
                    continue
            
            # Get next inspector
            try:
                inspector = next(inspectors_iter)
                inspector_id = inspector['_id']
                inspector_name = inspector.get('name', 'Unknown')
                
                # Update station with OC
                mongo.db.stations.update_one(
                    {'_id': station_id},
                    {'$set': {
                        'officer_in_charge': str(inspector_id),
                        'oc_name': inspector_name,
                        'oc_assigned_at': mongo.db.stations.find_one({'_id': station_id}).get('created_at')
                    }}
                )
                
                # Update inspector's station assignment
                mongo.db.users.update_one(
                    {'_id': inspector_id},
                    {'$set': {
                        'current_station_id': str(station_id),
                        'current_station_name': station_name,
                        'is_oc': True
                    }}
                )
                
                print(f"✓ {station_name}: Assigned {inspector_name} as OC")
                assigned_count += 1
                
            except StopIteration:
                print(f"⚠ {station_name}: No more inspectors available")
                break
        
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print(f"  Stations processed: {len(stations)}")
        print(f"  New assignments: {assigned_count}")
        print(f"  Already assigned (skipped): {skipped_count}")
        print("=" * 60)
        
        if assigned_count > 0:
            print("\n✓ Inspector assignment completed successfully!")
        else:
            print("\n⚠ No new assignments made. All stations already have OCs.")

if __name__ == '__main__':
    assign_inspectors()
