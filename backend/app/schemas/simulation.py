"""Simulation schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class SimulationStart(BaseModel):
    """Schema for starting simulation"""
    intersection_id: int = Field(..., gt=0)
    duration: int = Field(default=300, ge=10, le=3600)  # seconds
    speed_factor: float = Field(default=1.0, ge=0.1, le=10.0)


class LaneMetrics(BaseModel):
    """Lane traffic metrics"""
    lane_id: int
    lane_name: str
    vehicle_count: int
    congestion_score: float
    avg_wait_time: float
    throughput: float


class SignalMetrics(BaseModel):
    """Signal metrics"""
    signal_id: int
    signal_name: str
    state: str
    remaining_time: float
    green_duration: int
    is_optimized: bool


class SimulationMetrics(BaseModel):
    """Simulation metrics"""
    simulation_time: float
    is_running: bool
    total_vehicles: int
    vehicles_exited: int
    avg_waiting_time: float
    total_waiting_time: float
    congestion_score: float  # 0-100
    vehicles_per_minute: float
    lanes: list[LaneMetrics]
    signals: list[SignalMetrics]


class TrafficMetrics(BaseModel):
    """Overall traffic metrics"""
    intersection_id: int
    city_id: int
    metrics: SimulationMetrics
    timestamp: float
