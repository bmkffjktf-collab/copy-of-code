"""
Example: How to use the Traffic Management Platform API

This script demonstrates the main workflows:
1. Creating cities and intersections
2. Starting simulations
3. Injecting vehicles
4. Monitoring metrics
5. Optimizing signals
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000/api"

class TrafficAPIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json() if response.text else {}
    
    # Cities
    def get_cities(self) -> list:
        return self._request("GET", "/cities")
    
    # Intersections
    def get_intersections(self, city_id: int = None) -> list:
        endpoint = "/intersections"
        if city_id:
            endpoint += f"?city_id={city_id}"
        return self._request("GET", endpoint)
    
    # Vehicles
    def inject_vehicle(self, intersection_id: int, lane_id: int, vehicle_type: str, is_emergency: bool = False) -> Dict:
        data = {
            "vehicle_type": vehicle_type,
            "intersection_id": intersection_id,
            "lane_id": lane_id,
            "is_emergency": is_emergency,
        }
        return self._request("POST", "/vehicles/inject", data)
    
    def get_vehicles(self, intersection_id: int) -> list:
        return self._request("GET", f"/vehicles?intersection_id={intersection_id}")
    
    # Simulation
    def start_simulation(self, intersection_id: int, duration: int = 300) -> Dict:
        data = {
            "intersection_id": intersection_id,
            "duration": duration,
            "speed_factor": 1.0,
        }
        return self._request("POST", "/simulation/start", data)
    
    def stop_simulation(self, intersection_id: int) -> Dict:
        return self._request("POST", f"/simulation/stop/{intersection_id}")
    
    def optimize_signals(self, intersection_id: int) -> Dict:
        return self._request("POST", f"/simulation/optimize/{intersection_id}")
    
    def get_metrics(self, intersection_id: int) -> Dict:
        return self._request("GET", f"/simulation/metrics/{intersection_id}")


def main():
    """Main example workflow"""
    client = TrafficAPIClient()
    
    print("🚦 Traffic Management Platform - Example Usage")
    print("=" * 50)
    
    try:
        # Step 1: Get cities
        print("\n1️⃣ Getting available cities...")
        cities = client.get_cities()
        if not cities:
            print("❌ No cities available")
            return
        
        print(f"✅ Found {len(cities)} cities:")
        for city in cities:
            print(f"   - {city['name']} ({city['state']})")
        
        # Step 2: Select first city and get intersections
        selected_city = cities[0]
        print(f"\n2️⃣ Getting intersections in {selected_city['name']}...")
        intersections = client.get_intersections(selected_city['id'])
        
        if not intersections:
            print("❌ No intersections available")
            return
        
        print(f"✅ Found {len(intersections)} intersections:")
        for intersection in intersections:
            print(f"   - {intersection['name']} (Lanes: {intersection['num_lanes']})")
        
        # Step 3: Start simulation
        selected_intersection = intersections[0]
        print(f"\n3️⃣ Starting simulation for {selected_intersection['name']}...")
        sim_result = client.start_simulation(selected_intersection['id'], duration=300)
        print(f"✅ Simulation started: {sim_result}")
        
        # Step 4: Inject vehicles
        print(f"\n4️⃣ Injecting vehicles...")
        vehicle_types = ['CAR', 'BUS', 'TWO_WHEELER', 'AMBULANCE']
        
        for i in range(4):
            lane_id = (i % 4) + 1  # Distribute across lanes
            vehicle_type = vehicle_types[i]
            is_emergency = vehicle_type == 'AMBULANCE'
            
            vehicle = client.inject_vehicle(
                intersection_id=selected_intersection['id'],
                lane_id=lane_id,
                vehicle_type=vehicle_type,
                is_emergency=is_emergency
            )
            print(f"   ✅ Injected {vehicle_type}: {vehicle['vehicle_id']}")
        
        # Step 5: Monitor metrics
        print(f"\n5️⃣ Monitoring simulation metrics...")
        time.sleep(2)
        
        metrics = client.get_metrics(selected_intersection['id'])
        print(f"   ✅ Simulation Time: {metrics['simulation_time']:.1f}s")
        print(f"   ✅ Total Vehicles: {metrics['total_vehicles']}")
        print(f"   ✅ Avg Wait Time: {metrics['avg_waiting_time']:.1f}s")
        print(f"   ✅ Congestion Level: {metrics['congestion_score']:.1f}%")
        
        # Step 6: Optimize signals
        print(f"\n6️⃣ Optimizing signal timings...")
        opt_result = client.optimize_signals(selected_intersection['id'])
        print(f"✅ Signals optimized: {opt_result}")
        
        # Step 7: Get updated metrics
        print(f"\n7️⃣ Checking updated metrics...")
        time.sleep(2)
        
        metrics = client.get_metrics(selected_intersection['id'])
        print(f"   ✅ Updated Congestion Level: {metrics['congestion_score']:.1f}%")
        print(f"   ✅ Vehicles Exited: {metrics['vehicles_exited']}")
        print(f"   ✅ Throughput: {metrics['vehicles_per_minute']:.1f} vehicles/min")
        
        # Step 8: Stop simulation
        print(f"\n8️⃣ Stopping simulation...")
        stop_result = client.stop_simulation(selected_intersection['id'])
        print(f"✅ Simulation stopped: {stop_result}")
        
        print("\n" + "=" * 50)
        print("✅ Example completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Is the backend running?")
        print("   Start with: docker-compose up")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
