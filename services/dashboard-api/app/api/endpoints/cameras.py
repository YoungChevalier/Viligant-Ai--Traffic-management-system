from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.domain import Camera

router = APIRouter()

@router.get("")
def get_cameras(db: Session = Depends(get_db)):
    cameras = db.query(Camera).all()
    return [
        {
            "id": c.camera_code,
            "name": c.location_name,
            "zone": c.zone,
            "status": c.status,
            "health": c.health,
            "installed_at": c.installed_at.isoformat() if c.installed_at else None
        }
        for c in cameras
    ]
