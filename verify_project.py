#!/usr/bin/env python3
"""
Quick start verification script - checks if project structure is complete
"""

import os
import sys
from pathlib import Path

def check_file_exists(path: str, description: str) -> bool:
    """Check if file exists and print status"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory_exists(path: str, description: str) -> bool:
    """Check if directory exists"""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("🔍 Traffic Management Platform - Project Verification")
    print("=" * 60)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    all_checks = []
    
    # Backend files
    print("\n📦 Backend Python Files:")
    backend_files = [
        ("backend/main.py", "Main application"),
        ("backend/seed_db.py", "Database seeding"),
        ("backend/init_db.py", "DB initialization"),
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/.env.example", "Environment template"),
        ("backend/app/__init__.py", "App package"),
        ("backend/app/config.py", "Configuration"),
        ("backend/app/database.py", "Database setup"),
        ("backend/app/redis_client.py", "Redis client"),
    ]
    
    for file, desc in backend_files:
        all_checks.append(check_file_exists(os.path.join(base_path, file), desc))
    
    # Backend modules
    print("\n📁 Backend Modules:")
    backend_dirs = [
        ("backend/app/models", "Database models"),
        ("backend/app/schemas", "Pydantic schemas"),
        ("backend/app/api", "API routes"),
        ("backend/app/simulation", "Traffic simulation"),
        ("backend/app/optimization", "Signal optimization"),
        ("backend/tests", "Tests"),
    ]
    
    for dir, desc in backend_dirs:
        all_checks.append(check_directory_exists(os.path.join(base_path, dir), desc))
    
    # Backend model files
    print("\n🗄️ Backend Models:")
    models = [
        "backend/app/models/base.py",
        "backend/app/models/city.py",
        "backend/app/models/intersection.py",
        "backend/app/models/lane.py",
        "backend/app/models/signal.py",
        "backend/app/models/vehicle.py",
        "backend/app/models/simulation_state.py",
    ]
    
    for model in models:
        all_checks.append(check_file_exists(os.path.join(base_path, model), f"Model: {model.split('/')[-1]}"))
    
    # Backend API files
    print("\n🔌 Backend API Routes:")
    apis = [
        "backend/app/api/cities.py",
        "backend/app/api/intersections.py",
        "backend/app/api/vehicles.py",
        "backend/app/api/simulation.py",
    ]
    
    for api in apis:
        all_checks.append(check_file_exists(os.path.join(base_path, api), f"Route: {api.split('/')[-1]}"))
    
    # Backend services
    print("\n⚙️ Backend Services:")
    services = [
        "backend/app/simulation/vehicle_simulation.py",
        "backend/app/optimization/signal_optimizer.py",
    ]
    
    for service in services:
        all_checks.append(check_file_exists(os.path.join(base_path, service), f"Service: {service.split('/')[-1]}"))
    
    # Frontend files
    print("\n🎨 Frontend Files:")
    frontend_files = [
        ("frontend/package.json", "NPM configuration"),
        ("frontend/tsconfig.json", "TypeScript config"),
        ("frontend/vite.config.ts", "Vite config"),
        ("frontend/index.html", "HTML entry point"),
        ("frontend/src/main.tsx", "React entry point"),
        ("frontend/src/App.tsx", "Main app component"),
    ]
    
    for file, desc in frontend_files:
        all_checks.append(check_file_exists(os.path.join(base_path, file), desc))
    
    # Frontend components
    print("\n💻 Frontend Components:")
    components = [
        "frontend/src/components/Header.tsx",
        "frontend/src/components/TrafficMap.tsx",
        "frontend/src/components/VehicleInjector.tsx",
        "frontend/src/components/LiveDashboard.tsx",
        "frontend/src/pages/Dashboard.tsx",
        "frontend/src/pages/SimulationPage.tsx",
        "frontend/src/utils/api.ts",
        "frontend/src/types/index.ts",
    ]
    
    for comp in components:
        all_checks.append(check_file_exists(os.path.join(base_path, comp), f"Component: {comp.split('/')[-1]}"))
    
    # Docker files
    print("\n🐳 Docker Files:")
    docker_files = [
        ("docker-compose.yml", "Docker Compose"),
        ("Dockerfile.backend", "Backend container"),
        ("Dockerfile.frontend", "Frontend container"),
    ]
    
    for file, desc in docker_files:
        all_checks.append(check_file_exists(os.path.join(base_path, file), desc))
    
    # Documentation
    print("\n📚 Documentation:")
    docs = [
        ("README.md", "Main documentation"),
        ("DEVELOPMENT.md", "Development guide"),
        ("PROJECT_SUMMARY.md", "Project summary"),
    ]
    
    for file, desc in docs:
        all_checks.append(check_file_exists(os.path.join(base_path, file), desc))
    
    # Scripts
    print("\n🔧 Setup Scripts:")
    scripts = [
        ("setup.sh", "Full setup"),
        ("setup-backend.sh", "Backend setup"),
        ("setup-frontend.sh", "Frontend setup"),
        ("example_usage.py", "Example usage"),
    ]
    
    for file, desc in scripts:
        all_checks.append(check_file_exists(os.path.join(base_path, file), desc))
    
    # Summary
    print("\n" + "=" * 60)
    total = len(all_checks)
    passed = sum(all_checks)
    failed = total - passed
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if failed == 0:
        print("\n✅ All project files are in place!")
        print("\n🚀 You can now:")
        print("   1. Run: docker-compose up --build")
        print("   2. Visit: http://localhost:5173 (Frontend)")
        print("   3. Visit: http://localhost:8000/docs (API Docs)")
        return 0
    else:
        print(f"\n⚠️ {failed} files are missing")
        return 1

if __name__ == "__main__":
    sys.exit(main())
