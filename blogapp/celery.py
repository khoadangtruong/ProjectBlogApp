from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogapp.settings')

app = Celery('blogapp')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Vietnam')
app.config_from_object(settings, namespace = 'CELERY')

# Celery Beat Settings
app.conf.beat_scheduler = {}

app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print(f'Request: {self.request!r}')