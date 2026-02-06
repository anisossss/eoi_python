"""
Mining Schemas
CSIR EOI 8119 - Mining Data Analytics API
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.mining import ShiftType, EquipmentStatus, MaintenanceType


# ===================== Mining Shift Schemas =====================

class MiningShiftBase(BaseModel):
    """Base mining shift schema."""
    shift_date: date
    shift_type: ShiftType
    mine_section: str = Field(..., min_length=1, max_length=100)
    workers_count: int = Field(default=0, ge=0)
    notes: Optional[str] = None


class MiningShiftCreate(MiningShiftBase):
    """Schema for creating a mining shift."""
    supervisor_id: Optional[int] = None
    start_time: datetime


class MiningShiftUpdate(BaseModel):
    """Schema for updating a mining shift."""
    shift_type: Optional[ShiftType] = None
    mine_section: Optional[str] = Field(None, min_length=1, max_length=100)
    workers_count: Optional[int] = Field(None, ge=0)
    end_time: Optional[datetime] = None
    notes: Optional[str] = None


class MiningShiftResponse(MiningShiftBase):
    """Schema for mining shift response."""
    id: int
    supervisor_id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===================== Production Record Schemas =====================

class ProductionRecordBase(BaseModel):
    """Base production record schema."""
    ore_extracted_tonnes: float = Field(default=0.0, ge=0)
    waste_removed_tonnes: float = Field(default=0.0, ge=0)
    ore_grade_percentage: float = Field(default=0.0, ge=0, le=100)
    depth_meters: float = Field(default=0.0, ge=0)
    mining_level: Optional[str] = None
    stope_number: Optional[str] = None
    contamination_level: float = Field(default=0.0, ge=0, le=100)
    moisture_content: float = Field(default=0.0, ge=0, le=100)


class ProductionRecordCreate(ProductionRecordBase):
    """Schema for creating a production record."""
    shift_id: int
    equipment_id: Optional[int] = None


class ProductionRecordUpdate(BaseModel):
    """Schema for updating a production record."""
    ore_extracted_tonnes: Optional[float] = Field(None, ge=0)
    waste_removed_tonnes: Optional[float] = Field(None, ge=0)
    ore_grade_percentage: Optional[float] = Field(None, ge=0, le=100)
    depth_meters: Optional[float] = Field(None, ge=0)
    mining_level: Optional[str] = None
    stope_number: Optional[str] = None


class ProductionRecordResponse(ProductionRecordBase):
    """Schema for production record response."""
    id: int
    shift_id: int
    equipment_id: Optional[int]
    recorded_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===================== Equipment Schemas =====================

class EquipmentBase(BaseModel):
    """Base equipment schema."""
    equipment_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    equipment_type: str = Field(..., min_length=1, max_length=100)
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year_manufactured: Optional[int] = Field(None, ge=1900, le=2100)


class EquipmentCreate(EquipmentBase):
    """Schema for creating equipment."""
    status: EquipmentStatus = EquipmentStatus.OPERATIONAL
    capacity_tonnes: Optional[float] = Field(None, ge=0)
    fuel_type: Optional[str] = None
    current_location: Optional[str] = None
    assigned_section: Optional[str] = None
    commissioned_date: Optional[date] = None


class EquipmentUpdate(BaseModel):
    """Schema for updating equipment."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[EquipmentStatus] = None
    current_location: Optional[str] = None
    assigned_section: Optional[str] = None
    operating_hours: Optional[float] = Field(None, ge=0)
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None


class EquipmentResponse(EquipmentBase):
    """Schema for equipment response."""
    id: int
    status: EquipmentStatus
    capacity_tonnes: Optional[float]
    fuel_type: Optional[str]
    operating_hours: float
    current_location: Optional[str]
    assigned_section: Optional[str]
    commissioned_date: Optional[date]
    last_maintenance_date: Optional[date]
    next_maintenance_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===================== Maintenance Log Schemas =====================

class MaintenanceLogBase(BaseModel):
    """Base maintenance log schema."""
    maintenance_type: MaintenanceType
    description: str = Field(..., min_length=1)
    technician_name: Optional[str] = None


class MaintenanceLogCreate(MaintenanceLogBase):
    """Schema for creating a maintenance log."""
    equipment_id: int
    labor_hours: float = Field(default=0.0, ge=0)
    parts_cost: float = Field(default=0.0, ge=0)
    total_cost: float = Field(default=0.0, ge=0)
    parts_replaced: Optional[str] = None
    scheduled_date: Optional[date] = None


class MaintenanceLogUpdate(BaseModel):
    """Schema for updating a maintenance log."""
    description: Optional[str] = None
    technician_name: Optional[str] = None
    labor_hours: Optional[float] = Field(None, ge=0)
    parts_cost: Optional[float] = Field(None, ge=0)
    total_cost: Optional[float] = Field(None, ge=0)
    parts_replaced: Optional[str] = None
    is_completed: Optional[bool] = None
    completed_date: Optional[date] = None


class MaintenanceLogResponse(MaintenanceLogBase):
    """Schema for maintenance log response."""
    id: int
    equipment_id: int
    labor_hours: float
    parts_cost: float
    total_cost: float
    parts_replaced: Optional[str]
    is_completed: bool
    scheduled_date: Optional[date]
    completed_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===================== Analytics Schemas =====================

class ProductionStats(BaseModel):
    """Production statistics schema."""
    total_ore_extracted: float
    total_waste_removed: float
    average_ore_grade: float
    total_shifts: int
    average_workers_per_shift: float
    period_start: date
    period_end: date


class DailyProduction(BaseModel):
    """Daily production summary schema."""
    date: date
    total_ore: float
    total_waste: float
    shift_count: int
    equipment_used: int
