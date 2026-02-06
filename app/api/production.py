"""
Production Records API Routes
CSIR EOI 8119 - Mining Data Analytics API
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.mining import (
    ProductionRecordCreate, ProductionRecordUpdate, ProductionRecordResponse
)
from app.services.mining import MiningService

router = APIRouter()


@router.post("/", response_model=ProductionRecordResponse, status_code=status.HTTP_201_CREATED)
def create_production_record(
    record: ProductionRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new production record."""
    # Verify shift exists
    shift = MiningService.get_shift(db=db, shift_id=record.shift_id)
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid shift_id"
        )
    
    # Verify equipment exists if provided
    if record.equipment_id:
        equipment = MiningService.get_equipment(db=db, equipment_id=record.equipment_id)
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid equipment_id"
            )
    
    return MiningService.create_production_record(db=db, record=record)


@router.get("/", response_model=List[ProductionRecordResponse])
def get_production_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    shift_id: Optional[int] = None,
    equipment_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get production records with optional filtering."""
    return MiningService.get_production_records(
        db=db,
        skip=skip,
        limit=limit,
        shift_id=shift_id,
        equipment_id=equipment_id
    )


@router.get("/{record_id}", response_model=ProductionRecordResponse)
def get_production_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific production record by ID."""
    record = MiningService.get_production_record(db=db, record_id=record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production record not found"
        )
    return record


@router.put("/{record_id}", response_model=ProductionRecordResponse)
def update_production_record(
    record_id: int,
    record: ProductionRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a production record."""
    updated_record = MiningService.update_production_record(
        db=db, record_id=record_id, record=record
    )
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production record not found"
        )
    return updated_record
