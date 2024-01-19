import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Railway_Management.settings")
app = Celery("trains")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'create-daily-train-runs': {
        'task': 'trains.tasks.schedule',
        'schedule': crontab(hour=0, minute=0),
    },
}

@app.task
def addnumber():
    return

app.autodiscover_tasks()