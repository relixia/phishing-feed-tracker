from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

app.conf.beat_schedule = {
    "run-usom-check-every-30-minutes": {
        "task": "tasks.usom_check_time_interval",
        "schedule": crontab(minute='*/15'),
    },
    "run-phishtank-check-every-30-minutes": {
        "task": "tasks.phishtank_check_time_interval",
        "schedule": crontab(minute='*/15'),
    },
    "run-openphish-check-every-30-minutes": {
        "task": "tasks.openphish_check_time_interval",
        "schedule": crontab(minute='*/15'),
    },
    "run-phishstats-check-every-5-minutes": {
        "task": "tasks.phishstats_check_time_interval",
        "schedule": crontab(minute="*/15"),
    },
    
}

app.conf.timezone = "Europe/Istanbul" 
