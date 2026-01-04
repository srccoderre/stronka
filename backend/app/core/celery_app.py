"""Celery configuration for background tasks."""
from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "portfel",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.report_tasks",
        "app.tasks.data_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Periodic tasks configuration
celery_app.conf.beat_schedule = {
    "send-goal-reminders": {
        "task": "app.tasks.notification_tasks.send_goal_reminders",
        "schedule": 86400.0,  # Daily
    },
    "generate-monthly-reports": {
        "task": "app.tasks.report_tasks.generate_monthly_reports",
        "schedule": 86400.0,  # Daily
    },
    "cleanup-old-notifications": {
        "task": "app.tasks.data_tasks.cleanup_old_notifications",
        "schedule": 604800.0,  # Weekly
    },
}
