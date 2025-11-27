"""MongoDB Models for EHRMS System"""
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import mongo

class User(UserMixin):
    """User model for authentication"""
    
    def __init__(self, user_data):
        self.id = str(user_data.get('_id', ''))
        self.username = user_data.get('username', '')
        self.name = user_data.get('name', '')
        self.employee_id = user_data.get('employee_id', '')
        self.email = user_data.get('email', '')
        self.phone = user_data.get('phone', '')
        self.password_hash = user_data.get('password_hash', '')
        self.role = user_data.get('role', 'personnel')
        self.rank = user_data.get('rank', '')
        self.station_id = user_data.get('station_id')
        self.current_station_id = user_data.get('current_station_id')
        self.current_station = None  # Will be populated if needed
        self.current_station_name = user_data.get('current_station_name', '')
        self.personnel_id = user_data.get('personnel_id')
        self._is_active = user_data.get('is_active', True)
        self.created_at = user_data.get('created_at', datetime.utcnow())
        self.last_login = user_data.get('last_login')
        
        # Leave balances
        self.earned_leave_balance = user_data.get('earned_leave_balance', 30)
        self.casual_leave_balance = user_data.get('casual_leave_balance', 15)
        self.medical_leave_balance = user_data.get('medical_leave_balance', 12)
        self.half_pay_leave_balance = user_data.get('half_pay_leave_balance', 20)
        self.child_care_leave_balance = user_data.get('child_care_leave_balance', 730)
        self.maternity_leave_used = user_data.get('maternity_leave_used', 0)
        self.maternity_miscarriage_leave_used = user_data.get('maternity_miscarriage_leave_used', 0)
        self.is_on_leave = user_data.get('is_on_leave', False)
        self.is_suspended = user_data.get('is_suspended', False)
        
        # Personal Details
        self.father_name = user_data.get('father_name', '')
        self.mother_name = user_data.get('mother_name', '')
        self.spouse_name = user_data.get('spouse_name', '')
        self.date_of_birth = user_data.get('date_of_birth')
        self.gender = user_data.get('gender', '')
        self.blood_group = user_data.get('blood_group', '')
        self.marital_status = user_data.get('marital_status', '')
        self.religion = user_data.get('religion', '')
        self.caste = user_data.get('caste', '')
        self.category = user_data.get('category', '')
        self.nationality = user_data.get('nationality', 'Indian')
        
        # Contact Details
        self.alternate_phone = user_data.get('alternate_phone', '')
        self.address = user_data.get('address', '')
        self.permanent_address = user_data.get('permanent_address', '')
        self.present_address = user_data.get('present_address', '')
        self.city = user_data.get('city', '')
        self.state = user_data.get('state', '')
        self.pincode = user_data.get('pincode', '')
        self.district = user_data.get('district', '')
        self.village = user_data.get('village', '')
        self.post_office = user_data.get('post_office', '')
        
        # Official Documents
        self.aadhar_number = user_data.get('aadhar_number', '')
        self.pan_number = user_data.get('pan_number', '')
        self.passport_number = user_data.get('passport_number', '')
        self.driving_license = user_data.get('driving_license', '')
        self.voter_id = user_data.get('voter_id', '')
        
        # Service Details
        self.date_of_joining = user_data.get('date_of_joining')
        self.date_of_posting = user_data.get('date_of_posting')
        self.place_of_posting = user_data.get('place_of_posting', '')
        self.designation = user_data.get('designation', '')
        self.department = user_data.get('department', '')
        self.section = user_data.get('section', '')
        self.unit = user_data.get('unit', '')
        self.service_number = user_data.get('service_number', '')
        self.employee_code = user_data.get('employee_code', '')
        self.pay_scale = user_data.get('pay_scale', '')
        self.basic_pay = user_data.get('basic_pay', '')
        self.grade_pay = user_data.get('grade_pay', '')
        self.pay_band = user_data.get('pay_band', '')
        
        # Excel-specific fields
        self.old_constable_nos = user_data.get('old_constable_nos', '')
        self.ps_op = user_data.get('ps_op', '')  # Police Station/Outpost
        self.present_duty_location = user_data.get('present_duty_location', '')
        self.class_composition_community = user_data.get('class_composition_community', '')
        self.attached_to_dist = user_data.get('attached_to_dist', '')
        self.attached_from_dist = user_data.get('attached_from_dist', '')
        
        # Education
        self.qualification = user_data.get('qualification', '')
        self.educational_qualification = user_data.get('educational_qualification', '')
        self.professional_qualification = user_data.get('professional_qualification', '')
        self.training = user_data.get('training', '')
        self.courses = user_data.get('courses', '')
        
        # Bank Details
        self.bank_name = user_data.get('bank_name', '')
        self.bank_account_number = user_data.get('bank_account_number', '')
        self.bank_ifsc = user_data.get('bank_ifsc', '')
        self.bank_branch = user_data.get('bank_branch', '')
        
        # Emergency Contact
        self.emergency_contact_name = user_data.get('emergency_contact_name', '')
        self.emergency_contact_phone = user_data.get('emergency_contact_phone', '')
        self.emergency_contact_relation = user_data.get('emergency_contact_relation', '')
        
        # Physical Details
        self.height = user_data.get('height', '')
        self.weight = user_data.get('weight', '')
        self.identification_mark = user_data.get('identification_mark', '')
        
        # Family Details
        self.number_of_children = user_data.get('number_of_children', '')
        self.family_members = user_data.get('family_members', '')
        
        # Other Details
        self.photo = user_data.get('photo', '')
        self.signature = user_data.get('signature', '')
        self.remarks = user_data.get('remarks', '')
        self.status = user_data.get('status', 'Active')
        self.gpf_number = user_data.get('gpf_number', '')
        self.pran_number = user_data.get('pran_number', '')
        self.esi_number = user_data.get('esi_number', '')
        self.uniform_size = user_data.get('uniform_size', '')
        self.shoe_size = user_data.get('shoe_size', '')
    
    @property
    def is_active(self):
        """Override Flask-Login's is_active property"""
        return self._is_active
    
    @staticmethod
    def create_user(username, email, password, role='personnel', rank='', station_id=None):
        """Create a new user"""
        user_data = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,
            'rank': rank,
            'station_id': station_id,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'last_login': None
        }
        result = mongo.db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return User(user_data)
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            return User(user_data) if user_data else None
        except:
            return None
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        user_data = mongo.db.users.find_one({'username': username})
        return User(user_data) if user_data else None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        user_data = mongo.db.users.find_one({'email': email})
        return User(user_data) if user_data else None
    
    @staticmethod
    def from_dict(user_data):
        """Create User instance from dictionary"""
        return User(user_data) if user_data else None
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        mongo.db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'last_login': datetime.utcnow()}}
        )
    
    def get_id(self):
        """Override Flask-Login's get_id method"""
        return self.id


