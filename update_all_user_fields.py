"""
Update all user records with complete personnel details
Including all available fields for ASI, HC, Constable (Male/Female), Driver Constable
and hardcoded users like SP, SDPO, ASP
"""
from extensions import mongo
from bson.objectid import ObjectId
from app import app

def update_all_user_fields():
    """Update all users with comprehensive personnel data"""
    with app.app_context():
        print("Starting comprehensive user update with all available personnel fields...")
        print("=" * 70)
        
        # Get all users
        users = list(mongo.db.users.find({}))
        print(f"Found {len(users)} users to process")
        print()
        
        updated_count = 0
        field_stats = {}
        
        # Complete field mapping - all possible fields from personnel to user
        # Including fields from Excel: Father name, DOB, Address, PS/OP, Class, etc.
        field_mappings = {
            # Basic Information
            'name': 'name',
            'ein': 'employee_id',
            'father_name': 'father_name',
            'Fathers Name ': 'father_name',  # Excel column name
            'mother_name': 'mother_name',
            'spouse_name': 'spouse_name',
            'date_of_birth': 'date_of_birth',
            'DOB': 'date_of_birth',  # Excel column name
            'gender': 'gender',
            'blood_group': 'blood_group',
            'marital_status': 'marital_status',
            'religion': 'religion',
            'caste': 'caste',
            'category': 'category',
            'nationality': 'nationality',
            'old_constable_nos': 'old_constable_nos',
            'Old  Constable  Nos.': 'old_constable_nos',  # Excel column
            
            # Contact Details
            'phone': 'phone',
            'Mobiles  Nos.': 'phone',  # Excel column
            'alternate_phone': 'alternate_phone',
            'mobile': 'phone',  # fallback mapping
            'email': 'email',
            'address': 'address',
            'Home address': 'address',  # Excel column
            'permanent_address': 'permanent_address',
            'present_address': 'present_address',
            'city': 'city',
            'state': 'state',
            'pincode': 'pincode',
            'district': 'district',
            'attached_to_dist': 'attached_to_dist',
            'Attached  to Dist.': 'attached_to_dist',  # Excel column
            'attached_from_dist': 'attached_from_dist',
            'Attached from Dist.': 'attached_from_dist',  # Excel column
            'village': 'village',
            'post_office': 'post_office',
            
            # Official Documents
            'aadhar_number': 'aadhar_number',
            'aadhar': 'aadhar_number',
            'pan_number': 'pan_number',
            'pan': 'pan_number',
            'passport_number': 'passport_number',
            'driving_license': 'driving_license',
            'driving_licence_number': 'driving_license',
            'voter_id': 'voter_id',
            'epic_number': 'voter_id',
            
            # Service Details
            'date_of_joining': 'date_of_joining',
            'Date of  Joining the Deptt.': 'date_of_joining',  # Excel column
            'doj': 'date_of_joining',
            'date_of_appointment': 'date_of_joining',
            'date_of_posting': 'date_of_posting',
            'Date of joining the current place of posting ': 'date_of_posting',  # Excel column
            'posting_date': 'date_of_posting',
            'place_of_posting': 'place_of_posting',
            'posting_place': 'place_of_posting',
            'present_duty_location': 'present_duty_location',
            'Present duty  location': 'present_duty_location',  # Excel column
            'ps_op': 'ps_op',
            'PS/OP': 'ps_op',  # Excel column - Police Station/Outpost
            'current_station': 'current_station_name',
            'station': 'current_station_name',
            'station_name': 'current_station_name',
            'current_station_id': 'current_station_id',
            'station_id': 'current_station_id',
            'rank': 'rank',
            ' Rank ': 'rank',  # Excel column
            'designation': 'designation',
            'post': 'designation',
            'department': 'department',
            'section': 'section',
            'unit': 'unit',
            'class_composition_community': 'class_composition_community',
            'Class composition community': 'class_composition_community',  # Excel column
            'service_number': 'service_number',
            'service_no': 'service_number',
            'employee_code': 'employee_code',
            'employee_number': 'employee_code',
            'pay_scale': 'pay_scale',
            'basic_pay': 'basic_pay',
            'grade_pay': 'grade_pay',
            'pay_band': 'pay_band',
            
            # Education
            'qualification': 'qualification',
            'educational_qualification': 'educational_qualification',
            'Edn. Qfn.': 'educational_qualification',  # Excel column
            'education': 'educational_qualification',
            'professional_qualification': 'professional_qualification',
            'training': 'training',
            'courses': 'courses',
            
            # Bank Details
            'bank_name': 'bank_name',
            'bank_account_number': 'bank_account_number',
            'account_number': 'bank_account_number',
            'bank_ifsc': 'bank_ifsc',
            'ifsc_code': 'bank_ifsc',
            'bank_branch': 'bank_branch',
            
            # Emergency Contact
            'emergency_contact_name': 'emergency_contact_name',
            'emergency_contact_phone': 'emergency_contact_phone',
            'emergency_contact_relation': 'emergency_contact_relation',
            'emergency_phone': 'emergency_contact_phone',
            
            # Physical Details
            'height': 'height',
            'weight': 'weight',
            'identification_mark': 'identification_mark',
            'identification_marks': 'identification_mark',
            
            # Family Details
            'number_of_children': 'number_of_children',
            'family_members': 'family_members',
            
            # Other Details
            'photo': 'photo',
            'photo_path': 'photo',
            'signature': 'signature',
            'remarks': 'remarks',
            'notes': 'remarks',
            'status': 'status',
            'gpf_number': 'gpf_number',
            'pran_number': 'pran_number',
            'esi_number': 'esi_number',
            'uniform_size': 'uniform_size',
            'shoe_size': 'shoe_size',
        }
        
        for user in users:
            username = user.get('username', 'unknown')
            personnel = None
            
            # Try to find personnel record by personnel_id
            if user.get('personnel_id'):
                try:
                    personnel = mongo.db.personnel.find_one({'_id': ObjectId(user['personnel_id'])})
                except:
                    pass
            
            # If not found, try matching by ein/employee_id/username
            if not personnel:
                ein = user.get('employee_id') or user.get('username')
                if ein:
                    # Try exact match first
                    personnel = mongo.db.personnel.find_one({'ein': ein.upper()})
                    
                    # Try case-insensitive match
                    if not personnel:
                        personnel = mongo.db.personnel.find_one({'ein': {'$regex': f'^{ein}$', '$options': 'i'}})
            
            if not personnel:
                # For hardcoded users (sp_admin, sp001, asp001, etc.), skip if no personnel record
                continue
            
            # Collect all available fields from personnel
            update_fields = {}
            
            for personnel_field, user_field in field_mappings.items():
                if personnel.get(personnel_field) and personnel[personnel_field] not in [None, '', 'N/A', 'NA']:
                    # Only update if user doesn't already have this field or it's empty
                    if not user.get(user_field) or user.get(user_field) in [None, '', 'N/A', 'NA']:
                        update_fields[user_field] = personnel[personnel_field]
                        
                        # Track field statistics
                        if user_field not in field_stats:
                            field_stats[user_field] = 0
                        field_stats[user_field] += 1
            
            # Link personnel_id if not already linked
            if personnel and not user.get('personnel_id'):
                update_fields['personnel_id'] = str(personnel['_id'])
            
            if update_fields:
                # Update the user document
                mongo.db.users.update_one(
                    {'_id': user['_id']},
                    {'$set': update_fields}
                )
                updated_count += 1
                
                # Show progress
                rank = user.get('rank', 'Unknown')
                field_count = len(update_fields)
                field_names = list(update_fields.keys())
                
                # Show sample fields
                display_fields = field_names[:5]
                if len(field_names) > 5:
                    display_fields.append(f"... +{len(field_names)-5} more")
                
                print(f"[OK] {rank:20s} | {username:15s} | {field_count:2d} fields: {', '.join(display_fields)}")
        
        print()
        print("=" * 70)
        print(f"Updated {updated_count} out of {len(users)} users")
        print()
        
        # Show field statistics
        if field_stats:
            print("Field Statistics (fields added across all users):")
            print("-" * 70)
            sorted_fields = sorted(field_stats.items(), key=lambda x: x[1], reverse=True)
            for field, count in sorted_fields:
                percentage = (count / updated_count * 100) if updated_count > 0 else 0
                print(f"  {field:35s} : {count:4d} users ({percentage:5.1f}%)")
        
        print()
        print("=" * 70)
        print("Sample of updated users (showing key fields):")
        print("-" * 70)
        
        # Show samples from different ranks
        sample_ranks = ['SP', 'ASP', 'SDPO', 'Inspector', 'SI', 'ASI (Male)', 'ASI (Female)', 
                       'HC (Male)', 'HC (Female)', 'Constable (Male)', 'Constable (Female)', 
                       'Driver Constable', 'Driver']
        
        for rank in sample_ranks:
            sample = mongo.db.users.find_one({'rank': rank})
            if sample:
                name = sample.get('name', 'N/A')
                emp_id = sample.get('employee_id', 'N/A')
                phone = sample.get('phone', 'N/A')
                father = sample.get('father_name', 'N/A')
                posting = sample.get('place_of_posting', sample.get('current_station_name', 'N/A'))
                print(f"  {rank:20s} | {name:25s} | {phone:15s} | Father: {father:20s} | Place: {posting}")

if __name__ == '__main__':
    update_all_user_fields()
