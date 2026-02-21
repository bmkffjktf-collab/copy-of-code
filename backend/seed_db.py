"""Seed database with sample Indian cities and intersections"""
from app.database import SessionLocal, init_db
from app.models.city import City
from app.models.intersection import Intersection
from app.models.lane import Lane, Direction
from app.models.signal import Signal
from sqlalchemy.exc import IntegrityError

# Initialize database tables first
init_db()

db = SessionLocal()

# Sample Indian cities
cities_data = [
    {
        "name": "Bangalore",
        "state": "Karnataka",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "description": "Silicon Valley of India",
        "population": "12.5 Million"
    },
    {
        "name": "Mumbai",
        "state": "Maharashtra",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "description": "City of Dreams",
        "population": "20 Million"
    },
    {
        "name": "Delhi",
        "state": "Delhi",
        "latitude": 28.7041,
        "longitude": 77.1025,
        "description": "National Capital",
        "population": "16 Million"
    },
    {
        "name": "Hyderabad",
        "state": "Telangana",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "description": "City of Pearls",
        "population": "9.7 Million"
    },
    {
        "name": "Pune",
        "state": "Maharashtra",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "description": "Oxford of the East",
        "population": "6.4 Million"
    },
]

# Create cities
created_cities = []
for city_data in cities_data:
    try:
        city = City(**city_data)
        db.add(city)
        db.commit()
        created_cities.append(city)
        print(f"Created city: {city.name}")
    except IntegrityError:
        db.rollback()
        print(f"City {city_data['name']} already exists")

# Sample intersections for each city
intersections_data = {
    "Bangalore": [
        {"name": "MG Road - Brigade Road", "latitude": 12.9352, "longitude": 77.6245},
        {"name": "Koramangala - Mysore Road", "latitude": 12.9352, "longitude": 77.6245},
    ],
    "Mumbai": [
        {"name": "VT - Bandra", "latitude": 19.0176, "longitude": 72.8479},
        {"name": "Churchgate - CST", "latitude": 18.9352, "longitude": 72.8235},
    ],
    "Delhi": [
        {"name": "India Gate - New Delhi", "latitude": 28.6129, "longitude": 77.2295},
        {"name": "Connaught Place - CP", "latitude": 28.6328, "longitude": 77.1892},
    ],
    "Hyderabad": [
        {"name": "Hitech City - Madhapur", "latitude": 17.5560, "longitude": 78.3560},
        {"name": "Charminar - Old City", "latitude": 17.3606, "longitude": 78.4747},
    ],
    "Pune": [
        {"name": "Camp - Shivaji Nagar", "latitude": 18.5333, "longitude": 73.8667},
        {"name": "Koregaon Park - Yerwada", "latitude": 18.5352, "longitude": 73.9235},
    ],
}

# Create intersections and lanes
for city in created_cities:
    city_name = city.name
    if city_name in intersections_data:
        for idx, inter_data in enumerate(intersections_data[city_name]):
            intersection = Intersection(
                name=inter_data["name"],
                city_id=city.id,
                latitude=inter_data["latitude"],
                longitude=inter_data["longitude"],
                num_lanes=4
            )
            db.add(intersection)
            db.commit()
            print(f"Created intersection: {intersection.name}")
            
            # Create lanes for intersection
            directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
            for direction in directions:
                lane = Lane(
                    name=f"Lane {direction.value}",
                    intersection_id=intersection.id,
                    direction=direction,
                    capacity=30,
                    length=100.0,
                    width=3.5
                )
                db.add(lane)
            
            db.commit()
            
            # Create signals for intersection
            signals_data = [
                {"name": "Signal NS", "state": "RED"},
                {"name": "Signal EW", "state": "GREEN"},
            ]
            
            for sig_data in signals_data:
                signal = Signal(
                    name=sig_data["name"],
                    intersection_id=intersection.id,
                    green_duration=20,
                    yellow_duration=3,
                    red_duration=20,
                )
                db.add(signal)
            
            db.commit()
            print(f"Created 4 lanes and 2 signals for {intersection.name}")

print("Database seeding completed!")
