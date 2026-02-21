"""Vehicle routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vehicle import Vehicle, VehicleType
from app.models.lane import Lane
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.simulation import VehicleSimulation

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])

vehicle_sim = VehicleSimulation()


@router.post("/inject", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def inject_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """Inject a new vehicle into the simulation"""
    # Verify lane exists
    lane = db.query(Lane).filter(Lane.id == vehicle.lane_id).first()
    if not lane:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lane not found")
    
    # Check lane capacity
    active_vehicles = db.query(Vehicle).filter(
        Vehicle.lane_id == vehicle.lane_id,
        Vehicle.position < lane.length
    ).count()
    
    if active_vehicles >= lane.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Lane is at capacity"
        )
    
    # Add vehicle to simulation
    new_vehicle = vehicle_sim.add_vehicle(
        db=db,
        intersection_id=vehicle.intersection_id,
        lane_id=vehicle.lane_id,
        vehicle_type=VehicleType(vehicle.vehicle_type),
        is_emergency=vehicle.is_emergency
    )
    
    return new_vehicle


@router.get("", response_model=list[VehicleResponse])
def get_vehicles(intersection_id: int = None, db: Session = Depends(get_db)):
    """Get all active vehicles, optionally filtered by intersection"""
    query = db.query(Vehicle)
    if intersection_id:
        query = query.filter(Vehicle.intersection_id == intersection_id)
    return query.all()


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get vehicle by ID"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle
