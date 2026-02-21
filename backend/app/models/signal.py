"""Signal model"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum
from .base import BaseModel


class SignalState(str, Enum):
    """Signal state"""
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"


class Signal(BaseModel):
    """Represents a traffic signal"""
    __tablename__ = "signals"
    
    name = Column(String(255), nullable=False)
    intersection_id = Column(Integer, ForeignKey("intersections.id"), nullable=False)
    state = Column(SQLEnum(SignalState), default=SignalState.RED, nullable=False)
    
    # Timing parameters (in seconds)
    green_duration = Column(Integer, default=20, nullable=False)
    yellow_duration = Column(Integer, default=3, nullable=False)
    red_duration = Column(Integer, default=20, nullable=False)
    
    # Current timing
    remaining_time = Column(Float, default=0, nullable=False)
    
    # Optimization
    is_optimized = Column(Boolean, default=False)
    adaptive_green_duration = Column(Integer, nullable=True)
    
    # Relationships
    intersection = relationship("Intersection", back_populates="signals")
    
    def __repr__(self):
        return f"<Signal {self.name} - {self.state}>"
