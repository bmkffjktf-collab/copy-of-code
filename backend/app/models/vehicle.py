"""Vehicle model"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum
from .base import BaseModel


class VehicleType(str, Enum):
    """Type of vehicle"""
    CAR = "CAR"
    BUS = "BUS"
    TRUCK = "TRUCK"
    TWO_WHEELER = "TWO_WHEELER"
    AUTO = "AUTO"
    AMBULANCE = "AMBULANCE"
    FIRE_ENGINE = "FIRE_ENGINE"
    POLICE = "POLICE"


class VehicleState(str, Enum):
    """Vehicle state"""
    WAITING = "WAITING"
    MOVING = "MOVING"
    STOPPED = "STOPPED"
    EXITED = "EXITED"


class Vehicle(BaseModel):
    """Represents a vehicle in the simulation"""
    __tablename__ = "vehicles"
    
    vehicle_id = Column(String(50), unique=True, nullable=False, index=True)
    vehicle_type = Column(SQLEnum(VehicleType), nullable=False)
    intersection_id = Column(Integer, ForeignKey("intersections.id"), nullable=False)
    lane_id = Column(Integer, ForeignKey("lanes.id"), nullable=True)
    
    # Position and movement
    position = Column(Float, default=0.0, nullable=False)  # Distance from start of lane
    speed = Column(Float, default=0.0, nullable=False)  # m/s
    max_speed = Column(Float, default=15.0, nullable=False)  # m/s
    
    # Vehicle properties
    length = Column(Float, default=4.5, nullable=False)  # meters
    width = Column(Float, default=2.0, nullable=False)  # meters
    weight = Column(Float, default=1000.0, nullable=False)  # kg
    
    # States
    state = Column(SQLEnum(VehicleState), default=VehicleState.WAITING, nullable=False)
    is_emergency = Column(Boolean, default=False, nullable=False)
    waiting_time = Column(Integer, default=0, nullable=False)  # seconds
    
    # Entry/Exit
    entry_time = Column(Float, nullable=False)
    exit_time = Column(Float, nullable=True)
    
    # Relationships
    intersection = relationship("Intersection", back_populates="vehicles")
    lane = relationship("Lane", back_populates="vehicles")
    
    def __repr__(self):
        return f"<Vehicle {self.vehicle_id} ({self.vehicle_type})>"
