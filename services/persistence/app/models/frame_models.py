import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.base import Base

def generate_uuid():
    return uuid.uuid4().hex

class Frame(Base):
    __tablename__ = 'frames'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    camera_id = Column(String(64), ForeignKey('cameras.id', ondelete="CASCADE"), nullable=False)
    storage_path = Column(String(500), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    processed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    metrics = relationship("FrameQualityMetric", back_populates="frame", cascade="all, delete-orphan")


class FrameQualityMetric(Base):
    __tablename__ = 'frame_quality_metrics'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    frame_id = Column(String(64), ForeignKey('frames.id', ondelete="CASCADE"), nullable=False)
    
    metric_name = Column(String(100), nullable=False) # e.g., 'blur_score', 'brightness'
    metric_value = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    frame = relationship("Frame", back_populates="metrics")
