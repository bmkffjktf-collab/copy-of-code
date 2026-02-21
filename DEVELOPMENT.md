# AI-Powered Traffic Management Platform - Development Guide

## Project Overview

This is a comprehensive traffic management and simulation platform for Indian cities with AI-driven signal optimization.

## Technology Stack

### Backend
- **Framework**: FastAPI (modern, fast, async)
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Cache**: Redis
- **Optimization**: SciPy
- **Language**: Python 3.11

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: CSS3

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Cache**: Redis 7

## Key Components

### 1. Traffic Simulation Engine (`app/simulation/vehicle_simulation.py`)
- Simulates realistic vehicle movement
- Handles acceleration/deceleration
- Manages lane changes and collisions
- Updates vehicle positions based on signal state

### 2. Signal Optimization (`app/optimization/signal_optimizer.py`)
- Weighted congestion model
- Proportional green time allocation
- Emergency corridor detection
- Short-term congestion prediction

### 3. Database Models
- **City**: Urban centers in India
- **Intersection**: Traffic intersection points
- **Lane**: Individual traffic lanes
- **Signal**: Traffic signal with state and timing
- **Vehicle**: Individual vehicles in simulation
- **SimulationState**: Metrics and performance data

### 4. API Layer
- RESTful endpoints for all operations
- Real-time metrics and state
- Vehicle injection
- Simulation control

### 5. Frontend UI
- City selection dashboard
- Interactive traffic visualization
- Real-time metrics display
- Vehicle injection interface

## Development Workflow

### Adding New Features

#### Example 1: Add a New Vehicle Type

1. Update `app/models/vehicle.py`:
```python
class VehicleType(str, Enum):
    # Add new type
    RICKSHAW = "RICKSHAW"
```

2. Add properties in `VehicleSimulation.VEHICLE_PROPERTIES`
3. Update frontend `VehicleInjector.tsx` VEHICLE_TYPES list
4. Migrate database (create migration if needed)

#### Example 2: Modify Signal Optimization

Edit `app/optimization/signal_optimizer.py`:
```python
# Update weight model
VEHICLE_WEIGHTS = {
    "CAR": 1.0,
    # Adjust weights as needed
}

# Modify optimization logic in optimize_signal_timing()
```

### Running Tests

```bash
cd backend
pytest tests/

# Run specific test
pytest tests/test_optimization.py::test_congestion_calculation -v

# With coverage
pytest --cov=app tests/
```

### Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "from app.database import init_db; init_db()"
python seed_db.py
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## API Architecture

```
FastAPI Server (0.0.0.0:8000)
├── /api/cities
│   ├── GET /            # List all cities
│   ├── POST /           # Create city
│   ├── GET /{id}        # Get city
│   ├── PUT /{id}        # Update city
│   └── DELETE /{id}     # Delete city
├── /api/intersections
│   ├── GET /            # List intersections
│   ├── POST /           # Create intersection
│   ├── GET /{id}        # Get intersection
│   ├── PUT /{id}        # Update intersection
│   └── DELETE /{id}     # Delete intersection
├── /api/vehicles
│   ├── POST /inject     # Inject vehicle
│   ├── GET /            # List vehicles
│   └── GET /{id}        # Get vehicle
└── /api/simulation
    ├── POST /start      # Start simulation
    ├── POST /stop/{id}  # Stop simulation
    ├── POST /optimize   # Optimize signals
    ├── GET /metrics     # Get metrics
    └── POST /step       # Step simulation
```

## Data Flow

```
1. User selects city/intersection (Frontend)
   ↓
2. API fetches intersection details (Backend)
   ↓
3. User starts simulation
   ↓
4. Simulation engine initializes (Traffic sim)
   ↓
5. User injects vehicles
   ↓
6. Vehicles stored in database
   ↓
7. Each simulation step:
   - Update vehicle positions
   - Update signal states
   - Calculate metrics
   - Check emergency conditions
   - Every 10s: Optimize signals
   ↓
8. Frontend polls metrics endpoint
   ↓
9. Dashboard updates with live data
```

## Performance Considerations

### Database Optimization
- Index on `vehicle_id` for quick lookups
- Index on `intersection_id` for filtering
- Connection pooling (default 5 connections)

### Simulation Performance
- Efficient collision detection
- Optimized vehicle movement calculation
- Batched database commits

### Frontend Performance
- React components memoization
- Efficient canvas rendering
- Debounced API calls

## Configuration

### Environment Variables

`backend/.env`:
```
DATABASE_URL=postgresql://user:password@localhost/db
REDIS_URL=redis://localhost:6379/0
DEBUG=True
MAX_VEHICLES_PER_LANE=50
SIMULATION_TICK_INTERVAL=0.1
```

### Feature Flags

Could be added to config.py for A/B testing:
```python
ENABLE_EMERGENCY_CORRIDOR = True
ENABLE_ADAPTIVE_SIGNALS = True
ENABLE_REROUTING = False
```

## Debugging

### Backend Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
```

### Frontend DevTools
- React DevTools browser extension
- Network tab to monitor API calls
- Console for client-side errors

### Database
```bash
# Connect to PostgreSQL
psql postgresql://user:password@localhost/traffic_management

# View tables
\dt

# Check vehicle data
SELECT * FROM vehicles LIMIT 10;
```

## Deployment

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_ORIGINS
- [ ] Use strong database password
- [ ] Enable Redis persistence
- [ ] Setup SSL/HTTPS
- [ ] Configure database backups
- [ ] Monitor application logs
- [ ] Setup health checks

### Docker Deployment
```bash
docker-compose -f docker-compose.yml up -d
```

### Scaling Considerations
- Separate read/write databases
- Redis clustering for cache
- Load balancing for API servers
- Separate simulation workers

## Common Issues

### Database Connection Failed
```
Solution: Check DATABASE_URL format and PostgreSQL is running
psql postgresql://user:password@localhost/traffic_management
```

### Redis Connection Failed
```
Solution: Check Redis is running
redis-cli ping
```

### Frontend API Errors
```
Solution: Check CORS settings in backend config
Ensure backend URL is correct in frontend
```

## Future Roadmap

1. WebSocket support for real-time updates
2. Machine learning prediction models
3. Mobile app (React Native)
4. Multi-intersection coordination
5. Advanced visualization (3D/AR)
6. Real GPS integration
7. Traffic incident management
8. Historical data analytics

## Contributing Guidelines

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test
3. Commit: `git commit -am "Add feature"`
4. Push: `git push origin feature/name`
5. Create Pull Request

## Q&A

**Q: How frequently are signals optimized?**
A: Every 10 seconds during simulation (configurable)

**Q: Can I scale this to multiple cities?**
A: Yes, database supports multiple cities and intersections

**Q: How realistic is the simulation?**
A: Physics-based with vehicle properties and traffic rules, but simplified for performance

**Q: Can I integrate real vehicle data?**
A: Yes, modify VehicleInjector to accept GPS data instead of manual injection

---

For more information, see README.md
