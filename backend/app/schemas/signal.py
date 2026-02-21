"""Signal schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class SignalStateEnum(str, Enum):
    """Signal state"""
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"


class SignalBase(BaseModel):
    """Base signal schema"""
    name: str = Field(..., min_length=1, max_length=255)
    intersection_id: int = Field(..., gt=0)
    green_duration: int = Field(default=20, ge=5, le=120)
    yellow_duration: int = Field(default=3, ge=1, le=10)
    red_duration: int = Field(default=20, ge=5, le=120)


class SignalUpdate(BaseModel):
    """Schema for updating a signal"""
    green_duration: Optional[int] = None
    yellow_duration: Optional[int] = None
    red_duration: Optional[int] = None


class SignalResponse(SignalBase):
    """Response schema for signal"""
    id: int
    state: SignalStateEnum
    remaining_time: float
    is_optimized: bool
    adaptive_green_duration: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
