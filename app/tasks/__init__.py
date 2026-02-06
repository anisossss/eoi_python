# Celery Tasks
from app.tasks.celery_app import celery_app
from app.tasks.mining_tasks import (
    generate_daily_report,
    process_production_data,
    calculate_equipment_metrics,
    send_maintenance_alerts,
    cleanup_old_records
)

__all__ = [
    "celery_app",
    "generate_daily_report",
    "process_production_data",
    "calculate_equipment_metrics",
    "send_maintenance_alerts",
    "cleanup_old_records"
]
