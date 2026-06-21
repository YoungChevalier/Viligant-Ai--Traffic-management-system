from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.domain import Case, CaseDecision, CaseEvidence, User
from app.core.auth import get_current_user
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class CaseDecisionRequest(BaseModel):
    action: str
    reason: Optional[str] = None

@router.get("")
def get_cases(status: Optional[str] = None, violation_type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Case)
    if status:
        query = query.filter(Case.status == status)
    if violation_type:
        query = query.filter(Case.violation_type == violation_type)
        
    cases = query.limit(200).all()
    
    return [
        {
            "id": c.case_code,
            "type": c.violation_type,
            "plate": c.plate_number or "Unknown",
            "cam": c.camera.camera_code if c.camera else "Unknown",
            "time": c.occurred_at.isoformat() if c.occurred_at else None,
            "score": c.confidence_score,
            "status": c.status,
            "assignee": c.reviewer.name if c.reviewer else "Unassigned",
            "thumb": "📷"
        }
        for c in cases
    ]

@router.get("/{case_code}")
def get_case(case_code: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_code == case_code).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    evidence = db.query(CaseEvidence).filter(CaseEvidence.case_id == case.id).all()
    
    return {
        "id": case.case_code,
        "status": case.status,
        "type": case.violation_type,
        "severity": case.severity,
        "score": case.confidence_score,
        "time": case.occurred_at.isoformat() if case.occurred_at else None,
        "vehicleType": case.vehicle_type,
        "vehicleColor": case.vehicle_color,
        "plate": case.plate_number or "Unknown",
        "cam": case.camera.location_name if case.camera else "Unknown",
        "evidence": [e.image_url for e in evidence],
        "assignee": case.reviewer.name if case.reviewer else "Unassigned",
    }

@router.post("/{case_code}/decision")
def submit_decision(case_code: str, req: CaseDecisionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.case_code == case_code).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    decision = CaseDecision(
        case_id=case.id,
        reviewer_id=current_user.id,
        action=req.action,
        reason=req.reason,
        decided_at=datetime.utcnow()
    )
    db.add(decision)
    
    case.status = req.action
    case.assigned_reviewer_id = current_user.id
    
    db.commit()
    return {"status": "success", "new_status": req.action}