class Personnel:
    """Personnel/Employee model"""
    
    @staticmethod
    def create(data):
        """Create new personnel record"""
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = mongo.db.personnel.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(personnel_id):
        """Get personnel by ID"""
        try:
            return mongo.db.personnel.find_one({'_id': ObjectId(personnel_id)})
        except:
            return None
    
    @staticmethod
    def get_all(filters=None, skip=0, limit=10):
        """Get all personnel with optional filters"""
        query = filters or {}
        cursor = mongo.db.personnel.find(query).skip(skip).limit(limit).sort('name', 1)
        return list(cursor)
    
    @staticmethod
    def count(filters=None):
        """Count personnel records"""
        query = filters or {}
        return mongo.db.personnel.count_documents(query)
    
    @staticmethod
    def update(personnel_id, data):
        """Update personnel record"""
        data['updated_at'] = datetime.utcnow()
        result = mongo.db.personnel.update_one(
            {'_id': ObjectId(personnel_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(personnel_id):
        """Delete personnel record"""
        result = mongo.db.personnel.delete_one({'_id': ObjectId(personnel_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def search(search_term, skip=0, limit=10):
        """Search personnel by name, rank, or other fields"""
        query = {
            '$or': [
                {'name': {'$regex': search_term, '$options': 'i'}},
                {'rank': {'$regex': search_term, '$options': 'i'}},
                {'ein': {'$regex': search_term, '$options': 'i'}},
                {'mobile': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        cursor = mongo.db.personnel.find(query).skip(skip).limit(limit).sort('name', 1)
        return list(cursor)


class Station:
    """Police Station model"""
    
    def __init__(self, data):
        """Initialize Station from dictionary"""
        self.id = str(data.get('_id', ''))
        self.name = data.get('name', '')
        self.code = data.get('code', '')
        self.sdpo_id = data.get('sdpo_id')
        self.sanctioned_strength = data.get('sanctioned_strength', 0)
        self.current_strength = data.get('current_strength', 0)
        self.phone = data.get('phone', '')
        self.is_active = data.get('is_active', True)
        self.created_at = data.get('created_at', datetime.utcnow())
    
    @staticmethod
    def from_dict(data):
        """Create Station instance from dictionary"""
        return Station(data) if data else None
    
    @staticmethod
    def create(data):
        """Create new station"""
        data['created_at'] = datetime.utcnow()
        result = mongo.db.stations.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(station_id):
        """Get station by ID"""
        try:
            return mongo.db.stations.find_one({'_id': ObjectId(station_id)})
        except:
            return None
    
    @staticmethod
    def get_all():
        """Get all stations"""
        return list(mongo.db.stations.find().sort('name', 1))
    
    @staticmethod
    def update(station_id, data):
        """Update station"""
        result = mongo.db.stations.update_one(
            {'_id': ObjectId(station_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(station_id):
        """Delete station"""
        result = mongo.db.stations.delete_one({'_id': ObjectId(station_id)})
        return result.deleted_count > 0


class Attendance:
    """Attendance model"""
    
    @staticmethod
    def create(data):
        """Create attendance record"""
        data['created_at'] = datetime.utcnow()
        result = mongo.db.attendance.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_personnel_and_date(personnel_id, date):
        """Get attendance for personnel on specific date"""
        return mongo.db.attendance.find_one({
            'personnel_id': personnel_id,
            'date': date
        })
    
    @staticmethod
    def get_by_date_range(personnel_id, start_date, end_date):
        """Get attendance records for date range"""
        query = {
            'personnel_id': personnel_id,
            'date': {'$gte': start_date, '$lte': end_date}
        }
        return list(mongo.db.attendance.find(query).sort('date', -1))
    
    @staticmethod
    def update(attendance_id, data):
        """Update attendance record"""
        result = mongo.db.attendance.update_one(
            {'_id': ObjectId(attendance_id)},
            {'$set': data}
        )
        return result.modified_count > 0


class Leave:
    """Leave Application model"""
    
    @staticmethod
    def create(data):
        """Create leave application"""
        data['created_at'] = datetime.utcnow()
        data['status'] = data.get('status', 'pending')
        result = mongo.db.leaves.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(leave_id):
        """Get leave by ID"""
        try:
            return mongo.db.leaves.find_one({'_id': ObjectId(leave_id)})
        except:
            return None
    
    @staticmethod
    def get_by_personnel(personnel_id, skip=0, limit=10):
        """Get leaves for personnel"""
        cursor = mongo.db.leaves.find({'personnel_id': personnel_id}).skip(skip).limit(limit).sort('created_at', -1)
        return list(cursor)
    
    @staticmethod
    def get_pending(skip=0, limit=10):
        """Get pending leave applications"""
        cursor = mongo.db.leaves.find({'status': 'pending'}).skip(skip).limit(limit).sort('created_at', -1)
        return list(cursor)
    
    @staticmethod
    def update_status(leave_id, status, remarks=None):
        """Update leave status"""
        update_data = {
            'status': status,
            'processed_at': datetime.utcnow()
        }
        if remarks:
            update_data['remarks'] = remarks
        
        result = mongo.db.leaves.update_one(
            {'_id': ObjectId(leave_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0


class Transfer:
    """Transfer Order model"""
    
    @staticmethod
    def create(data):
        """Create transfer order"""
        data['created_at'] = datetime.utcnow()
        data['status'] = data.get('status', 'pending')
        result = mongo.db.transfers.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(transfer_id):
        """Get transfer by ID"""
        try:
            return mongo.db.transfers.find_one({'_id': ObjectId(transfer_id)})
        except:
            return None
    
    @staticmethod
    def get_by_personnel(personnel_id):
        """Get transfers for personnel"""
        return list(mongo.db.transfers.find({'personnel_id': personnel_id}).sort('created_at', -1))
    
    @staticmethod
    def get_all(skip=0, limit=10):
        """Get all transfers"""
        cursor = mongo.db.transfers.find().skip(skip).limit(limit).sort('created_at', -1)
        return list(cursor)
    
    @staticmethod
    def update_status(transfer_id, status):
        """Update transfer status"""
        result = mongo.db.transfers.update_one(
            {'_id': ObjectId(transfer_id)},
            {'$set': {'status': status, 'processed_at': datetime.utcnow()}}
        )
        return result.modified_count > 0


class Duty:
    """Duty Assignment model"""
    
    @staticmethod
    def create(data):
        """Create duty assignment"""
        data['created_at'] = datetime.utcnow()
        result = mongo.db.duties.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(duty_id):
        """Get duty by ID"""
        try:
            return mongo.db.duties.find_one({'_id': ObjectId(duty_id)})
        except:
            return None
    
    @staticmethod
    def get_by_personnel(personnel_id):
        """Get duties for personnel"""
        return list(mongo.db.duties.find({'personnel_id': personnel_id}).sort('duty_date', -1))
    
    @staticmethod
    def get_by_date(date):
        """Get duties for specific date"""
        return list(mongo.db.duties.find({'duty_date': date}).sort('personnel_id', 1))
    
    @staticmethod
    def update(duty_id, data):
        """Update duty assignment"""
        result = mongo.db.duties.update_one(
            {'_id': ObjectId(duty_id)},
            {'$set': data}
        )
        return result.modified_count > 0


class Grievance:
    """Grievance model"""
    
    @staticmethod
    def create(data):
        """Create grievance"""
        data['created_at'] = datetime.utcnow()
        data['status'] = data.get('status', 'open')
        result = mongo.db.grievances.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(grievance_id):
        """Get grievance by ID"""
        try:
            return mongo.db.grievances.find_one({'_id': ObjectId(grievance_id)})
        except:
            return None
    
    @staticmethod
    def get_by_personnel(personnel_id):
        """Get grievances for personnel"""
        return list(mongo.db.grievances.find({'personnel_id': personnel_id}).sort('created_at', -1))
    
    @staticmethod
    def get_all(status=None, skip=0, limit=10):
        """Get all grievances"""
        query = {'status': status} if status else {}
        cursor = mongo.db.grievances.find(query).skip(skip).limit(limit).sort('created_at', -1)
        return list(cursor)
    
    @staticmethod
    def update_status(grievance_id, status, response=None):
        """Update grievance status"""
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        if response:
            update_data['response'] = response
        
        result = mongo.db.grievances.update_one(
            {'_id': ObjectId(grievance_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0


class Notification:
    """Notification model"""
    
    @staticmethod
    def create(data):
        """Create notification"""
        data['created_at'] = datetime.utcnow()
        data['is_read'] = False
        result = mongo.db.notifications.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_user(user_id, skip=0, limit=10):
        """Get notifications for user"""
        cursor = mongo.db.notifications.find({'user_id': user_id}).skip(skip).limit(limit).sort('created_at', -1)
        return list(cursor)
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        result = mongo.db.notifications.update_one(
            {'_id': ObjectId(notification_id)},
            {'$set': {'is_read': True}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def get_unread_count(user_id):
        """Get unread notification count"""
        return mongo.db.notifications.count_documents({'user_id': user_id, 'is_read': False})


class Asset:
    """Station Asset model"""
    
    @staticmethod
    def create(data):
        """Create asset"""
        data['created_at'] = datetime.utcnow()
        result = mongo.db.assets.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(asset_id):
        """Get asset by ID"""
        try:
            return mongo.db.assets.find_one({'_id': ObjectId(asset_id)})
        except:
            return None
    
    @staticmethod
    def get_by_station(station_id):
        """Get assets for station"""
        return list(mongo.db.assets.find({'station_id': station_id}).sort('name', 1))
    
    @staticmethod
    def update(asset_id, data):
        """Update asset"""
        data['updated_at'] = datetime.utcnow()
        result = mongo.db.assets.update_one(
            {'_id': ObjectId(asset_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(asset_id):
        """Delete asset"""
        result = mongo.db.assets.delete_one({'_id': ObjectId(asset_id)})
        return result.deleted_count > 0


class AuditLog:
    """Audit Log model for tracking user actions"""
    
    @staticmethod
    def create(user_id, action, details=None):
        """Create audit log entry"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.utcnow(),
            'ip_address': None
        }
        result = mongo.db.audit_logs.insert_one(log_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_user(user_id, skip=0, limit=50):
        """Get audit logs for user"""
        cursor = mongo.db.audit_logs.find({'user_id': user_id}).skip(skip).limit(limit).sort('timestamp', -1)
        return list(cursor)
    
    @staticmethod
    def get_all(skip=0, limit=50):
        """Get all audit logs"""
        cursor = mongo.db.audit_logs.find().skip(skip).limit(limit).sort('timestamp', -1)
        return list(cursor)

class PostingHistory:
    """Posting history model."""
    def __init__(self, **kwargs):
        self.id = str(kwargs.get('_id', ''))
        self.user_id = kwargs.get('user_id')
        self.station_id = kwargs.get('station_id')
        self.from_date = kwargs.get('from_date')
        self.to_date = kwargs.get('to_date')
        self.remarks = kwargs.get('remarks', '')
        self.created_at = kwargs.get('created_at')
    
    @classmethod
    def from_dict(cls, doc):
        if not doc:
            return None
        return cls(**doc)


class Kanglasha:
    """Kanglasha model."""
    def __init__(self, **kwargs):
        self.id = str(kwargs.get('_id', ''))
        self.personnel_id = kwargs.get('personnel_id')
        self.record_type = kwargs.get('record_type')
        self.status = kwargs.get('status')
        self.order_number = kwargs.get('order_number')
        self.order_date = kwargs.get('order_date')
    
    @classmethod
    def from_dict(cls, doc):
        if not doc:
            return None
        return cls(**doc)


class PaySlip:
    """PaySlip model."""
    def __init__(self, **kwargs):
        self.id = str(kwargs.get('_id', ''))
        self.user_id = kwargs.get('user_id')
        self.month = kwargs.get('month')
        self.year = kwargs.get('year')
        self.file_path = kwargs.get('file_path')
        self.file_name = kwargs.get('file_name')
    
    @classmethod
    def from_dict(cls, doc):
        if not doc:
            return None
        return cls(**doc)


class StationAsset:
    """StationAsset model."""
    def __init__(self, **kwargs):
        self.id = str(kwargs.get('_id', ''))
        self.station_id = kwargs.get('station_id')
        self.asset_name = kwargs.get('asset_name')
        self.asset_code = kwargs.get('asset_code')
        self.asset_type = kwargs.get('asset_type')
        self.quantity = kwargs.get('quantity', 1)
        self.condition = kwargs.get('condition')
    
    @classmethod
    def from_dict(cls, doc):
        if not doc:
            return None
        return cls(**doc)
