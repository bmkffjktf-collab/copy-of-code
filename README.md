# Nationwide AI-Powered Traffic Management and Simulation Platform for India

A comprehensive traffic management system that simulates real-world Indian mixed-traffic scenarios with AI-driven signal optimization, emergency vehicle detection, and intelligent rerouting.

## 🚀 Features

### Core Features
- **Interactive Map-Based UI**: Select any Indian city and intersection to simulate
- **Vehicle Injection System**: Manually inject different vehicle types (cars, buses, two-wheelers, trucks, emergency vehicles) into specific lanes
- **AI Signal Optimization**: Weighted congestion model that optimizes signal timings based on vehicle density and road capacity
- **Emergency Corridor**: Instant green corridor for emergency vehicles (ambulances, fire engines, police)
- **Congestion Prediction**: Short-term traffic prediction to prevent bottlenecks
- **Real-Time Dashboard**: Live metrics with animated traffic flow, signal states, and performance indicators
- **Intelligent Rerouting**: Suggestions to avoid overloaded roads

### Indian Traffic Scenarios
- Support for major Indian cities: Bangalore, Mumbai, Delhi, Hyderabad, Pune
- Multiple intersections per city with realistic lane configurations
- Mixed-traffic simulation (characteristic of Indian roads)
- Vehicle types: Cars, Buses, Two-wheelers, Trucks, Autos, Ambulances, Fire Engines, Police

## 🏗️ Architecture

### Backend (Python FastAPI)
- **API Server**: RESTful API for all operations
- **Simulation Engine**: Vehicle movement and traffic dynamics
- **Signal Optimizer**: AI-driven signal control using scipy optimization
- **Emergency Detection**: Instant green corridor creation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Real-time Cache**: Redis for state management

### Frontend (React TypeScript)
- **City Dashboard**: Browse and select cities/intersections
- **Simulation Viewer**: Real-time traffic visualization
- **Vehicle Injector**: UI for adding vehicles to simulation
- **Live Dashboard**: Metrics, congestion levels, throughput
- **Responsive Design**: Works on desktop and tablet devices

### Database Models
- **Cities**: Indian city locations
- **Intersections**: Detailed intersection data
- **Lanes**: Lane configuration per intersection
- **Signals**: Traffic signal state and timing
- **Vehicles**: Individual vehicle data and movement
- **SimulationState**: Metrics and performance data

## 📋 Prerequisites

- Docker & Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+
  - Redis 7+

## 🚀 Quick Start with Docker

```bash
# Clone the repository
git clone <repo-url>
cd copy-of-code

# Start all services
docker-compose up --build

# Frontend will be available at http://localhost:5173
# Backend API at http://localhost:8000
# API Documentation at http://localhost:8000/docs
```

## 🛠️ Development Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database configuration

# Initialize database
python -c "from app.database import init_db; init_db()"

# Seed database with sample cities
python seed_db.py

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# App will be available at http://localhost:5173
```

## 📚 API Documentation

### Available Endpoints

#### Cities
- `GET /api/cities` - Get all cities
- `GET /api/cities/{city_id}` - Get city details
- `POST /api/cities` - Create new city
- `PUT /api/cities/{city_id}` - Update city
- `DELETE /api/cities/{city_id}` - Delete city

#### Intersections
- `GET /api/intersections` - Get intersections
- `GET /api/intersections/{intersection_id}` - Get intersection details
- `POST /api/intersections` - Create intersection
- `PUT /api/intersections/{intersection_id}` - Update intersection
- `DELETE /api/intersections/{intersection_id}` - Delete intersection

#### Vehicles
- `POST /api/vehicles/inject` - Inject vehicle into simulation
- `GET /api/vehicles` - Get all vehicles
- `GET /api/vehicles/{vehicle_id}` - Get vehicle details

#### Simulation
- `POST /api/simulation/start` - Start simulation
- `POST /api/simulation/stop/{intersection_id}` - Stop simulation
- `POST /api/simulation/optimize/{intersection_id}` - Optimize signals
- `GET /api/simulation/metrics/{intersection_id}` - Get metrics
- `POST /api/simulation/step/{intersection_id}` - Step simulation

### Interactive API Documentation
Visit `http://localhost:8000/docs` for interactive Swagger documentation

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/traffic_management
REDIS_URL=redis://localhost:6379/0
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🚗 Vehicle Types & Properties

