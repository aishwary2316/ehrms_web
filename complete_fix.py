"""
Complete fix: Standardize ranks (C, HC, SI, ASI), remove dummy data, update all users
"""
from extensions import mongo
from app import app
from bson import ObjectId
from datetime import datetime

def main():
    with app.app_context():
        print("=" * 70)
        print("COMPLETE DATABASE FIX")
        print("=" * 70)
        
        # Step 1: Standardize ranks in personnel
        print("\n1. Standardizing ranks in personnel collection...")
        rank_mappings = {
            'ASI (Male)': 'ASI',
            'ASI (Female)': 'ASI',
            'Constable (Male)': 'C',
            'Constable (Female)': 'C',
            'Constable': 'C',
            'HC (Male)': 'HC',
            'HC (Female)': 'HC',
            'Head Constable': 'HC',
            'SI (Male)': 'SI',
            'SI (Female)': 'SI',
            'Sub-Inspector': 'SI',
            'Dy.SP': 'SDPO',
            'Driver Constable': 'Driver',
        }
        
        for old_rank, new_rank in rank_mappings.items():
            result = mongo.db.personnel.update_many(
                {'rank': old_rank},
                {'$set': {'rank': new_rank}}
            )
            if result.modified_count > 0:
                print(f"   {old_rank:25s} -> {new_rank:10s} ({result.modified_count} records)")
        
        # Step 2: Remove dummy data (personnel without father_name)
        print("\n2. Removing dummy personnel data...")
        result = mongo.db.personnel.delete_many({
            'father_name': {'$exists': False}
        })
        print(f"   Removed {result.deleted_count} dummy records")
        
        # Step 3: Standardize ranks in users
        print("\n3. Standardizing ranks in users collection...")
        for old_rank, new_rank in rank_mappings.items():
            result = mongo.db.users.update_many(
                {'rank': old_rank},
                {'$set': {'rank': new_rank}}
            )
            if result.modified_count > 0:
                print(f"   {old_rank:25s} -> {new_rank:10s} ({result.modified_count} users)")
        
        # Step 4: Update all users with personnel data
        print("\n4. Updating users with personnel data...")
        users = list(mongo.db.users.find())
        updated = 0
        
        for user in users:
            personnel = None
            
            # Try to find personnel
            if user.get('personnel_id'):
                try:
                    personnel = mongo.db.personnel.find_one({'_id': ObjectId(user['personnel_id'])})
                except:
                    pass
            
            if not personnel:
                ein = user.get('employee_id') or user.get('username')
                if ein:
                    personnel = mongo.db.personnel.find_one({'ein': {'$regex': f'^{ein}$', '$options': 'i'}})
            
            if not personnel:
                continue
            
            # Build update
            update_fields = {}
            field_map = {
                'name': 'name',
                'ein': 'employee_id',
                'father_name': 'father_name',
                'date_of_birth': 'date_of_birth',
                'educational_qualification': 'educational_qualification',
                'address': 'address',
                'date_of_joining': 'date_of_joining',
                'date_of_posting': 'date_of_posting',
                'class_composition_community': 'class_composition_community',
                'ps_op': 'ps_op',
                'present_duty_location': 'present_duty_location',
                'attached_to_dist': 'attached_to_dist',
                'attached_from_dist': 'attached_from_dist',
                'phone': 'phone',
                'old_constable_nos': 'old_constable_nos',
                'rank': 'rank',
            }
            
            for pers_field, user_field in field_map.items():
                if personnel.get(pers_field):
                    update_fields[user_field] = personnel[pers_field]
            
            if not user.get('personnel_id'):
                update_fields['personnel_id'] = str(personnel['_id'])
            
            if update_fields:
                mongo.db.users.update_one({'_id': user['_id']}, {'$set': update_fields})
                updated += 1
                
                if updated % 100 == 0:
                    print(f"   Updated {updated} users...")
        
        print(f"   Total updated: {updated} users")
        
        # Step 5: Final statistics
        print("\n" + "=" * 70)
        print("FINAL STATISTICS")
        print("=" * 70)
        
        print("\nPersonnel by rank:")
        ranks = mongo.db.personnel.distinct('rank')
        for rank in sorted(ranks):
            count = mongo.db.personnel.count_documents({'rank': rank})
            with_details = mongo.db.personnel.count_documents({
                'rank': rank, 
                'father_name': {'$exists': True, '$ne': None, '$ne': ''}
            })
            print(f"   {rank:15s}: {count:4d} total, {with_details:4d} with details")
        
        print("\nUsers by rank:")
        user_ranks = mongo.db.users.distinct('rank')
        for rank in sorted(user_ranks):
            count = mongo.db.users.count_documents({'rank': rank})
            with_details = mongo.db.users.count_documents({
                'rank': rank,
                'father_name': {'$exists': True, '$ne': None, '$ne': ''}
            })
            print(f"   {rank:15s}: {count:4d} total, {with_details:4d} with details")
        
        print("\n" + "=" * 70)
        print("Sample users (one per rank):")
        print("=" * 70)
        
        for rank in ['C', 'HC', 'SI', 'ASI', 'Inspector', 'SDPO', 'ASP', 'SP']:
            user = mongo.db.users.find_one({'rank': rank})
            if user:
                print(f"\n{rank}:")
                print(f"   Username: {user.get('username')}")
                print(f"   Name: {user.get('name', 'N/A')}")
                print(f"   Father: {user.get('father_name', 'N/A')}")
                print(f"   Phone: {user.get('phone', 'N/A')}")
                print(f"   PS/OP: {user.get('ps_op', 'N/A')}")
                print(f"   Address: {user.get('address', 'N/A')[:30]}..." if user.get('address') else "   Address: N/A")

if __name__ == '__main__':
    main()
