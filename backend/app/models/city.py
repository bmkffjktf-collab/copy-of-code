"""City model"""
from sqlalchemy import Column, String, Float, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class City(BaseModel):
    """Represents an Indian city"""
    __tablename__ = "cities"
    
    name = Column(String(255), unique=True, nullable=False, index=True)
    state = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    population = Column(String(255), nullable=True)
    
    # Relationships
    intersections = relationship("Intersection", back_populates="city", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<City {self.name}, {self.state}>"