| Type | Max Speed | Acceleration | Length | Weight |
|------|-----------|--------------|--------|--------|
| Car | 15 m/s | 2.0 m/s² | 4.5m | 1000kg |
| Bus | 12 m/s | 1.5 m/s² | 10m | 5000kg |
| Truck | 12 m/s | 1.2 m/s² | 8m | 8000kg |
| Two-Wheeler | 20 m/s | 3.0 m/s² | 2m | 200kg |
| Auto | 14 m/s | 2.5 m/s² | 3.5m | 600kg |
| Ambulance | 25 m/s | 4.0 m/s² | 5m | 2000kg |
| Fire Engine | 22 m/s | 3.5 m/s² | 7m | 5000kg |
| Police | 25 m/s | 4.0 m/s² | 5m | 1500kg |

## 🧠 Signal Optimization Algorithm

The system uses a weighted congestion model:

1. **Vehicle Weighting**: Different vehicle types have different congestion weights
   - Two-wheeler: 0.4× (lighter)
   - Car: 1.0× (baseline)
   - Auto: 0.8× (lighter)
   - Bus: 2.5× (heavier)
   - Truck: 3.0× (heaviest)

2. **Congestion Calculation**:
   ```
   Congestion = (Weighted Vehicle Count / Lane Capacity) × 100
   ```

3. **Signal Timing Optimization**:
   - Allocates green time proportionally to lane congestion
   - Respects min/max duration constraints
   - Updates every 10 seconds during simulation

4. **Emergency Detection**:
   - Automatically detects emergency vehicles
   - Creates instant green corridor
   - Other signals transition to red

## 📊 Key Metrics

- **Congestion Score**: 0-100 indicating traffic density
- **Average Waiting Time**: Per vehicle in seconds
- **Throughput**: Vehicles exiting per minute
- **Total Vehicles**: Active vehicles in intersection
- **Vehicles Exited**: Successfully passed through intersection

## 🎯 Usage Example

1. **Start the Application**
   ```bash
   docker-compose up
   ```

2. **Browse Cities**
   - Navigate to http://localhost:5173
   - Select a city (e.g., Bangalore)
   - Choose an intersection

3. **Run Simulation**
   - Click "Start Simulation"
   - Use Vehicle Injector to add traffic
   - Monitor live metrics on the dashboard

4. **Optimize Traffic**
   - Click "Optimize Signals" to run AI optimization
   - Observe signal timing adjustments
   - Check congestion levels

5. **Test Emergency Scenarios**
   - Inject emergency vehicles (ambulance, police)
   - Observe automatic green corridor creation
   - Monitor rerouting suggestions

## 📁 Project Structure

```
copy-of-code/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── api/             # API routes
│   │   ├── services/        # Business logic
│   │   ├── simulation/      # Traffic simulation engine
│   │   ├── optimization/    # Signal optimization
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # DB setup
│   │   └── redis_client.py  # Redis setup
│   ├── main.py              # FastAPI app entry
│   ├── seed_db.py           # Database seeding
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── utils/           # API client
│   │   ├── types/           # TypeScript types
│   │   ├── styles/          # Global styles
│   │   ├── App.tsx          # Main app
│   │   └── main.tsx         # Entry point
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite configuration
├── docker-compose.yml       # Docker services
├── Dockerfile.backend       # Backend image
└── Dockerfile.frontend      # Frontend image
```

## 🔮 Future Enhancements

- Real-time WebSocket updates for live traffic
- Machine learning models for traffic prediction
- GPS integration for real vehicle tracking
- Multi-intersection coordination
- Advanced vehicle routing algorithms
- 3D visualization of traffic flow
- Mobile app for iOS/Android

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 📧 Support

For issues or questions, please open an GitHub issue or contact the development team.

---

**Built with ❤️ for Smart Cities in India**
