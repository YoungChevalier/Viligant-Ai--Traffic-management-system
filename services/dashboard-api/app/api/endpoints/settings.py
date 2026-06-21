from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.domain import Setting

router = APIRouter()

@router.get("")
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(Setting).all()
    return [
        {"category": s.category, "key": s.key, "value": s.value}
        for s in settings
    ]
