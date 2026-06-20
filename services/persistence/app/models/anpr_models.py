import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.base import Base

def generate_uuid():
    return uuid.uuid4().hex

class PlateRead(Base):
    __tablename__ = 'plate_reads'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    frame_id = Column(String(64), ForeignKey('frames.id', ondelete="CASCADE"), nullable=False)
    track_id = Column(String(64), ForeignKey('tracks.id', ondelete="SET NULL"), nullable=True)
    
    best_plate_text = Column(String(50), nullable=False)
    best_confidence = Column(Float, nullable=False)
    region = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidates = relationship("PlateCandidateRecord", back_populates="plate_read", cascade="all, delete-orphan")


class PlateCandidateRecord(Base):
    __tablename__ = 'plate_candidates'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    plate_read_id = Column(String(64), ForeignKey('plate_reads.id', ondelete="CASCADE"), nullable=False)
    
    plate_text = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    plate_read = relationship("PlateRead", back_populates="candidates")
