import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from ..db.base import Base

def generate_uuid():
    return uuid.uuid4().hex

class Detection(Base):
    __tablename__ = 'detections'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    frame_id = Column(String(64), ForeignKey('frames.id', ondelete="CASCADE"), nullable=False)
    
    class_name = Column(String(100), nullable=False) # e.g., 'car', 'person'
    confidence = Column(Float, nullable=False)
    
    # Bounding Box Coordinates
    bbox_x1 = Column(Float, nullable=False)
    bbox_y1 = Column(Float, nullable=False)
    bbox_x2 = Column(Float, nullable=False)
    bbox_y2 = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
