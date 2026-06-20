import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.base import Base

def generate_uuid():
    return uuid.uuid4().hex

class ViolationCandidateRecord(Base):
    __tablename__ = 'violation_candidates'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    track_id = Column(String(64), ForeignKey('tracks.id', ondelete="SET NULL"), nullable=True)
    frame_id = Column(String(64), ForeignKey('frames.id', ondelete="SET NULL"), nullable=True)
    
    violation_type = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = 'incidents'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    track_id = Column(String(64), ForeignKey('tracks.id', ondelete="SET NULL"), nullable=True)
    
    status = Column(String(50), nullable=False, default="OPEN")
    confidence_score = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    score_breakdown = relationship("IncidentScore", back_populates="incident", uselist=False, cascade="all, delete-orphan")
    evidence_assets = relationship("EvidenceAsset", back_populates="incident", cascade="all, delete-orphan")
    review_actions = relationship("ReviewAction", back_populates="incident", cascade="all, delete-orphan")

class IncidentScore(Base):
    __tablename__ = 'incident_scores'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    incident_id = Column(String(64), ForeignKey('incidents.id', ondelete="CASCADE"), unique=True, nullable=False)
    
    detection_score = Column(Float, default=0.0)
    tracking_score = Column(Float, default=0.0)
    anpr_score = Column(Float, default=0.0)
    rule_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("Incident", back_populates="score_breakdown")

class EvidenceAsset(Base):
    __tablename__ = 'evidence_assets'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    incident_id = Column(String(64), ForeignKey('incidents.id', ondelete="CASCADE"), nullable=False)
    
    asset_type = Column(String(50), nullable=False)
    storage_path = Column(String(500), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("Incident", back_populates="evidence_assets")

class ReviewAction(Base):
    __tablename__ = 'review_actions'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    incident_id = Column(String(64), ForeignKey('incidents.id', ondelete="CASCADE"), nullable=False)
    
    reviewer_id = Column(String(64), nullable=False)
    action = Column(String(50), nullable=False)
    notes = Column(String(1000), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("Incident", back_populates="review_actions")
