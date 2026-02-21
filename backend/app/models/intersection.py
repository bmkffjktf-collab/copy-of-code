"""Intersection model"""
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Intersection(BaseModel):
    """Represents a traffic intersection"""
    __tablename__ = "intersections"
    
    name = Column(String(255), nullable=False, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    num_lanes = Column(Integer, default=4, nullable=False)
    
    # Relationships
    city = relationship("City", back_populates="intersections")
    lanes = relationship("Lane", back_populates="intersection", cascade="all, delete-orphan")
    signals = relationship("Signal", back_populates="intersection", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="intersection")
    
    def __repr__(self):
        return f"<Intersection {self.name}>"
