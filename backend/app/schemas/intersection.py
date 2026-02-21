"""Intersection schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IntersectionBase(BaseModel):
    """Base intersection schema"""
    name: str = Field(..., min_length=1, max_length=255)
    city_id: int = Field(..., gt=0)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    description: Optional[str] = None
    num_lanes: int = Field(default=4, ge=2, le=16)


class IntersectionCreate(IntersectionBase):
    """Schema for creating an intersection"""
    pass


class IntersectionUpdate(BaseModel):
    """Schema for updating an intersection"""
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    num_lanes: Optional[int] = None


class IntersectionResponse(IntersectionBase):
    """Response schema for intersection"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
