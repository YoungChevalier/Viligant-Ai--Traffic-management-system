from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="Reviewer") # Admin, Supervisor, Reviewer
    status = Column(String, default="Active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    camera_code = Column(String, unique=True, index=True)
    location_name = Column(String)
    zone = Column(String)
    status = Column(String) # Active, Offline, Maintenance
    health = Column(Integer) # Percentage
    installed_at = Column(DateTime)

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    case_code = Column(String, unique=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    assigned_reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    violation_type = Column(String)
    status = Column(String) # Pending, Approved, Rejected, Escalated
    severity = Column(String) # High, Medium, Low
    confidence_score = Column(Float)
    occurred_at = Column(DateTime)
    vehicle_type = Column(String, nullable=True)
    vehicle_color = Column(String, nullable=True)
    plate_number = Column(String, nullable=True)
    
    camera = relationship("Camera")
    reviewer = relationship("User")
    evidence = relationship("CaseEvidence", back_populates="case")

class CaseEvidence(Base):
    __tablename__ = "case_evidence"
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    type = Column(String) # Image, PlateCrop
    image_url = Column(String)
    captured_at = Column(DateTime)
    
    case = relationship("Case", back_populates="evidence")

class CaseDecision(Base):
    __tablename__ = "case_decisions"
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String) # Approved, Rejected, Escalated
    reason = Column(String, nullable=True)
    decided_at = Column(DateTime, default=datetime.datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    alert_code = Column(String, unique=True)
    title = Column(String)
    description = Column(Text)
    severity = Column(String) # Critical, Warning, Info
    source = Column(String) # Camera, System, OCR
    entity = Column(String)
    status = Column(String) # Unread, Open, Acknowledged, Resolved
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    key = Column(String, unique=True)
    value = Column(String)
