"""
Mining Models
CSIR EOI 8119 - Mining Data Analytics API
Demonstrates SQL database design for mining industry
"""

from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date,
    ForeignKey, Text, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class ShiftType(str, enum.Enum):
    """Mining shift types."""
    DAY = "day"
    NIGHT = "night"
    MORNING = "morning"
    AFTERNOON = "afternoon"


class EquipmentStatus(str, enum.Enum):
    """Equipment operational status."""
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    REPAIR = "repair"
    DECOMMISSIONED = "decommissioned"


class MaintenanceType(str, enum.Enum):
    """Types of maintenance."""
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    EMERGENCY = "emergency"
    SCHEDULED = "scheduled"


class MiningShift(Base):
    """Mining shift records."""
    
    __tablename__ = "mining_shifts"
    
    id = Column(Integer, primary_key=True, index=True)
    shift_date = Column(Date, nullable=False, index=True)
    shift_type = Column(SQLEnum(ShiftType), nullable=False)
    mine_section = Column(String(100), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    workers_count = Column(Integer, default=0)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supervisor = relationship("User", back_populates="shifts")
    production_records = relationship("ProductionRecord", back_populates="shift")
    
    def __repr__(self):
        return f"<MiningShift {self.shift_date} - {self.shift_type}>"


class ProductionRecord(Base):
    """Mining production records - ore extraction data."""
    
    __tablename__ = "production_records"
    
    id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("mining_shifts.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)
    
    # Production metrics
    ore_extracted_tonnes = Column(Float, default=0.0)
    waste_removed_tonnes = Column(Float, default=0.0)
    ore_grade_percentage = Column(Float, default=0.0)
    depth_meters = Column(Float, default=0.0)
    
    # Location
    mining_level = Column(String(50), nullable=True)
    stope_number = Column(String(50), nullable=True)
    
    # Quality metrics
    contamination_level = Column(Float, default=0.0)
    moisture_content = Column(Float, default=0.0)
    
    # Timestamps
    recorded_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shift = relationship("MiningShift", back_populates="production_records")
    equipment = relationship("Equipment", back_populates="production_records")
    
    def __repr__(self):
        return f"<ProductionRecord {self.id} - {self.ore_extracted_tonnes}t>"


class Equipment(Base):
    """Mining equipment registry."""
    
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    equipment_type = Column(String(100), nullable=False)  # excavator, truck, drill, etc.
    manufacturer = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    year_manufactured = Column(Integer, nullable=True)
    
    # Operational data
    status = Column(SQLEnum(EquipmentStatus), default=EquipmentStatus.OPERATIONAL)
    capacity_tonnes = Column(Float, nullable=True)
    fuel_type = Column(String(50), nullable=True)
    operating_hours = Column(Float, default=0.0)
    
    # Location
    current_location = Column(String(100), nullable=True)
    assigned_section = Column(String(100), nullable=True)
    
    # Timestamps
    commissioned_date = Column(Date, nullable=True)
    last_maintenance_date = Column(Date, nullable=True)
    next_maintenance_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    production_records = relationship("ProductionRecord", back_populates="equipment")
    maintenance_logs = relationship("MaintenanceLog", back_populates="equipment")
    
    def __repr__(self):
        return f"<Equipment {self.equipment_code} - {self.name}>"


class MaintenanceLog(Base):
    """Equipment maintenance records."""
    
    __tablename__ = "maintenance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    
    # Maintenance details
    maintenance_type = Column(SQLEnum(MaintenanceType), nullable=False)
    description = Column(Text, nullable=False)
    technician_name = Column(String(200), nullable=True)
    
    # Costs and duration
    labor_hours = Column(Float, default=0.0)
    parts_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Parts replaced
    parts_replaced = Column(Text, nullable=True)
    
    # Status
    is_completed = Column(Boolean, default=False)
    scheduled_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_logs")
    
    def __repr__(self):
        return f"<MaintenanceLog {self.id} - {self.maintenance_type}>"
