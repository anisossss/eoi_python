"""
Celery Application Configuration
CSIR EOI 8119 - Mining Data Analytics API
Demonstrates background processing capabilities
"""

from celery import Celery
from celery.schedules import crontab

from app.config import settings

# Create Celery application
celery_app = Celery(
    "mining_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.mining_tasks"]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Johannesburg",
    enable_utc=True,
    
    # Task execution settings
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    
    # Result backend settings
    result_expires=86400,  # 24 hours
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
)

# Celery Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    # Generate daily production report every day at 6 AM
    "daily-production-report": {
        "task": "app.tasks.mining_tasks.generate_daily_report",
        "schedule": crontab(hour=6, minute=0),
        "args": (),
    },
    
    # Process production data every hour
    "hourly-production-processing": {
        "task": "app.tasks.mining_tasks.process_production_data",
        "schedule": crontab(minute=0),  # Every hour at minute 0
        "args": (),
    },
    
    # Calculate equipment metrics every 4 hours
    "equipment-metrics": {
        "task": "app.tasks.mining_tasks.calculate_equipment_metrics",
        "schedule": crontab(hour="*/4", minute=0),
        "args": (),
    },
    
    # Send maintenance alerts every day at 8 AM
    "maintenance-alerts": {
        "task": "app.tasks.mining_tasks.send_maintenance_alerts",
        "schedule": crontab(hour=8, minute=0),
        "args": (),
    },
    
    # Cleanup old records weekly on Sunday at midnight
    "weekly-cleanup": {
        "task": "app.tasks.mining_tasks.cleanup_old_records",
        "schedule": crontab(hour=0, minute=0, day_of_week=0),
        "args": (),
    },
}
