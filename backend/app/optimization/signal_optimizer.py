"""Traffic signal optimization engine"""
from typing import List, Dict
import numpy as np
from scipy.optimize import minimize
from sqlalchemy.orm import Session
from app.models.signal import Signal, SignalState
from app.models.lane import Lane
from app.models.vehicle import Vehicle


class SignalOptimizer:
    """Optimizes traffic signal timings using weighted congestion model"""
    
    def __init__(self, min_green: int = 5, max_green: int = 60):
        self.min_green = min_green
        self.max_green = max_green
    
    # Vehicle weights for congestion calculation
    VEHICLE_WEIGHTS = {
        "CAR": 1.0,
        "AUTO": 0.8,
        "TWO_WHEELER": 0.4,
        "BUS": 2.5,
        "TRUCK": 3.0,
    }
    
    def calculate_congestion_score(self, lane: Lane, db: Session) -> float:
        """
        Calculate congestion score for a lane using weighted model.
        Takes into account vehicle types and road capacity.
        """
        vehicles = db.query(Vehicle).filter_by(lane_id=lane.id).all()
        
        if not vehicles:
            return 0.0
        
        # Calculate weighted vehicle count
        weighted_count = sum(
            self.VEHICLE_WEIGHTS.get(v.vehicle_type.value, 1.0) 
            for v in vehicles
        )
        
        # Normalize by lane capacity
        capacity_utilization = weighted_count / lane.capacity
        
        # Congestion score: 0-100
        congestion = min(100.0, capacity_utilization * 100)
        
        return congestion
    
    def get_intersection_congestion(self, db: Session, intersection_id: int) -> Dict[int, float]:
        """Get congestion scores for all lanes in intersection"""
        lanes = db.query(Lane).filter_by(intersection_id=intersection_id).all()
        
        congestion_map = {}
        for lane in lanes:
            congestion_map[lane.id] = self.calculate_congestion_score(lane, db)
        
        return congestion_map
    
    def optimize_signal_timing(
        self, 
        db: Session, 
        intersection_id: int, 
        total_cycle_time: int = 60
    ) -> Dict[int, int]:
        """
        Optimize signal timings for intersection lanes.
        Uses congestion scores to allocate green time proportionally.
        """
        congestion_scores = self.get_intersection_congestion(db, intersection_id)
        signals = db.query(Signal).filter_by(intersection_id=intersection_id).all()
        
        if not signals or not congestion_scores:
            return {}
        
        # Allocate green time proportionally to congestion
        total_congestion = sum(congestion_scores.values())
        
        optimized_timings = {}
        
        for signal in signals:
            # Group lanes by signal (simplified: first n lanes to first signal, etc)
            signal_idx = signals.index(signal)
            lane_indices = list(congestion_scores.keys())
            
            if signal_idx < len(lane_indices):
                lane_id = lane_indices[signal_idx]
                congestion = congestion_scores.get(lane_id, 0)
                
                # Proportional allocation
                if total_congestion > 0:
                    proportion = congestion / total_congestion
                else:
                    proportion = 1.0 / len(signals)
                
                # Calculate green time (with min/max constraints)
                green_time = max(
                    self.min_green,
                    min(self.max_green, int(proportion * (total_cycle_time - 10)))
                )
                
                optimized_timings[signal.id] = green_time
                signal.adaptive_green_duration = green_time
                signal.is_optimized = True
        
        db.commit()
        return optimized_timings
    
    def detect_emergency_corridor(
        self, 
        db: Session, 
        intersection_id: int
    ) -> bool:
        """
        Detect if there's an emergency vehicle in intersection.
        If yes, create instant green corridor.
        """
        emergency_vehicles = db.query(Vehicle).filter(
            Vehicle.intersection_id == intersection_id,
            Vehicle.is_emergency == True
        ).all()
        
        if emergency_vehicles:
            # Set all signals to green for emergency corridor
            signals = db.query(Signal).filter_by(intersection_id=intersection_id).all()
            for signal in signals:
                signal.state = SignalState.GREEN
                signal.remaining_time = 999  # Effectively permanent
            
            db.commit()
            return True
        
        return False
    
    def predict_congestion_level(self, db: Session, intersection_id: int) -> float:
        """
        Predict short-term congestion level (0-100).
        Based on current vehicle count and entry rate.
        """
        lanes = db.query(Lane).filter_by(intersection_id=intersection_id).all()
        
        total_congestion = 0
        for lane in lanes:
            total_congestion += self.calculate_congestion_score(lane, db)
        
        avg_congestion = total_congestion / len(lanes) if lanes else 0
        return min(100.0, avg_congestion)
