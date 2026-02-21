"""Traffic simulation engine"""
import random
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle, VehicleState, VehicleType
from app.models.signal import Signal, SignalState
from app.models.lane import Lane
from app.models.intersection import Intersection
from app.models.simulation_state import SimulationState
from app.config import settings


class VehicleSimulation:
    """Handles vehicle movement and behavior in traffic simulation"""
    
    def __init__(self):
        self.simulation_time = 0.0
        self.dt = settings.simulation_tick_interval  # Time step
    
    # Vehicle properties by type
    VEHICLE_PROPERTIES = {
        VehicleType.CAR.value: {
            "max_speed": 15.0,  # m/s (~54 km/h)
            "acceleration": 2.0,
            "length": 4.5,
            "width": 2.0,
            "weight": 1000,
        },
        VehicleType.BUS.value: {
            "max_speed": 12.0,
            "acceleration": 1.5,
            "length": 10.0,
            "width": 2.5,
            "weight": 5000,
        },
        VehicleType.TRUCK.value: {
            "max_speed": 12.0,
            "acceleration": 1.2,
            "length": 8.0,
            "width": 2.5,
            "weight": 8000,
        },
        VehicleType.TWO_WHEELER.value: {
            "max_speed": 20.0,
            "acceleration": 3.0,
            "length": 2.0,
            "width": 0.8,
            "weight": 200,
        },
        VehicleType.AUTO.value: {
            "max_speed": 14.0,
            "acceleration": 2.5,
            "length": 3.5,
            "width": 1.5,
            "weight": 600,
        },
        VehicleType.AMBULANCE.value: {
            "max_speed": 25.0,
            "acceleration": 4.0,
            "length": 5.0,
            "width": 2.2,
            "weight": 2000,
        },
        VehicleType.FIRE_ENGINE.value: {
            "max_speed": 22.0,
            "acceleration": 3.5,
            "length": 7.0,
            "width": 2.5,
            "weight": 5000,
        },
        VehicleType.POLICE.value: {
            "max_speed": 25.0,
            "acceleration": 4.0,
            "length": 5.0,
            "width": 2.0,
            "weight": 1500,
        },
    }
    
    def add_vehicle(
        self, 
        db: Session, 
        intersection_id: int, 
        lane_id: int, 
        vehicle_type: VehicleType,
        is_emergency: bool = False
    ) -> Vehicle:
        """Add a new vehicle to the simulation"""
        vehicle_id = f"{vehicle_type.value}-{uuid.uuid4().hex[:8]}"
        
        props = self.VEHICLE_PROPERTIES.get(vehicle_type.value, {})
        
        vehicle = Vehicle(
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            intersection_id=intersection_id,
            lane_id=lane_id,
            position=0.0,
            speed=0.0,
            max_speed=props.get("max_speed", 15.0),
            length=props.get("length", 4.5),
            width=props.get("width", 2.0),
            weight=props.get("weight", 1000),
            state=VehicleState.WAITING,
            is_emergency=is_emergency,
            waiting_time=0,
            entry_time=self.simulation_time,
        )
        
        db.add(vehicle)
        db.commit()
        return vehicle
    
    def update_vehicle_movement(self, vehicle: Vehicle, lane: Lane, signal: Signal, db: Session):
        """Update vehicle position and speed based on signal and traffic conditions"""
        
        if vehicle.state == VehicleState.EXITED:
            return
        
        # Get vehicles ahead
        vehicles_ahead = db.query(Vehicle).filter(
            Vehicle.lane_id == vehicle.lane_id,
            Vehicle.position > vehicle.position
        ).all()
        
        # Calculate safe following distance
        min_distance = vehicle.length + 2.0  # 2m safety margin
        
        # Determine target speed based on signal
        if signal.state == SignalState.GREEN:
            target_speed = vehicle.max_speed
            vehicle.state = VehicleState.MOVING
        elif signal.state == SignalState.YELLOW:
            target_speed = max(0, vehicle.max_speed * 0.5)  # Half speed
            vehicle.state = VehicleState.MOVING
        else:  # RED
            target_speed = 0
            vehicle.state = VehicleState.STOPPED
        
        # Check if emergency vehicle - can go even on red
        if vehicle.is_emergency:
            target_speed = vehicle.max_speed
            vehicle.state = VehicleState.MOVING
        
        # Reduce speed if vehicle ahead
        if vehicles_ahead:
            nearest_vehicle = min(vehicles_ahead, key=lambda v: v.position)
            distance_to_ahead = nearest_vehicle.position - vehicle.position
            
            if distance_to_ahead < min_distance:
                target_speed = 0
                vehicle.state = VehicleState.STOPPED
            elif distance_to_ahead < min_distance * 2:
                target_speed = min(target_speed, nearest_vehicle.speed * 0.8)
        
        # Apply acceleration/deceleration
        current_speed = vehicle.speed
        acceleration = 2.0  # m/s²
        
        if target_speed > current_speed:
            vehicle.speed = min(target_speed, current_speed + acceleration * self.dt)
        elif target_speed < current_speed:
            vehicle.speed = max(target_speed, current_speed - acceleration * self.dt)
        else:
            vehicle.speed = target_speed
        
        # Update position
        vehicle.position += vehicle.speed * self.dt
        
        # Update waiting time
        if vehicle.speed == 0:
            vehicle.waiting_time += 1
        
        # Check if vehicle exited the lane
        if vehicle.position >= lane.length:
            vehicle.state = VehicleState.EXITED
            vehicle.exit_time = self.simulation_time
            vehicle.lane_id = None
        
        db.commit()
    
    def simulate_step(self, db: Session, intersection_id: int, dt: float):
        """Simulate one time step for all vehicles at intersection"""
        self.simulation_time += dt
        
        # Get all active vehicles
        vehicles = db.query(Vehicle).filter(
            Vehicle.intersection_id == intersection_id,
            Vehicle.state != VehicleState.EXITED
        ).all()
        
        # Get signal states
        signals = db.query(Signal).filter_by(intersection_id=intersection_id).all()
        signal_map = {s.id: s for s in signals}
        
        # Update each vehicle
        for vehicle in vehicles:
            if vehicle.lane_id:
                lane = db.query(Lane).filter_by(id=vehicle.lane_id).first()
                # Simplified: use first signal (in reality, map lanes to signals)
                signal = signal_map.get(signals[0].id) if signals else None
                
                if lane and signal:
                    self.update_vehicle_movement(vehicle, lane, signal, db)
        
        # Update signal timings
        for signal in signals:
            if signal.remaining_time > 0:
                signal.remaining_time -= dt
            else:
                # Transition to next state
                if signal.state == SignalState.GREEN:
                    signal.state = SignalState.YELLOW
                    signal.remaining_time = signal.yellow_duration
                elif signal.state == SignalState.YELLOW:
                    signal.state = SignalState.RED
                    signal.remaining_time = signal.red_duration
                else:  # RED
                    signal.state = SignalState.GREEN
                    green_time = signal.adaptive_green_duration or signal.green_duration
                    signal.remaining_time = green_time
        
        db.commit()
    
    def get_simulation_metrics(self, db: Session, intersection_id: int) -> Dict:
        """Calculate current simulation metrics"""
        vehicles = db.query(Vehicle).filter_by(intersection_id=intersection_id).all()
        
        total_vehicles = len(vehicles)
        exited_vehicles = len([v for v in vehicles if v.state == VehicleState.EXITED])
        
        total_waiting_time = sum(v.waiting_time for v in vehicles if v.state != VehicleState.EXITED)
        
        avg_waiting_time = (
            total_waiting_time / len([v for v in vehicles if v.state != VehicleState.EXITED])
            if len([v for v in vehicles if v.state != VehicleState.EXITED]) > 0
            else 0
        )
        
        # Calculate throughput (vehicles/minute)
        throughput = 0
        if exited_vehicles > 0:
            throughput = (exited_vehicles / (self.simulation_time + 0.1)) * 60
        
        return {
            "total_vehicles": total_vehicles,
            "exited_vehicles": exited_vehicles,
            "total_waiting_time": total_waiting_time,
            "avg_waiting_time": avg_waiting_time,
            "throughput": throughput,
        }
