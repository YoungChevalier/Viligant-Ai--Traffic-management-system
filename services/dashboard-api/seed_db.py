import os
import sys
import datetime
import random
import bcrypt

# Add project root to sys path to allow importing app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, Base, SessionLocal
from app.models.domain import User, Camera, Case, CaseEvidence, CaseDecision, Alert, Setting

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_db():
    print("Dropping and recreating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Seed Users
        print("Seeding Users...")
        admin = User(name="System Admin", email="admin@vigilant.ai", password_hash=hash_password("admin123"), role="Admin")
        supervisor = User(name="S. Supervisor", email="supervisor@vigilant.ai", password_hash=hash_password("sup123"), role="Supervisor")
        reviewer1 = User(name="R. Vargas", email="rvargas@vigilant.ai", password_hash=hash_password("rev123"), role="Reviewer")
        reviewer2 = User(name="A. Smith", email="asmith@vigilant.ai", password_hash=hash_password("rev123"), role="Reviewer")
        db.add_all([admin, supervisor, reviewer1, reviewer2])
        db.commit()

        # Seed Cameras
        print("Seeding Cameras...")
        cameras = []
        directions = ["Northbound", "Southbound", "Eastbound", "Westbound"]
        zones = ["Highway", "Urban", "School Zone"]
        for i in range(1, 13):
            status = "Active"
            health = random.randint(85, 100)
            if i == 4:
                status = "Offline"
                health = 0
            if i == 7:
                status = "Maintenance"
                health = 50
            
            cam = Camera(
                camera_code=f"CAM-{directions[i%4][0]}-{i:02d}",
                location_name=f"Intersection {i}",
                zone=random.choice(zones),
                status=status,
                health=health,
                installed_at=datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(100, 500))
            )
            db.add(cam)
            cameras.append(cam)
        db.commit()

        # Seed Cases
        print("Seeding Cases...")
        violation_types = ["Red-Light Violation", "Speeding", "Helmet Non-Compliance", "Wrong-Side Driving", "Triple Riding", "Stop-Line Violation", "Illegal Parking"]
        severities = ["High", "Medium", "Low"]
        statuses = ["Pending", "Pending", "Pending", "Approved", "Rejected", "Escalated"] # more pending
        
        for i in range(1, 101):
            cam = random.choice(cameras)
            vt = random.choice(violation_types)
            status = random.choice(statuses)
            reviewer_id = None
            if status in ["Approved", "Rejected"]:
                reviewer_id = random.choice([reviewer1.id, reviewer2.id])

            case = Case(
                case_code=f"CAS-{datetime.datetime.utcnow().strftime('%Y%m%d')}-{i:04d}",
                camera_id=cam.id,
                assigned_reviewer_id=reviewer_id,
                violation_type=vt,
                status=status,
                severity=random.choice(severities),
                confidence_score=round(random.uniform(70.0, 99.9), 1),
                occurred_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(1, 10000)),
                vehicle_type=random.choice(["Car", "Motorcycle", "Truck", "Bus"]),
                vehicle_color=random.choice(["Red", "Blue", "Black", "White", "Silver"]),
                plate_number=f"ABC-{random.randint(1000, 9999)}" if random.random() > 0.2 else None
            )
            db.add(case)
            db.flush() # flush to get case.id

            # Add Evidence
            ev1 = CaseEvidence(case_id=case.id, type="Image", image_url=f"/static/violation_{i%5}.jpg", captured_at=case.occurred_at)
            db.add(ev1)
            
            # Add Decision if not pending
            if status != "Pending":
                dec = CaseDecision(
                    case_id=case.id,
                    reviewer_id=reviewer_id,
                    action=status,
                    reason="Clear evidence." if status == "Approved" else "Unclear plate." if status == "Rejected" else "Need supervisor review.",
                    decided_at=case.occurred_at + datetime.timedelta(minutes=random.randint(1, 60))
                )
                db.add(dec)

        db.commit()

        # Seed Alerts
        print("Seeding Alerts...")
        alerts = [
            Alert(alert_code="ALT-001", title="Camera Offline - Connection Lost", description="Lost heartbeat for 5 mins.", severity="Critical", source="Camera", entity="CAM-N-04", status="Unread"),
            Alert(alert_code="ALT-002", title="OCR Confidence Drop Spike", description="Average dropped below 60%.", severity="Warning", source="OCR", entity="System-Wide", status="Open"),
            Alert(alert_code="ALT-003", title="Reviewer Queue Overloaded", description="Backlog exceeds 80 cases.", severity="Warning", source="Queue", entity="R. Vargas", status="Acknowledged"),
        ]
        db.add_all(alerts)
        db.commit()

        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
