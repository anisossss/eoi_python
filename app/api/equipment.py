"""
Equipment API Routes
CSIR EOI 8119 - Mining Data Analytics API
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.mining import EquipmentStatus
from app.schemas.mining import EquipmentCreate, EquipmentUpdate, EquipmentResponse
from app.services.mining import MiningService

router = APIRouter()


@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Register new mining equipment."""
    # Check if equipment code already exists
    existing = MiningService.get_equipment_by_code(db=db, equipment_code=equipment.equipment_code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Equipment code already exists"
        )
    
    return MiningService.create_equipment(db=db, equipment=equipment)


@router.get("/", response_model=List[EquipmentResponse])
def get_all_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[EquipmentStatus] = None,
    equipment_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all equipment with optional filtering."""
    return MiningService.get_all_equipment(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        equipment_type=equipment_type
    )


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific equipment by ID."""
    equipment = MiningService.get_equipment(db=db, equipment_id=equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update equipment information."""
    updated = MiningService.update_equipment(db=db, equipment_id=equipment_id, equipment=equipment)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    return updated
