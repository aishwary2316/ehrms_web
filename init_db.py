"""
Database initialization script for E-HRMS
Creates sample data for testing all functionalities
"""
from app import create_app
from extensions import db
from models import (User, Station, Leave, Transfer, Duty, Attendance, PaySlip,
                   Grievance, Notification, AuditLog, PostingHistory)
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with sample data."""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if User.query.count() > 0:
            response = input("Database already contains data. Reset? (yes/no): ")
            if response.lower() != 'yes':
                print("Initialization cancelled.")
                return
            
            print("Dropping all tables...")
            db.drop_all()
            db.create_all()
        
        print("\n=== Creating Stations ===")
        stations_data = [
            {"name": "Imphal West PS", "code": "IWPS", "phone": "0385-2411111",
             "sanctioned_c": 20, "sanctioned_hc": 10, "sanctioned_asi": 5, "sanctioned_si": 3, "sanctioned_inspector": 1},
            {"name": "Lamphel PS", "code": "LPHL", "phone": "0385-2422222",
             "sanctioned_c": 15, "sanctioned_hc": 8, "sanctioned_asi": 4, "sanctioned_si": 2, "sanctioned_inspector": 1},
            {"name": "Singjamei PS", "code": "SGJM", "phone": "0385-2433333",
             "sanctioned_c": 18, "sanctioned_hc": 9, "sanctioned_asi": 5, "sanctioned_si": 3, "sanctioned_inspector": 1},
            {"name": "Porompat PS", "code": "PRPT", "phone": "0385-2444444",
             "sanctioned_c": 12, "sanctioned_hc": 6, "sanctioned_asi": 3, "sanctioned_si": 2, "sanctioned_inspector": 1},
            {"name": "Heingang PS", "code": "HGNG", "phone": "0385-2455555",
             "sanctioned_c": 14, "sanctioned_hc": 7, "sanctioned_asi": 4, "sanctioned_si": 2, "sanctioned_inspector": 1},
        ]
        
        stations = []
        for data in stations_data:
            station = Station(**data, address=f"{data['name']} Area, Imphal West", is_active=True)
            db.session.add(station)
            stations.append(station)
        
        db.session.commit()
        print(f"Created {len(stations)} stations")
        
        print("\n=== Creating Users ===")
        
        # SP
        sp = User(
            employee_id="SP001",
            name="R.K. Singh",
            email="sp@iwpolice.gov.in",
            phone="9876543210",
            rank="SP",
            date_of_joining=datetime(2020, 1, 15).date(),
            date_of_birth=datetime(1975, 5, 10).date(),
            is_active=True
        )
        sp.set_password("password123")
        db.session.add(sp)
        print(f"Created SP: {sp.name}")
        
        # ASP
        asp = User(
            employee_id="ASP001",
            name="M. Devi",
            email="asp@iwpolice.gov.in",
            phone="9876543211",
            rank="ASP",
            date_of_joining=datetime(2021, 3, 1).date(),
            date_of_birth=datetime(1980, 8, 15).date(),
            is_active=True
        )
        asp.set_password("password123")
        db.session.add(asp)
        print(f"Created ASP: {asp.name}")
        
        # SDPO
        sdpo = User(
            employee_id="SDPO001",
            name="L. Kumar",
            email="sdpo@iwpolice.gov.in",
            phone="9876543212",
            rank="SDPO",
            date_of_joining=datetime(2019, 6, 10).date(),
            date_of_birth=datetime(1978, 12, 20).date(),
            is_active=True
        )
        sdpo.set_password("password123")
        db.session.add(sdpo)
        print(f"Created SDPO: {sdpo.name}")
        
        db.session.commit()
        
        # Assign SDPO to stations
        for station in stations[:3]:
            station.sdpo_id = sdpo.id
        db.session.commit()
        
        # Inspectors/OCs - one per station
        inspectors = []
        for i, station in enumerate(stations, 1):
            inspector = User(
                employee_id=f"INS{i:03d}",
                name=f"Inspector {chr(64+i)}. Sharma",
                email=f"oc{i}@iwpolice.gov.in",
                phone=f"987654{3210+i}",
                rank="Inspector",
                current_station_id=station.id,
                date_of_joining=datetime(2018, random.randint(1, 12), random.randint(1, 28)).date(),
                date_of_birth=datetime(1982, random.randint(1, 12), random.randint(1, 28)).date(),
                is_active=True
            )
            inspector.set_password("password123")
            db.session.add(inspector)
            inspectors.append(inspector)
        
        db.session.commit()
        
        # Create posting history for inspectors
        for inspector in inspectors:
            history = PostingHistory(
                user_id=inspector.id,
                station_id=inspector.current_station_id,
                from_date=inspector.date_of_joining,
                remarks="Initial posting"
            )
            db.session.add(history)
        
        db.session.commit()
        print(f"Created {len(inspectors)} Inspectors/OCs")
        
        # Create SI, ASI, HC, C for each station
        all_personnel = []
        ranks_config = [
            ("SI", 2),
            ("ASI", 4),
            ("HC", 8),
            ("C", 15)
        ]
        
        emp_counter = {"SI": 1, "ASI": 1, "HC": 1, "C": 1}
        
        for station in stations:
            for rank, count in ranks_config:
                for i in range(count):
                    user = User(
                        employee_id=f"{rank}{emp_counter[rank]:04d}",
                        name=f"{rank} {chr(65 + (emp_counter[rank] % 26))}. {'Singh' if emp_counter[rank] % 2 == 0 else 'Kumar'}",
                        email=f"{rank.lower()}{emp_counter[rank]}@iwpolice.gov.in",
                        phone=f"98765{10000 + emp_counter[rank]}",
                        rank=rank,
                        current_station_id=station.id,
                        date_of_joining=datetime(2015 + random.randint(0, 7), random.randint(1, 12), random.randint(1, 28)).date(),
                        date_of_birth=datetime(1985 + random.randint(0, 10), random.randint(1, 12), random.randint(1, 28)).date(),
                        is_active=True,
                        earned_leave_balance=random.randint(20, 30),
                        casual_leave_balance=random.randint(10, 15),
                        medical_leave_balance=random.randint(8, 12)
                    )
                    user.set_password("password123")
                    db.session.add(user)
                    all_personnel.append(user)
                    
                    emp_counter[rank] += 1
        
        db.session.commit()
        
        # Create posting history for all personnel
        for user in all_personnel:
            history = PostingHistory(
                user_id=user.id,
                station_id=user.current_station_id,
                from_date=user.date_of_joining,
                remarks="Initial posting"
            )
            db.session.add(history)
        
        db.session.commit()
        print(f"Created {len(all_personnel)} personnel (SI, ASI, HC, C)")
        
        print("\n=== Creating Leave Applications ===")
        # Create sample leave applications
        leave_count = 0
        for _ in range(30):
            personnel = random.choice(all_personnel)
            start_date = datetime.utcnow().date() + timedelta(days=random.randint(-30, 30))
            num_days = random.randint(2, 7)
            end_date = start_date + timedelta(days=num_days - 1)
            
            leave = Leave(
                user_id=personnel.id,
                leave_type=random.choice(['Earned', 'Casual', 'Medical']),
                start_date=start_date,
                end_date=end_date,
                num_days=num_days,
                reason=random.choice(['Family function', 'Medical checkup', 'Personal work', 'Emergency at home']),
                leaving_station=random.choice([True, False]),
                status=random.choice(['Pending', 'Approved_OC', 'Approved_SDPO', 'Approved']),
                applied_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
            )
            db.session.add(leave)
            leave_count += 1
        
        db.session.commit()
        print(f"Created {leave_count} leave applications")
        
        print("\n=== Creating Transfer Orders ===")
        # Create sample transfers
        transfer_count = 0
        for i in range(5):
            personnel = random.choice([p for p in all_personnel if p.rank in ['C', 'HC', 'ASI', 'SI']])
            from_station = personnel.current_station
            to_station = random.choice([s for s in stations if s.id != from_station.id])
            
            order_date = datetime.utcnow().date() - timedelta(days=random.randint(1, 30))
            
            transfer = Transfer(
                order_number=f"TO/2025/{i+1:04d}",
                user_id=personnel.id,
                from_station_id=from_station.id,
                to_station_id=to_station.id,
                transfer_type="Intra-district",
                order_date=order_date,
                effective_date=order_date,
                issued_by_id=sp.id,
                status=random.choice(['Ordered', 'Relieved', 'Awaiting_Joining', 'Joined'])
            )
            db.session.add(transfer)
            transfer_count += 1
        
        db.session.commit()
        print(f"Created {transfer_count} transfer orders")
        
        print("\n=== Creating Duty Orders ===")
        # Create sample duties
        duty_count = 0
        for i in range(20):
            station = random.choice(stations)
            personnel = random.choice([p for p in all_personnel if p.current_station_id == station.id])
            duty_date = datetime.utcnow().date() + timedelta(days=random.randint(-10, 10))
            
            duty = Duty(
                duty_order_number=f"DO/2025/{i+1:04d}",
                event_name=random.choice(['Traffic Control', 'Bandobast', 'Patrol Duty', 'Security Duty', 'VIP Security']),
                location=random.choice(['Main Market', 'Government Office', 'Stadium', 'City Center', 'Border Area']),
                duty_date=duty_date,
                start_time=datetime.strptime("09:00", "%H:%M").time(),
                end_time=datetime.strptime("17:00", "%H:%M").time(),
                duration_hours=8.0,
                assignment_type='By_Name',
                user_id=personnel.id,
                station_id=station.id,
                created_by_id=random.choice(inspectors).id,
                is_present=random.choice([True, False]),
                actual_hours=random.uniform(6.0, 8.5)
            )
            db.session.add(duty)
            duty_count += 1
        
        db.session.commit()
        print(f"Created {duty_count} duty orders")
        
        print("\n=== Creating Attendance Records ===")
        # Create attendance for last 7 days
        attendance_count = 0
        for days_ago in range(7):
            date = datetime.utcnow().date() - timedelta(days=days_ago)
            for personnel in all_personnel[:50]:  # Sample for first 50 personnel
                status = random.choices(
                    ['Present', 'Absent', 'Late', 'On_Leave'],
                    weights=[70, 5, 15, 10]
                )[0]
                
                attendance = Attendance(
                    user_id=personnel.id,
                    station_id=personnel.current_station_id,
                    date=date,
                    status=status,
                    check_in_time=datetime.strptime("09:00", "%H:%M").time() if status in ['Present', 'Late'] else None,
                    check_out_time=datetime.strptime("17:00", "%H:%M").time() if status == 'Present' else None
                )
                db.session.add(attendance)
                attendance_count += 1
        
        db.session.commit()
        print(f"Created {attendance_count} attendance records")
        
        print("\n=== Creating Grievances ===")
        # Create sample grievances
        grievance_count = 0
        for i in range(10):
            personnel = random.choice(all_personnel)
            grievance = Grievance(
                user_id=personnel.id,
                subject=random.choice([
                    'Leave approval delay',
                    'Transfer request',
                    'Duty allocation concern',
                    'Facility improvement request',
                    'Equipment requirement'
                ]),
                description="This is a sample grievance description. " * 5,
                category=random.choice(['Leave', 'Transfer', 'Duty', 'Workplace', 'Other']),
                status=random.choice(['Submitted', 'Under_Review', 'Resolved']),
                priority='Normal',
                submitted_at=datetime.utcnow() - timedelta(days=random.randint(1, 20))
            )
            db.session.add(grievance)
            grievance_count += 1
        
        db.session.commit()
        print(f"Created {grievance_count} grievances")
        
        print("\n=== Database Initialization Complete! ===")
        print("\nLogin Credentials:")
        print("==================")
        print("SP:        Employee ID: SP001       Password: password123")
        print("ASP:       Employee ID: ASP001      Password: password123")
        print("SDPO:      Employee ID: SDPO001     Password: password123")
        print("Inspector: Employee ID: INS001      Password: password123")
        print("SI:        Employee ID: SI0001      Password: password123")
        print("ASI:       Employee ID: ASI0001     Password: password123")
        print("HC:        Employee ID: HC0001      Password: password123")
        print("C:         Employee ID: C0001       Password: password123")
        print("\nTotal Users Created:", User.query.count())
        print("Total Stations:", Station.query.count())
        print("Total Leave Applications:", Leave.query.count())
        print("Total Transfers:", Transfer.query.count())
        print("Total Duties:", Duty.query.count())
        print("Total Attendance Records:", Attendance.query.count())
        print("Total Grievances:", Grievance.query.count())

if __name__ == '__main__':
    init_database()
