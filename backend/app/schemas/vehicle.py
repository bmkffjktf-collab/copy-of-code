"""Vehicle schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class VehicleTypeEnum(str, Enum):
    """Vehicle type"""
    CAR = "CAR"
    BUS = "BUS"
    TRUCK = "TRUCK"
    TWO_WHEELER = "TWO_WHEELER"
    AUTO = "AUTO"
    AMBULANCE = "AMBULANCE"
    FIRE_ENGINE = "FIRE_ENGINE"
    POLICE = "POLICE"


class VehicleStateEnum(str, Enum):
    """Vehicle state"""
    WAITING = "WAITING"
    MOVING = "MOVING"
    STOPPED = "STOPPED"
    EXITED = "EXITED"


class VehicleCreate(BaseModel):
    """Schema for creating a vehicle in simulation"""
    vehicle_type: VehicleTypeEnum
    intersection_id: int = Field(..., gt=0)
    lane_id: int = Field(..., gt=0)
    is_emergency: bool = Field(default=False)


class VehicleResponse(BaseModel):
    """Response schema for vehicle"""
    id: int
    vehicle_id: str
    vehicle_type: VehicleTypeEnum
    intersection_id: int
    lane_id: Optional[int]
    position: float
    speed: float
    max_speed: float
    state: VehicleStateEnum
    is_emergency: bool
    waiting_time: int
    entry_time: float
    exit_time: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
