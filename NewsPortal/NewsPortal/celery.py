import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

celery_app = Celery('NewsPortal')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.update(
    timezone='Europe/Moscow',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'category_subscribtion_emails_every_week': {
        'task': 'news_feed.tasks.weekly_category_subscription_emails',
        'schedule': crontab(hour=8, day_of_week='mon'),
    }
}