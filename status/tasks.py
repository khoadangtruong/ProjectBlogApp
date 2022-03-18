from celery import shared_task, current_app
from celery.utils.log import get_task_logger

from django.db import connection
from django.core.mail import send_mail
from django.contrib.auth.models import User

from blogapp import settings
from blogapp.celery import app

logger = get_task_logger(__name__)

# @app.task(bind = True, name = "db_health_check_task")
@shared_task(bind = True, name = "db_health_check_task")
def db_health_check_task(self):
    logger.info(f'ID: {self.request.id} - DB Health Check')
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            one = cursor.fetchone()[0]
            if one != 1:
                raise Exception('FAILED')
        return 'SUCCESS'
    except Exception as exc:
        email_subject = 'DB Connection Check Report!'
        message = 'This is a message from Celery that your db connection is FAILED!'
        send_mail(
            subject = email_subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = ['admkhoa173@gmail.com',],
            fail_silently = True,
        )
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc = exc, max_retries = 5, countdown = 5)