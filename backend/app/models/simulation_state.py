"""Simulation state model"""
from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class SimulationState(BaseModel):
    """Stores simulation state for cities and intersections"""
    __tablename__ = "simulation_states"
    
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    intersection_id = Column(Integer, ForeignKey("intersections.id"), nullable=True)
    
    # Simulation timing
    simulation_time = Column(Float, default=0.0, nullable=False)
    is_running = Column(Integer, default=0, nullable=False)  # 0 = stopped, 1 = running
    
    # Metrics
    total_vehicles = Column(Integer, default=0, nullable=False)
    vehicles_exited = Column(Integer, default=0, nullable=False)
    total_waiting_time = Column(Float, default=0.0, nullable=False)
    avg_waiting_time = Column(Float, default=0.0, nullable=False)
    congestion_score = Column(Float, default=0.0, nullable=False)  # 0-100
    
    # Throughput
    vehicles_per_minute = Column(Float, default=0.0, nullable=False)
    
    # Metadata (JSON for flexibility)
    state_metadata = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<SimulationState city_id={self.city_id} time={self.simulation_time}>"
