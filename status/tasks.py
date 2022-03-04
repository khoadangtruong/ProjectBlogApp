from celery import shared_task
from celery.utils.log import get_task_logger

from django.db import connection
from django.core.mail import send_mail
from django.contrib.auth.models import User

from blogapp import settings

logger = get_task_logger(__name__)

@shared_task(name = "db_health_check_task")
def db_health_check_task():
    logger.info('Check DB Connection')
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return 'Connection is OK'
    except Exception as ex:
        
        email_subject = 'DB Connection Check Report!'
        message = 'This is a message from Celery that your db connection is FAILED!'
        
        send_mail(
            subject = email_subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = ['admkhoa173@gmail.com',],
            fail_silently = True,
        )
        return 'Connection is FAILED'