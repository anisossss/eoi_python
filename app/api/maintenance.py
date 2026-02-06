"""
Maintenance API Routes
CSIR EOI 8119 - Mining Data Analytics API
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.mining import (
    MaintenanceLogCreate, MaintenanceLogUpdate, MaintenanceLogResponse
)
from app.services.mining import MiningService

router = APIRouter()


@router.post("/", response_model=MaintenanceLogResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_log(
    log: MaintenanceLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new maintenance log entry."""
    # Verify equipment exists
    equipment = MiningService.get_equipment(db=db, equipment_id=log.equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid equipment_id"
        )
    
    return MiningService.create_maintenance_log(db=db, log=log)


@router.get("/", response_model=List[MaintenanceLogResponse])
def get_maintenance_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    equipment_id: Optional[int] = None,
    is_completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get maintenance logs with optional filtering."""
    return MiningService.get_maintenance_logs(
        db=db,
        skip=skip,
        limit=limit,
        equipment_id=equipment_id,
        is_completed=is_completed
    )


@router.put("/{log_id}", response_model=MaintenanceLogResponse)
def update_maintenance_log(
    log_id: int,
    log: MaintenanceLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a maintenance log entry."""
    updated = MiningService.update_maintenance_log(db=db, log_id=log_id, log=log)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance log not found"
        )
    return updated
