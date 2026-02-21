"""Unit tests for signal optimization"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.base import Base
from app.models.city import City
from app.models.intersection import Intersection
from app.models.lane import Lane, Direction
from app.models.vehicle import Vehicle, VehicleType, VehicleState
from app.optimization import SignalOptimizer


@pytest.fixture
def db_session():
    """Create test database session"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_data(db_session: Session):
    """Create sample data for testing"""
    city = City(name="Test City", state="Test State", latitude=0.0, longitude=0.0)
    db_session.add(city)
    db_session.commit()
    
    intersection = Intersection(
        name="Test Intersection",
        city_id=city.id,
        latitude=0.0,
        longitude=0.0,
        num_lanes=4,
    )
    db_session.add(intersection)
    db_session.commit()
    
    lanes = []
    for direction in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
        lane = Lane(
            name=f"Lane {direction.value}",
            intersection_id=intersection.id,
            direction=direction,
            capacity=30,
            length=100.0,
            width=3.5,
        )
        db_session.add(lane)
        lanes.append(lane)
    
    db_session.commit()
    
    return {
        "city": city,
        "intersection": intersection,
        "lanes": lanes,
    }


def test_congestion_calculation(db_session: Session, sample_data):
    """Test congestion score calculation"""
    optimizer = SignalOptimizer()
    
    # Add vehicles to a lane
    lane = sample_data["lanes"][0]
    for i in range(5):
        vehicle = Vehicle(
            vehicle_id=f"car-{i}",
            vehicle_type=VehicleType.CAR,
            intersection_id=sample_data["intersection"].id,
            lane_id=lane.id,
            position=0.0,
            speed=0.0,
            max_speed=15.0,
            state=VehicleState.WAITING,
            entry_time=0.0,
        )
        db_session.add(vehicle)
    
    db_session.commit()
    
    # Calculate congestion
    congestion = optimizer.calculate_congestion_score(lane, db_session)
    
    # Should be non-zero
    assert congestion > 0
    # Should not exceed 100
    assert congestion <= 100


def test_emergency_detection(db_session: Session, sample_data):
    """Test emergency vehicle detection"""
    optimizer = SignalOptimizer()
    
    # Add emergency vehicle
    cycle_optimize = optimizer
    vehicle = Vehicle(
        vehicle_id="ambulance-1",
        vehicle_type=VehicleType.AMBULANCE,
        intersection_id=sample_data["intersection"].id,
        lane_id=sample_data["lanes"][0].id,
        position=0.0,
        speed=0.0,
        max_speed=25.0,
        state=VehicleState.MOVING,
        is_emergency=True,
        entry_time=0.0,
    )
    db_session.add(vehicle)
    db_session.commit()
    
    # Detect emergency
    has_emergency = optimizer.detect_emergency_corridor(db_session, sample_data["intersection"].id)
    
    assert has_emergency is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
