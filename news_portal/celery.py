import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'email_news_every_monday': {
        'task': 'simpleapp.tasks.send_week_notification',
        # 'schedule': crontab (hour = 8, minute=0, day_of_week='mon'),
        'schedule': 10,
        'args':(),
    },
}