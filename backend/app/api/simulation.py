"""Simulation routes"""
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.simulation_state import SimulationState
from app.models.intersection import Intersection
from app.models.lane import Lane
from app.models.vehicle import Vehicle
from app.models.signal import Signal
from app.schemas.simulation import SimulationStart, SimulationMetrics, LaneMetrics, SignalMetrics
from app.simulation import VehicleSimulation
from app.optimization import SignalOptimizer
from app.config import settings

router = APIRouter(prefix="/api/simulation", tags=["simulation"])

vehicle_sim = VehicleSimulation()
signal_optimizer = SignalOptimizer()

# Store simulation state in memory
_simulations = {}


@router.post("/start")
def start_simulation(sim_start: SimulationStart, db: Session = Depends(get_db)):
    """Start a traffic simulation for an intersection"""
    # Verify intersection exists
    intersection = db.query(Intersection).filter(Intersection.id == sim_start.intersection_id).first()
    if not intersection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Intersection not found")
    
    # Create or get simulation state
    sim_state = db.query(SimulationState).filter(
        SimulationState.intersection_id == sim_start.intersection_id
    ).first()
    
    if not sim_state:
        sim_state = SimulationState(
            city_id=intersection.city_id,
            intersection_id=sim_start.intersection_id,
            is_running=1
        )
        db.add(sim_state)
    else:
        sim_state.is_running = 1
    
    db.commit()
    
    _simulations[sim_start.intersection_id] = {
        "running": True,
        "duration": sim_start.duration,
        "speed_factor": sim_start.speed_factor,
        "elapsed": 0,
    }
    
    return {"status": "started", "intersection_id": sim_start.intersection_id}


@router.post("/stop/{intersection_id}")
def stop_simulation(intersection_id: int, db: Session = Depends(get_db)):
    """Stop simulation"""
    sim_state = db.query(SimulationState).filter(
        SimulationState.intersection_id == intersection_id
    ).first()
    
    if sim_state:
        sim_state.is_running = 0
        db.commit()
    
    if intersection_id in _simulations:
        _simulations[intersection_id]["running"] = False
    
    return {"status": "stopped", "intersection_id": intersection_id}


@router.post("/optimize/{intersection_id}")
def optimize_signals(intersection_id: int, db: Session = Depends(get_db)):
    """Optimize signal timings for intersection"""
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Intersection not found")
    
    # Run optimization
    optimized_timings = signal_optimizer.optimize_signal_timing(db, intersection_id)
    
    # Check for emergency vehicles
    emergency_detected = signal_optimizer.detect_emergency_corridor(db, intersection_id)
    
    return {
        "status": "optimized",
        "intersection_id": intersection_id,
        "optimized_timings": optimized_timings,
        "emergency_detected": emergency_detected,
    }


@router.get("/metrics/{intersection_id}", response_model=SimulationMetrics)
def get_simulation_metrics(intersection_id: int, db: Session = Depends(get_db)):
    """Get current simulation metrics"""
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Intersection not found")
    
    # Get vehicle metrics
    vehicle_metrics = vehicle_sim.get_simulation_metrics(db, intersection_id)
    
    # Get congestion score
    congestion_score = signal_optimizer.predict_congestion_level(db, intersection_id)
    
    # Get lane metrics
    lanes = db.query(Lane).filter(Lane.intersection_id == intersection_id).all()
    lane_metrics = []
    
    for lane in lanes:
        vehicles = db.query(Vehicle).filter(Vehicle.lane_id == lane.id).all()
        active_vehicles = [v for v in vehicles if v.state.value != "EXITED"]
        
        lane_metrics.append(LaneMetrics(
            lane_id=lane.id,
            lane_name=lane.name,
            vehicle_count=len(active_vehicles),
            congestion_score=signal_optimizer.calculate_congestion_score(lane, db),
            avg_wait_time=sum(v.waiting_time for v in active_vehicles) / len(active_vehicles) if active_vehicles else 0,
            throughput=vehicle_metrics.get("throughput", 0),
        ))
    
    # Get signal metrics
    signals = db.query(Signal).filter(Signal.intersection_id == intersection_id).all()
    signal_metrics = []
    
    for signal in signals:
        signal_metrics.append(SignalMetrics(
            signal_id=signal.id,
            signal_name=signal.name,
            state=signal.state.value,
            remaining_time=signal.remaining_time,
            green_duration=signal.adaptive_green_duration or signal.green_duration,
            is_optimized=signal.is_optimized,
        ))
    
    return SimulationMetrics(
        simulation_time=vehicle_sim.simulation_time,
        is_running=bool(_simulations.get(intersection_id, {}).get("running")),
        total_vehicles=vehicle_metrics.get("total_vehicles", 0),
        vehicles_exited=vehicle_metrics.get("exited_vehicles", 0),
        avg_waiting_time=vehicle_metrics.get("avg_waiting_time", 0),
        total_waiting_time=vehicle_metrics.get("total_waiting_time", 0),
        congestion_score=congestion_score,
        vehicles_per_minute=vehicle_metrics.get("throughput", 0),
        lanes=lane_metrics,
        signals=signal_metrics,
    )


@router.post("/step/{intersection_id}")
def simulation_step(intersection_id: int, dt: float = settings.simulation_tick_interval, db: Session = Depends(get_db)):
    """Advance simulation by one step"""
    if intersection_id not in _simulations or not _simulations[intersection_id]["running"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Simulation not running")
    
    # Update vehicle movements
    vehicle_sim.simulate_step(db, intersection_id, dt)
    
    # Periodically optimize signals
    if int(vehicle_sim.simulation_time) % 10 == 0:  # Every 10 seconds
        signal_optimizer.optimize_signal_timing(db, intersection_id)
    
    return {"status": "stepped", "simulation_time": vehicle_sim.simulation_time}
