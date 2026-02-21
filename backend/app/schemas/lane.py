"""Lane schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class DirectionEnum(str, Enum):
    """Lane direction"""
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class LaneBase(BaseModel):
    """Base lane schema"""
    name: str = Field(..., min_length=1, max_length=255)
    intersection_id: int = Field(..., gt=0)
    direction: DirectionEnum
    capacity: int = Field(default=30, ge=10, le=100)
    length: float = Field(default=100.0, gt=0)
    width: float = Field(default=3.5, gt=0)


class LaneCreate(LaneBase):
    """Schema for creating a lane"""
    pass


class LaneResponse(LaneBase):
    """Response schema for lane"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
