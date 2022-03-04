from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogapp.settings')

app = Celery('blogapp')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Ho_Chi_Minh')
app.config_from_object(settings, namespace = 'CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {

    'check_db_connection_every_60': {
        'task': 'db_health_check_task',
        'schedule': 60.0,
        # 'args': ()
    },

    # 'send_mail_every_30': {
    #     'task': 'send_all_mail_task',
    #     'schedule': 30.0,
    # },

}

app.autodiscover_tasks()

# @app.task(bind = True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')


# worker: celery -A blogapp.celery worker -l info
# beat: celery -A blogapp beat -l info