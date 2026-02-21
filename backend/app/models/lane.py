"""Lane model"""
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from .base import BaseModel


class Direction(str, Enum):
    """Direction of lane"""
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class Lane(BaseModel):
    """Represents a lane in an intersection"""
    __tablename__ = "lanes"
    
    name = Column(String(255), nullable=False)
    intersection_id = Column(Integer, ForeignKey("intersections.id"), nullable=False)
    direction = Column(SQLEnum(Direction), nullable=False)
    capacity = Column(Integer, default=30, nullable=False)  # Max vehicles
    length = Column(Float, default=100.0, nullable=False)  # meters
    width = Column(Float, default=3.5, nullable=False)  # meters
    
    # Relationships
    intersection = relationship("Intersection", back_populates="lanes")
    vehicles = relationship("Vehicle", back_populates="lane", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lane {self.name} ({self.direction})>"
