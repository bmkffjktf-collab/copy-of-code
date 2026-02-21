"""Configuration settings for the application"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/traffic_management"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # App settings
    debug: bool = True
    app_name: str = "Traffic Management Platform"
    app_version: str = "1.0.0"
    secret_key: str = "your-secret-key-here"
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]
    
    # Simulation parameters
    simulation_tick_interval: float = 0.1  # seconds per simulation tick
    max_vehicles_per_lane: int = 50
    
    class Config:
        env_file = ".env"


settings = Settings()
