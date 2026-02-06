"""
Analytics API Routes
CSIR EOI 8119 - Mining Data Analytics API
Demonstrates SQL aggregation and analytical queries
"""

from datetime import date, timedelta
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.mining import ProductionStats, DailyProduction
from app.services.mining import MiningService

router = APIRouter()


@router.get("/production-stats", response_model=ProductionStats)
def get_production_statistics(
    start_date: date = Query(..., description="Start date for statistics"),
    end_date: date = Query(..., description="End date for statistics"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get production statistics for a date range.
    
    Demonstrates SQL aggregation functions:
    - SUM for total ore and waste
    - AVG for average grade and workers
    - COUNT for total shifts
    """
    return MiningService.get_production_stats(db=db, start_date=start_date, end_date=end_date)


@router.get("/daily-production", response_model=List[DailyProduction])
def get_daily_production(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get daily production summaries.
    
    Demonstrates SQL GROUP BY with aggregations.
    """
    return MiningService.get_daily_production(db=db, start_date=start_date, end_date=end_date)


@router.get("/equipment-utilization", response_model=List[Dict[str, Any]])
def get_equipment_utilization(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get equipment utilization statistics.
    
    Demonstrates:
    - Complex SQL JOINs
    - Aggregation across related tables
    - ORDER BY with aggregated values
    """
    return MiningService.get_equipment_utilization(db=db)


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a quick summary of mining operations.
    
    Returns:
    - Last 7 days production stats
    - Equipment utilization
    - Recent maintenance activities
    """
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Get production stats for last 7 days
    production_stats = MiningService.get_production_stats(
        db=db, start_date=week_ago, end_date=today
    )
    
    # Get equipment utilization
    equipment_util = MiningService.get_equipment_utilization(db=db)
    
    # Get recent maintenance logs
    maintenance_logs = MiningService.get_maintenance_logs(
        db=db, skip=0, limit=5, is_completed=False
    )
    
    return {
        "period": {
            "start": week_ago.isoformat(),
            "end": today.isoformat()
        },
        "production": {
            "total_ore_extracted": production_stats.total_ore_extracted,
            "total_waste_removed": production_stats.total_waste_removed,
            "average_ore_grade": production_stats.average_ore_grade,
            "total_shifts": production_stats.total_shifts
        },
        "equipment": {
            "total_tracked": len(equipment_util),
            "top_performers": equipment_util[:5] if equipment_util else []
        },
        "pending_maintenance": len(maintenance_logs)
    }
