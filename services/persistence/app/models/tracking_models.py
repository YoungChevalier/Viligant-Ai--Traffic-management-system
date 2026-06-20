import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.base import Base

def generate_uuid():
    return uuid.uuid4().hex

class Track(Base):
    __tablename__ = 'tracks'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    camera_id = Column(String(64), nullable=False)
    class_name = Column(String(100), nullable=False)
    
    is_active = Column(Boolean, default=True)
    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    history = relationship("TrackHistory", back_populates="track", cascade="all, delete-orphan", order_by="TrackHistory.timestamp")


class TrackHistory(Base):
    __tablename__ = 'track_history'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    track_id = Column(String(64), ForeignKey('tracks.id', ondelete="CASCADE"), nullable=False)
    frame_id = Column(String(64), ForeignKey('frames.id', ondelete="SET NULL"), nullable=True)
    
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    speed = Column(Float, nullable=True)
    
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    track = relationship("Track", back_populates="history")
