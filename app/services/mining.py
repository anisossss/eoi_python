"""
Mining Service
CSIR EOI 8119 - Mining Data Analytics API
Demonstrates proficiency with SQL queries and relational database operations
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session

from app.models.mining import (
    MiningShift, ProductionRecord, Equipment, MaintenanceLog,
    ShiftType, EquipmentStatus
)
from app.schemas.mining import (
    MiningShiftCreate, MiningShiftUpdate,
    ProductionRecordCreate, ProductionRecordUpdate,
    EquipmentCreate, EquipmentUpdate,
    MaintenanceLogCreate, MaintenanceLogUpdate,
    ProductionStats, DailyProduction
)


class MiningService:
    """Service class for mining operations - demonstrates SQL proficiency."""
    
    # ==================== Mining Shift Operations ====================
    
    @staticmethod
    def create_shift(db: Session, shift: MiningShiftCreate) -> MiningShift:
        """Create a new mining shift."""
        db_shift = MiningShift(**shift.model_dump())
        db.add(db_shift)
        db.commit()
        db.refresh(db_shift)
        return db_shift
    
    @staticmethod
    def get_shift(db: Session, shift_id: int) -> Optional[MiningShift]:
        """Get a mining shift by ID."""
        return db.query(MiningShift).filter(MiningShift.id == shift_id).first()
    
    @staticmethod
    def get_shifts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        mine_section: Optional[str] = None
    ) -> List[MiningShift]:
        """Get mining shifts with filtering - demonstrates SQL WHERE clauses."""
        query = db.query(MiningShift)
        
        if start_date:
            query = query.filter(MiningShift.shift_date >= start_date)
        if end_date:
            query = query.filter(MiningShift.shift_date <= end_date)
        if mine_section:
            query = query.filter(MiningShift.mine_section == mine_section)
        
        return query.order_by(desc(MiningShift.shift_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_shift(db: Session, shift_id: int, shift: MiningShiftUpdate) -> Optional[MiningShift]:
        """Update a mining shift."""
        db_shift = db.query(MiningShift).filter(MiningShift.id == shift_id).first()
        if db_shift:
            update_data = shift.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_shift, key, value)
            db.commit()
            db.refresh(db_shift)
        return db_shift
    
    @staticmethod
    def delete_shift(db: Session, shift_id: int) -> bool:
        """Delete a mining shift."""
        db_shift = db.query(MiningShift).filter(MiningShift.id == shift_id).first()
        if db_shift:
            db.delete(db_shift)
            db.commit()
            return True
        return False
    
    # ==================== Production Record Operations ====================
    
    @staticmethod
    def create_production_record(db: Session, record: ProductionRecordCreate) -> ProductionRecord:
        """Create a new production record."""
        db_record = ProductionRecord(**record.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    
    @staticmethod
    def get_production_record(db: Session, record_id: int) -> Optional[ProductionRecord]:
        """Get a production record by ID."""
        return db.query(ProductionRecord).filter(ProductionRecord.id == record_id).first()
    
    @staticmethod
    def get_production_records(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        shift_id: Optional[int] = None,
        equipment_id: Optional[int] = None
    ) -> List[ProductionRecord]:
        """Get production records with filtering."""
        query = db.query(ProductionRecord)
        
        if shift_id:
            query = query.filter(ProductionRecord.shift_id == shift_id)
        if equipment_id:
            query = query.filter(ProductionRecord.equipment_id == equipment_id)
        
        return query.order_by(desc(ProductionRecord.recorded_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_production_record(
        db: Session, record_id: int, record: ProductionRecordUpdate
    ) -> Optional[ProductionRecord]:
        """Update a production record."""
        db_record = db.query(ProductionRecord).filter(ProductionRecord.id == record_id).first()
        if db_record:
            update_data = record.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_record, key, value)
            db.commit()
            db.refresh(db_record)
        return db_record
    
    # ==================== Equipment Operations ====================
    
    @staticmethod
    def create_equipment(db: Session, equipment: EquipmentCreate) -> Equipment:
        """Create new equipment."""
        db_equipment = Equipment(**equipment.model_dump())
        db.add(db_equipment)
        db.commit()
        db.refresh(db_equipment)
        return db_equipment
    
    @staticmethod
    def get_equipment(db: Session, equipment_id: int) -> Optional[Equipment]:
        """Get equipment by ID."""
        return db.query(Equipment).filter(Equipment.id == equipment_id).first()
    
    @staticmethod
    def get_equipment_by_code(db: Session, equipment_code: str) -> Optional[Equipment]:
        """Get equipment by code."""
        return db.query(Equipment).filter(Equipment.equipment_code == equipment_code).first()
    
    @staticmethod
    def get_all_equipment(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[EquipmentStatus] = None,
        equipment_type: Optional[str] = None
    ) -> List[Equipment]:
        """Get all equipment with filtering."""
        query = db.query(Equipment)
        
        if status:
            query = query.filter(Equipment.status == status)
        if equipment_type:
            query = query.filter(Equipment.equipment_type == equipment_type)
        
        return query.order_by(Equipment.equipment_code).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_equipment(
        db: Session, equipment_id: int, equipment: EquipmentUpdate
    ) -> Optional[Equipment]:
        """Update equipment."""
        db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if db_equipment:
            update_data = equipment.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_equipment, key, value)
            db.commit()
            db.refresh(db_equipment)
        return db_equipment
    
    # ==================== Maintenance Log Operations ====================
    
    @staticmethod
    def create_maintenance_log(db: Session, log: MaintenanceLogCreate) -> MaintenanceLog:
        """Create a new maintenance log."""
        db_log = MaintenanceLog(**log.model_dump())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def get_maintenance_logs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        equipment_id: Optional[int] = None,
        is_completed: Optional[bool] = None
    ) -> List[MaintenanceLog]:
        """Get maintenance logs with filtering."""
        query = db.query(MaintenanceLog)
        
        if equipment_id:
            query = query.filter(MaintenanceLog.equipment_id == equipment_id)
        if is_completed is not None:
            query = query.filter(MaintenanceLog.is_completed == is_completed)
        
        return query.order_by(desc(MaintenanceLog.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_maintenance_log(
        db: Session, log_id: int, log: MaintenanceLogUpdate
    ) -> Optional[MaintenanceLog]:
        """Update a maintenance log."""
        db_log = db.query(MaintenanceLog).filter(MaintenanceLog.id == log_id).first()
        if db_log:
            update_data = log.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_log, key, value)
            db.commit()
            db.refresh(db_log)
        return db_log
    
    # ==================== Analytics Operations (SQL Aggregations) ====================
    
    @staticmethod
    def get_production_stats(
        db: Session,
        start_date: date,
        end_date: date
    ) -> ProductionStats:
        """
        Get production statistics for a date range.
        Demonstrates SQL aggregation functions (SUM, AVG, COUNT).
        """
        # Join shifts with production records for the date range
        result = db.query(
            func.sum(ProductionRecord.ore_extracted_tonnes).label("total_ore"),
            func.sum(ProductionRecord.waste_removed_tonnes).label("total_waste"),
            func.avg(ProductionRecord.ore_grade_percentage).label("avg_grade")
        ).join(
            MiningShift, ProductionRecord.shift_id == MiningShift.id
        ).filter(
            and_(
                MiningShift.shift_date >= start_date,
                MiningShift.shift_date <= end_date
            )
        ).first()
        
        # Get shift statistics
        shift_stats = db.query(
            func.count(MiningShift.id).label("total_shifts"),
            func.avg(MiningShift.workers_count).label("avg_workers")
        ).filter(
            and_(
                MiningShift.shift_date >= start_date,
                MiningShift.shift_date <= end_date
            )
        ).first()
        
        return ProductionStats(
            total_ore_extracted=result.total_ore or 0.0,
            total_waste_removed=result.total_waste or 0.0,
            average_ore_grade=result.avg_grade or 0.0,
            total_shifts=shift_stats.total_shifts or 0,
            average_workers_per_shift=shift_stats.avg_workers or 0.0,
            period_start=start_date,
            period_end=end_date
        )
    
    @staticmethod
    def get_daily_production(
        db: Session,
        start_date: date,
        end_date: date
    ) -> List[DailyProduction]:
        """
        Get daily production summaries.
        Demonstrates SQL GROUP BY with aggregations.
        """
        results = db.query(
            MiningShift.shift_date.label("date"),
            func.sum(ProductionRecord.ore_extracted_tonnes).label("total_ore"),
            func.sum(ProductionRecord.waste_removed_tonnes).label("total_waste"),
            func.count(func.distinct(MiningShift.id)).label("shift_count"),
            func.count(func.distinct(ProductionRecord.equipment_id)).label("equipment_used")
        ).join(
            ProductionRecord, MiningShift.id == ProductionRecord.shift_id
        ).filter(
            and_(
                MiningShift.shift_date >= start_date,
                MiningShift.shift_date <= end_date
            )
        ).group_by(
            MiningShift.shift_date
        ).order_by(
            MiningShift.shift_date
        ).all()
        
        return [
            DailyProduction(
                date=r.date,
                total_ore=r.total_ore or 0.0,
                total_waste=r.total_waste or 0.0,
                shift_count=r.shift_count or 0,
                equipment_used=r.equipment_used or 0
            )
            for r in results
        ]
    
    @staticmethod
    def get_equipment_utilization(db: Session) -> List[Dict[str, Any]]:
        """
        Get equipment utilization statistics.
        Demonstrates complex SQL joins and aggregations.
        """
        results = db.query(
            Equipment.equipment_code,
            Equipment.name,
            Equipment.equipment_type,
            Equipment.status,
            func.count(ProductionRecord.id).label("total_records"),
            func.sum(ProductionRecord.ore_extracted_tonnes).label("total_ore")
        ).outerjoin(
            ProductionRecord, Equipment.id == ProductionRecord.equipment_id
        ).group_by(
            Equipment.id
        ).order_by(
            desc(func.sum(ProductionRecord.ore_extracted_tonnes))
        ).all()
        
        return [
            {
                "equipment_code": r.equipment_code,
                "name": r.name,
                "equipment_type": r.equipment_type,
                "status": r.status.value if r.status else None,
                "total_production_records": r.total_records or 0,
                "total_ore_extracted": r.total_ore or 0.0
            }
            for r in results
        ]
