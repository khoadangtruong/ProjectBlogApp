from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery import shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogapp.settings')

app = Celery('blogapp')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Ho_Chi_Minh')
app.config_from_object(settings, namespace = 'CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {

    'check_db_connection_every_minute': {
        'task': 'db_health_check_task',
        'schedule': 60.0,
        # 'args': ()
    },

    'send_mail_every_5_minute': {
        'task': 'send_all_mail_task',
        'schedule': crontab(minute = '*/5'),
        'args': ('khoadangtruong99@gmail.com',)
    },

    # 'test_task_every_30_1': {
    #     'task': 'blog.tasks.test_task_1',
    #     'schedule': 30.0,
    #     # 'args': ()
    # },

    # 'test_task_every_30_2': {
    #     'task': 'blog.tasks.test_task_2',
    #     'schedule': 30.0,
    #     # 'args': ()
    # },

    # 'test_task_every_30_3': {
    #     'task': 'blog.tasks.test_task_3',
    #     'schedule': 30.0,
    #     # 'args': ()
    # },
}

app.autodiscover_tasks()

@app.task(bind = True, name = 'debug_task')
def debug_task(self):
    print(f'Request: {self.request!r}')


# worker: celery -A blogapp.celery worker --concurrency=4 --autoscale=4,2 -l info 
# add worker: celery -A blogapp.celery worker -n worker1example.com -l info
# beat: celery -A blogapp beat -l info
# status: celery -A blogapp status
# bind, name, ignore_result, rate_limit, time_limit, soft_time_limit, track_started