"""
Fix ranks in personnel collection and update users
1. Standardize ranks: ASI (Male/Female) -> ASI, Constable (Male/Female) -> C, etc.
2. Remove old dummy data (records without detailed fields)
3. Update all users with new personnel data
"""
from extensions import mongo
from app import app
from bson import ObjectId

def standardize_ranks():
    """Standardize rank names"""
    with app.app_context():
        print("=" * 70)
        print("STANDARDIZING RANKS")
        print("=" * 70)
        
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
                print(f"  {old_rank:25s} -> {new_rank:10s} ({result.modified_count} records)")
        
        # Also update users
        print("\nUpdating user ranks...")
        for old_rank, new_rank in rank_mappings.items():
            result = mongo.db.users.update_many(
                {'rank': old_rank},
                {'$set': {'rank': new_rank}}
            )
            if result.modified_count > 0:
                print(f"  {old_rank:25s} -> {new_rank:10s} ({result.modified_count} users)")

def remove_dummy_data():
    """Remove personnel records without detailed fields (dummy data)"""
    with app.app_context():
        print("\n" + "=" * 70)
        print("REMOVING DUMMY DATA")
        print("=" * 70)
        
        # Remove records that don't have father_name (indicator of detailed data)
        result = mongo.db.personnel.delete_many({
            'father_name': {'$exists': False}
        })
        print(f"  Removed {result.deleted_count} dummy personnel records (no father_name)")
        
        # Also remove records with only basic fields (created_at, updated_at, ein, name, rank)
        pipeline = [
            {
                '$addFields': {
                    'fieldCount': {'$size': {'$objectToArray': '$$ROOT'}}
                }
            },
            {
                '$match': {
                    'fieldCount': {'$lte': 8}  # Only has basic fields
                }
            }
        ]
        
        basic_only = list(mongo.db.personnel.aggregate(pipeline))
        if basic_only:
            ids_to_remove = [doc['_id'] for doc in basic_only]
            result = mongo.db.personnel.delete_many({'_id': {'$in': ids_to_remove}})
            print(f"  Removed {result.deleted_count} basic-only records")

def update_all_users_with_personnel():
    """Update all users with personnel data"""
    with app.app_context():
        print("\n" + "=" * 70)
        print("UPDATING USERS WITH PERSONNEL DATA")
        print("=" * 70)
        
        users = list(mongo.db.users.find())
        updated = 0
        
        for user in users:
            username = user.get('username', '').lower()
            personnel = None
            
            # Try to find personnel by personnel_id
            if user.get('personnel_id'):
                try:
                    personnel = mongo.db.personnel.find_one({'_id': ObjectId(user['personnel_id'])})
                except:
                    pass
            
            # Try matching by EIN (case insensitive)
            if not personnel:
                ein = user.get('employee_id') or user.get('username')
                if ein:
                    personnel = mongo.db.personnel.find_one({'ein': {'$regex': f'^{ein}$', '$options': 'i'}})
            
            if not personnel:
                continue
            
            # Update user with all personnel fields
            update_fields = {}
            
            # Map all available fields
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
            
            # Link personnel_id
            if not user.get('personnel_id'):
                update_fields['personnel_id'] = str(personnel['_id'])
            
            if update_fields:
                mongo.db.users.update_one(
                    {'_id': user['_id']},
                    {'$set': update_fields}
                )
                updated += 1
                
                if updated % 100 == 0:
                    print(f"  Updated {updated} users...")
        
        print(f"\n  Total updated: {updated} users")

def show_statistics():
    """Show final statistics"""
    with app.app_context():
        print("\n" + "=" * 70)
        print("FINAL STATISTICS")
        print("=" * 70)
        
        print("\nPersonnel by rank:")
        ranks = mongo.db.personnel.distinct('rank')
        for rank in sorted(ranks):
            count = mongo.db.personnel.count_documents({'rank': rank})
            with_father = mongo.db.personnel.count_documents({'rank': rank, 'father_name': {'$exists': True, '$ne': None}})
            print(f"  {rank:15s}: {count:4d} total, {with_father:4d} with father_name")
        
        print("\nUsers by rank:")
        user_ranks = mongo.db.users.distinct('rank')
        for rank in sorted(user_ranks):
            count = mongo.db.users.count_documents({'rank': rank})
            with_father = mongo.db.users.count_documents({'rank': rank, 'father_name': {'$exists': True, '$ne': None}})
            print(f"  {rank:15s}: {count:4d} total, {with_father:4d} with father_name")
        
        print("\n" + "=" * 70)
        print("Sample users with detailed data:")
        
        for rank in ['C', 'HC', 'SI', 'ASI']:
            user = mongo.db.users.find_one({'rank': rank, 'father_name': {'$exists': True}})
            if user:
                print(f"\n{rank}:")
                print(f"  Username: {user.get('username')}")
                print(f"  Name: {user.get('name', 'N/A')}")
                print(f"  Father: {user.get('father_name', 'N/A')}")
                print(f"  Phone: {user.get('phone', 'N/A')}")
                print(f"  PS/OP: {user.get('ps_op', 'N/A')}")
                print(f"  DOB: {user.get('date_of_birth', 'N/A')}")

if __name__ == '__main__':
    standardize_ranks()
    remove_dummy_data()
    update_all_users_with_personnel()
    show_statistics()
