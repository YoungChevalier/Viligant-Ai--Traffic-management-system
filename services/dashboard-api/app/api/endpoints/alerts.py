from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.domain import Alert

router = APIRouter()

@router.get("")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return [
        {
            "id": a.alert_code,
            "title": a.title,
            "description": a.description,
            "severity": a.severity,
            "source": a.source,
            "entity": a.entity,
            "status": a.status,
            "timestamp": a.created_at.isoformat() if a.created_at else None
        }
        for a in alerts
    ]
