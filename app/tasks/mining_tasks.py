"""
Mining Background Tasks
CSIR EOI 8119 - Mining Data Analytics API
Demonstrates Celery background processing capabilities
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, Any, List

from celery import shared_task
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.mining import (
    MiningShift, ProductionRecord, Equipment, MaintenanceLog,
    EquipmentStatus
)

logger = logging.getLogger(__name__)


def get_db_session() -> Session:
    """Get a new database session for background tasks."""
    return SessionLocal()


@shared_task(bind=True, name="app.tasks.mining_tasks.generate_daily_report")
def generate_daily_report(self) -> Dict[str, Any]:
    """
    Generate daily production report.
    
    This task demonstrates:
    - Background report generation
    - SQL aggregation queries
    - Scheduled task execution
    
    Returns:
        Dict containing the daily report data
    """
    logger.info("Starting daily report generation...")
    db = get_db_session()
    
    try:
        yesterday = date.today() - timedelta(days=1)
        
        # Get production statistics for yesterday
        production_stats = db.query(
            func.sum(ProductionRecord.ore_extracted_tonnes).label("total_ore"),
            func.sum(ProductionRecord.waste_removed_tonnes).label("total_waste"),
            func.avg(ProductionRecord.ore_grade_percentage).label("avg_grade"),
            func.count(ProductionRecord.id).label("record_count")
        ).join(
            MiningShift, ProductionRecord.shift_id == MiningShift.id
        ).filter(
            MiningShift.shift_date == yesterday
        ).first()
        
        # Get shift statistics
        shift_stats = db.query(
            func.count(MiningShift.id).label("total_shifts"),
            func.sum(MiningShift.workers_count).label("total_workers")
        ).filter(
            MiningShift.shift_date == yesterday
        ).first()
        
        # Get equipment used
        equipment_count = db.query(
            func.count(func.distinct(ProductionRecord.equipment_id))
        ).join(
            MiningShift, ProductionRecord.shift_id == MiningShift.id
        ).filter(
            MiningShift.shift_date == yesterday
        ).scalar()
        
        report = {
            "report_date": yesterday.isoformat(),
            "generated_at": datetime.utcnow().isoformat(),
            "production": {
                "total_ore_tonnes": production_stats.total_ore or 0,
                "total_waste_tonnes": production_stats.total_waste or 0,
                "average_ore_grade": round(production_stats.avg_grade or 0, 2),
                "production_records": production_stats.record_count or 0
            },
            "operations": {
                "total_shifts": shift_stats.total_shifts or 0,
                "total_workers": shift_stats.total_workers or 0,
                "equipment_used": equipment_count or 0
            },
            "status": "completed"
        }
        
        logger.info(f"Daily report generated: {report}")
        return report
        
    except Exception as e:
        logger.error(f"Error generating daily report: {str(e)}")
        raise
    finally:
        db.close()


@shared_task(bind=True, name="app.tasks.mining_tasks.process_production_data")
def process_production_data(self) -> Dict[str, Any]:
    """
    Process and aggregate production data.
    
    This task demonstrates:
    - Periodic data processing
    - Data aggregation and summarization
    - Background computation
    
    Returns:
        Dict containing processing results
    """
    logger.info("Starting production data processing...")
    db = get_db_session()
    
    try:
        # Get recent production records (last hour)
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        
        recent_records = db.query(ProductionRecord).filter(
            ProductionRecord.created_at >= one_hour_ago
        ).all()
        
        # Calculate totals
        total_ore = sum(r.ore_extracted_tonnes for r in recent_records)
        total_waste = sum(r.waste_removed_tonnes for r in recent_records)
        
        result = {
            "processed_at": datetime.utcnow().isoformat(),
            "records_processed": len(recent_records),
            "total_ore_extracted": total_ore,
            "total_waste_removed": total_waste,
            "status": "completed"
        }
        
        logger.info(f"Production data processed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing production data: {str(e)}")
        raise
    finally:
        db.close()


@shared_task(bind=True, name="app.tasks.mining_tasks.calculate_equipment_metrics")
def calculate_equipment_metrics(self) -> List[Dict[str, Any]]:
    """
    Calculate equipment performance metrics.
    
    This task demonstrates:
    - Complex SQL queries
    - Performance metric calculation
    - Background analytics
    
    Returns:
        List of equipment metrics
    """
    logger.info("Starting equipment metrics calculation...")
    db = get_db_session()
    
    try:
        # Get all equipment with their production totals
        results = db.query(
            Equipment.id,
            Equipment.equipment_code,
            Equipment.name,
            Equipment.status,
            Equipment.operating_hours,
            func.count(ProductionRecord.id).label("total_records"),
            func.sum(ProductionRecord.ore_extracted_tonnes).label("total_ore")
        ).outerjoin(
            ProductionRecord, Equipment.id == ProductionRecord.equipment_id
        ).group_by(
            Equipment.id
        ).all()
        
        metrics = []
        for r in results:
            # Calculate efficiency (ore per operating hour)
            efficiency = 0
            if r.operating_hours and r.operating_hours > 0 and r.total_ore:
                efficiency = round(r.total_ore / r.operating_hours, 2)
            
            metrics.append({
                "equipment_id": r.id,
                "equipment_code": r.equipment_code,
                "name": r.name,
                "status": r.status.value if r.status else None,
                "operating_hours": r.operating_hours or 0,
                "total_production_records": r.total_records or 0,
                "total_ore_extracted": r.total_ore or 0,
                "efficiency_tonnes_per_hour": efficiency
            })
        
        logger.info(f"Equipment metrics calculated for {len(metrics)} equipment")
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating equipment metrics: {str(e)}")
        raise
    finally:
        db.close()


@shared_task(bind=True, name="app.tasks.mining_tasks.send_maintenance_alerts")
def send_maintenance_alerts(self) -> Dict[str, Any]:
    """
    Check for upcoming maintenance and send alerts.
    
    This task demonstrates:
    - Scheduled alerting
    - Date-based filtering
    - Notification system integration point
    
    Returns:
        Dict containing alert summary
    """
    logger.info("Starting maintenance alert check...")
    db = get_db_session()
    
    try:
        today = date.today()
        week_ahead = today + timedelta(days=7)
        
        # Find equipment with upcoming maintenance
        upcoming_maintenance = db.query(Equipment).filter(
            and_(
                Equipment.next_maintenance_date >= today,
                Equipment.next_maintenance_date <= week_ahead,
                Equipment.status == EquipmentStatus.OPERATIONAL
            )
        ).all()
        
        # Find overdue maintenance
        overdue_maintenance = db.query(Equipment).filter(
            and_(
                Equipment.next_maintenance_date < today,
                Equipment.status == EquipmentStatus.OPERATIONAL
            )
        ).all()
        
        # Find pending maintenance logs
        pending_logs = db.query(MaintenanceLog).filter(
            MaintenanceLog.is_completed == False
        ).count()
        
        alerts = {
            "checked_at": datetime.utcnow().isoformat(),
            "upcoming_maintenance": [
                {
                    "equipment_code": e.equipment_code,
                    "name": e.name,
                    "maintenance_date": e.next_maintenance_date.isoformat()
                }
                for e in upcoming_maintenance
            ],
            "overdue_maintenance": [
                {
                    "equipment_code": e.equipment_code,
                    "name": e.name,
                    "overdue_since": e.next_maintenance_date.isoformat()
                }
                for e in overdue_maintenance
            ],
            "pending_maintenance_logs": pending_logs,
            "status": "completed"
        }
        
        logger.info(f"Maintenance alerts: {len(upcoming_maintenance)} upcoming, "
                   f"{len(overdue_maintenance)} overdue")
        return alerts
        
    except Exception as e:
        logger.error(f"Error checking maintenance alerts: {str(e)}")
        raise
    finally:
        db.close()


@shared_task(bind=True, name="app.tasks.mining_tasks.cleanup_old_records")
def cleanup_old_records(self, days_to_keep: int = 365) -> Dict[str, Any]:
    """
    Clean up old records from the database.
    
    This task demonstrates:
    - Scheduled maintenance tasks
    - Data retention policies
    - Batch delete operations
    
    Args:
        days_to_keep: Number of days to retain records
        
    Returns:
        Dict containing cleanup results
    """
    logger.info(f"Starting cleanup of records older than {days_to_keep} days...")
    db = get_db_session()
    
    try:
        cutoff_date = date.today() - timedelta(days=days_to_keep)
        
        # Count records to be deleted (for logging, not actually deleting in demo)
        old_shifts = db.query(MiningShift).filter(
            MiningShift.shift_date < cutoff_date
        ).count()
        
        old_maintenance = db.query(MaintenanceLog).filter(
            and_(
                MaintenanceLog.is_completed == True,
                MaintenanceLog.completed_date < cutoff_date
            )
        ).count()
        
        result = {
            "cleaned_at": datetime.utcnow().isoformat(),
            "cutoff_date": cutoff_date.isoformat(),
            "shifts_eligible_for_cleanup": old_shifts,
            "maintenance_logs_eligible_for_cleanup": old_maintenance,
            "status": "completed",
            "note": "Demo mode - records not actually deleted"
        }
        
        logger.info(f"Cleanup check complete: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise
    finally:
        db.close()


# Task to be called on-demand
@shared_task(bind=True, name="app.tasks.mining_tasks.export_data")
def export_data(self, start_date: str, end_date: str, format: str = "json") -> Dict[str, Any]:
    """
    Export production data for a date range.
    
    This task demonstrates:
    - On-demand background processing
    - Data export functionality
    - Async task execution
    
    Args:
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
        format: Export format (json, csv)
        
    Returns:
        Dict containing export results
    """
    logger.info(f"Starting data export from {start_date} to {end_date}...")
    db = get_db_session()
    
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        
        # Get production records for the date range
        records = db.query(
            MiningShift.shift_date,
            MiningShift.shift_type,
            MiningShift.mine_section,
            ProductionRecord.ore_extracted_tonnes,
            ProductionRecord.waste_removed_tonnes,
            ProductionRecord.ore_grade_percentage
        ).join(
            ProductionRecord, MiningShift.id == ProductionRecord.shift_id
        ).filter(
            and_(
                MiningShift.shift_date >= start,
                MiningShift.shift_date <= end
            )
        ).all()
        
        result = {
            "exported_at": datetime.utcnow().isoformat(),
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "records_exported": len(records),
            "format": format,
            "status": "completed"
        }
        
        logger.info(f"Data export complete: {len(records)} records")
        return result
        
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise
    finally:
        db.close()
