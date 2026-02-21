"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.config import settings
from app.database import init_db
from app.api import cities, intersections, vehicles, simulation

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Nationwide AI-Powered Traffic Management and Simulation Platform for India",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(cities.router)
app.include_router(intersections.router)
app.include_router(vehicles.router)
app.include_router(simulation.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Traffic Management Platform API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
