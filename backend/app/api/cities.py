"""City routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate, CityResponse

router = APIRouter(prefix="/api/cities", tags=["cities"])


@router.get("", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    """Get all cities"""
    cities = db.query(City).all()
    return cities


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """Get city by ID"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city


@router.post("", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    """Create a new city"""
    # Check if city already exists
    existing = db.query(City).filter(City.name == city.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="City with this name already exists"
        )
    
    new_city = City(**city.model_dump())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.put("/{city_id}", response_model=CityResponse)
def update_city(city_id: int, city_update: CityUpdate, db: Session = Depends(get_db)):
    """Update city"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(city, field, value)
    
    db.commit()
    db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete city"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    db.delete(city)
    db.commit()
