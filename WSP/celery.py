# WSP/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WSP.settings')

app = Celery('WSP')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()