from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import register_routes

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the Dashboard API FastAPI application.
    """
    app = FastAPI(
        title="Traffic Dashboard API",
        description="Serves incident data, evidence assets, and review actions to the frontend.",
        version="0.1.0",
    )

    import os
    cors_origin = os.getenv("CORS_ORIGIN", "*")
    origins = [origin.strip() for origin in cors_origin.split(",")] if cors_origin != "*" else ["*"]

    # Enable CORS for frontend clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.db.database import engine, Base, SessionLocal
    from app.models import domain # ensure models are loaded
    
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed initial data if empty
    db = SessionLocal()
    try:
        import bcrypt
        import datetime
        import random
        if db.query(domain.User).count() == 0:
            # Create user
            pw_hash = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = domain.User(name="Admin", email="admin@vigilantai.com", password_hash=pw_hash, role="Admin")
            db.add(admin)
            
            # Create camera
            cam = domain.Camera(camera_code="CAM-001", location_name="Main Intersection", zone="Downtown", status="Active", health=100, installed_at=datetime.datetime.utcnow())
            db.add(cam)
            db.commit()

            # Create cases
            for i in range(1, 15):
                case = domain.Case(
                    case_code=f"CAS-{1000+i}",
                    camera_id=cam.id,
                    violation_type=random.choice(["Speeding", "Red Light", "Illegal Parking", "Wrong Side", "No Helmet"]),
                    status=random.choice(["Pending", "Pending", "Flagged", "Reviewed"]),
                    severity=random.choice(["High", "Medium", "Low"]),
                    confidence_score=round(random.uniform(0.7, 0.99), 2),
                    occurred_at=datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(1, 48)),
                    plate_number=f"MH12{random.randint(1000, 9999)}"
                )
                db.add(case)
            db.commit()
    except Exception as e:
        print("Error seeding database:", e)
    finally:
        db.close()

    register_routes(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "dashboard-api"}

    return app

app = create_app()
