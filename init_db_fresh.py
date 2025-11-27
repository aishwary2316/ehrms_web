"""
Initialize database within Flask app context to ensure proper binding
"""
from datetime import datetime, timedelta
import random
from extensions import db
from app import create_app
from models import User, Station, Leave, Transfer, Duty, Attendance, Grievance, PostingHistory

# Create app and context
app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    
    print("\n=== Creating Stations ===")
    stations = [
        Station(code="LPS", name="Lamphel Police Station", phone="0385-2441234",
                sanctioned_c=15, sanctioned_hc=8, sanctioned_asi=4, sanctioned_si=2, sanctioned_inspector=1),
        Station(code="IPS", name="Imphal Police Station", phone="0385-2442234",
                sanctioned_c=20, sanctioned_hc=10, sanctioned_asi=5, sanctioned_si=3, sanctioned_inspector=1),
        Station(code="SPS", name="Singjamei Police Station", phone="0385-2443234",
                sanctioned_c=12, sanctioned_hc=6, sanctioned_asi=3, sanctioned_si=2, sanctioned_inspector=1),
        Station(code="PPS", name="Porompat Police Station", phone="0385-2444234",
                sanctioned_c=10, sanctioned_hc=5, sanctioned_asi=3, sanctioned_si=2, sanctioned_inspector=1),
        Station(code="KPS", name="Kwakeithel Police Station", phone="0385-2445234",
                sanctioned_c=13, sanctioned_hc=7, sanctioned_asi=4, sanctioned_si=2, sanctioned_inspector=1)
    ]
    
    for station in stations:
        db.session.add(station)
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
    db.session.commit()
    print(f"Created SP: {sp.name}")
    
    # ASP
    asp = User(
        employee_id="ASP001",
        name="M. Devi",
        email="asp@iwpolice.gov.in",
        phone="9876543211",
        rank="ASP",
        date_of_joining=datetime(2018, 3, 20).date(),
        date_of_birth=datetime(1980, 8, 15).date(),
        is_active=True
    )
    asp.set_password("password123")
    db.session.add(asp)
    db.session.commit()
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
    db.session.commit()
    print(f"Created SDPO: {sdpo.name}")
    
    # Assign SDPO to stations
    for station in stations[:3]:
        station.sdpo_id = sdpo.id
    db.session.commit()
    
    # Inspectors - one per station
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
    
    # Create other ranks
    all_personnel = []
    ranks_config = [
        ("SI", 2),
        ("ASI", 3),
        ("HC", 6),
        ("C", 12)
    ]
    
    emp_counter = {"SI": 1, "ASI": 1, "HC": 1, "C": 1}
    
    for station in stations:
        for rank, count in ranks_config:
            for _ in range(count):
                user = User(
                    employee_id=f"{rank}{emp_counter[rank]:04d}",
                    name=f"{rank} {chr(65 + random.randint(0, 25))}. {random.choice(['Kumar', 'Singh', 'Devi', 'Sharma', 'Patel'])}",
                    email=f"{rank.lower()}{emp_counter[rank]}@iwpolice.gov.in",
                    phone=f"98765{40000 + emp_counter[rank]}",
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
    
    print("\n=== Database Initialization Complete! ===\n")
    print("Login Credentials:")
    print("=" * 50)
    print("SP:        Employee ID: SP001       Password: password123")
    print("ASP:       Employee ID: ASP001      Password: password123")
    print("SDPO:      Employee ID: SDPO001     Password: password123")
    print("Inspector: Employee ID: INS001      Password: password123")
    print("SI:        Employee ID: SI0001      Password: password123")
    print("Constable: Employee ID: C0001       Password: password123")
    print("=" * 50)
    
    # Verify
    total_users = User.query.count()
    print(f"\nTotal Users Created: {total_users}")
    print(f"Total Stations: {Station.query.count()}")
    
    # Test login
    print("\n=== Testing Login ===")
    test_user = User.query.filter_by(employee_id='SP001').first()
    if test_user:
        print(f"✓ User SP001 found: {test_user.name}")
        print(f"✓ Password check: {test_user.check_password('password123')}")
    else:
        print("✗ User SP001 NOT FOUND!")

print("\nDatabase file created at: ehrms.db")
print("You can now start the Flask app with: python app.py")
