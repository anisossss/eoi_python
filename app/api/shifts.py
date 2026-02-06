"""
Mining Shifts API Routes
CSIR EOI 8119 - Mining Data Analytics API
"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.mining import MiningShiftCreate, MiningShiftUpdate, MiningShiftResponse
from app.services.mining import MiningService

router = APIRouter()


@router.post("/", response_model=MiningShiftResponse, status_code=status.HTTP_201_CREATED)
def create_shift(
    shift: MiningShiftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new mining shift."""
    return MiningService.create_shift(db=db, shift=shift)


@router.get("/", response_model=List[MiningShiftResponse])
def get_shifts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    mine_section: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get mining shifts with optional filtering."""
    return MiningService.get_shifts(
        db=db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        mine_section=mine_section
    )


@router.get("/{shift_id}", response_model=MiningShiftResponse)
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific mining shift by ID."""
    shift = MiningService.get_shift(db=db, shift_id=shift_id)
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found"
        )
    return shift


@router.put("/{shift_id}", response_model=MiningShiftResponse)
def update_shift(
    shift_id: int,
    shift: MiningShiftUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a mining shift."""
    updated_shift = MiningService.update_shift(db=db, shift_id=shift_id, shift=shift)
    if not updated_shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found"
        )
    return updated_shift


@router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a mining shift."""
    if not MiningService.delete_shift(db=db, shift_id=shift_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found"
        )
