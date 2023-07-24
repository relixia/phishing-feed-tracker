from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

app.conf.beat_schedule = {
    "run-usom-check-every-15-minutes": {
        "task": "tasks.usom_check_time_interval",
        "schedule": crontab(minute='*/15'),
    },
    "run-phishtank-check-every-15-minutes": {
        "task": "tasks.phishtank_check_time_interval",
        "schedule": crontab(minute='*/15'),
    },
    "run-openphish-check-every-15-minutes": {
        "task": "tasks.openphish_check_time_interval",
        "schedule": crontab(minute='*/15'),
    },
    "run-phishstats-check-every-15-minutes": {
        "task": "tasks.phishstats_check_time_interval",
        "schedule": crontab(minute="*/15"),
    },
    "run-url-status-check-daily": {
        "task": "tasks.check_url_status_daily",
        "schedule": crontab(hour=4, minute=30),
    },
    
}

app.conf.timezone = "Europe/Istanbul" 
