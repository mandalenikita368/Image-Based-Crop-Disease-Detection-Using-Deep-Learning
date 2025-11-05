from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    detections = relationship("DetectionHistory", back_populates="user", cascade="all, delete-orphan")

class DetectionHistory(Base):
    __tablename__ = 'detection_history'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image_name = Column(String(255))
    predicted_class = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    crop_type = Column(String(50))
    disease_name = Column(String(100))
    top_3_predictions = Column(Text)
    detection_date = Column(DateTime, default=datetime.utcnow, index=True)
    notes = Column(Text)
    
    user = relationship("User", back_populates="detections")
