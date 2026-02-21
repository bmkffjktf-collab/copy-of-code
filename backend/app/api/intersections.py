"""Intersection routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.intersection import Intersection
from app.models.city import City
from app.schemas.intersection import IntersectionCreate, IntersectionUpdate, IntersectionResponse

router = APIRouter(prefix="/api/intersections", tags=["intersections"])


@router.get("", response_model=list[IntersectionResponse])
def get_intersections(city_id: int = None, db: Session = Depends(get_db)):
    """Get all intersections, optionally filtered by city"""
    query = db.query(Intersection)
    if city_id:
        query = query.filter(Intersection.city_id == city_id)
    return query.all()


@router.get("/{intersection_id}", response_model=IntersectionResponse)
def get_intersection(intersection_id: int, db: Session = Depends(get_db)):
    """Get intersection by ID"""
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intersection not found")
    return intersection


@router.post("", response_model=IntersectionResponse, status_code=status.HTTP_201_CREATED)
def create_intersection(intersection: IntersectionCreate, db: Session = Depends(get_db)):
    """Create a new intersection"""
    # Verify city exists
    city = db.query(City).filter(City.id == intersection.city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City not found")
    
    new_intersection = Intersection(**intersection.model_dump())
    db.add(new_intersection)
    db.commit()
    db.refresh(new_intersection)
    return new_intersection


@router.put("/{intersection_id}", response_model=IntersectionResponse)
def update_intersection(
    intersection_id: int, 
    intersection_update: IntersectionUpdate, 
    db: Session = Depends(get_db)
):
    """Update intersection"""
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intersection not found")
    
    update_data = intersection_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(intersection, field, value)
    
    db.commit()
    db.refresh(intersection)
    return intersection


@router.delete("/{intersection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_intersection(intersection_id: int, db: Session = Depends(get_db)):
    """Delete intersection"""
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intersection not found")
    
    db.delete(intersection)
    db.commit()
