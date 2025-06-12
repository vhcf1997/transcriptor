# projeto_transcritor/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')

app = Celery('transcript')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()