import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.base import Base

def generate_uuid():
    return uuid.uuid4().hex

class Camera(Base):
    __tablename__ = 'cameras'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default='ONLINE')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    calibration = relationship("CameraCalibration", back_populates="camera", uselist=False, cascade="all, delete-orphan")
    zones = relationship("CameraZone", back_populates="camera", cascade="all, delete-orphan")


class CameraCalibration(Base):
    __tablename__ = 'camera_calibrations'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    camera_id = Column(String(64), ForeignKey('cameras.id', ondelete="CASCADE"), unique=True, nullable=False)
    
    # Storing matrix/distortion data as JSON strings for simplicity
    intrinsic_matrix = Column(String(500), nullable=True)
    distortion_coeffs = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    camera = relationship("Camera", back_populates="calibration")


class CameraZone(Base):
    __tablename__ = 'camera_zones'
    
    id = Column(String(64), primary_key=True, default=generate_uuid)
    camera_id = Column(String(64), ForeignKey('cameras.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    zone_type = Column(String(100), nullable=False) # e.g., 'SPEED_LIMIT', 'NO_PARKING'
    polygon = Column(String(1000), nullable=False)  # JSON serialized list of points
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    camera = relationship("Camera", back_populates="zones")
