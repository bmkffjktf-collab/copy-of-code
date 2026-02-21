"""City schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CityBase(BaseModel):
    """Base city schema"""
    name: str = Field(..., min_length=1, max_length=255)
    state: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    description: Optional[str] = None
    population: Optional[str] = None


class CityCreate(CityBase):
    """Schema for creating a city"""
    pass


class CityUpdate(BaseModel):
    """Schema for updating a city"""
    name: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    population: Optional[str] = None


class CityResponse(CityBase):
    """Response schema for city"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
