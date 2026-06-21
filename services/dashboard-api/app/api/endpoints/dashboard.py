from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.domain import Case, Alert

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_cases = db.query(Case).count()
    pending_cases = db.query(Case).filter(Case.status == "Pending").count()
    escalated_cases = db.query(Case).filter(Case.status == "Escalated").count()
    active_alerts = db.query(Alert).filter(Alert.status.in_(["Unread", "Open"])).count()
    
    # We could also do trends here but let's mock the charts for now 
    # to save time as requested by user, while returning real KPIs.
    
    return {
        "kpis": {
            "total_cases": total_cases,
            "pending_review": pending_cases,
            "escalated": escalated_cases,
            "active_alerts": active_alerts
        }
    }
