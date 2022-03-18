from django.core.mail import send_mail
from django.contrib.auth.models import User

from celery import shared_task, Celery
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

from blogapp import settings

logger = get_task_logger(__name__)

@shared_task(bind = True, name = "send_confirmation_mail_task")
def send_confirmation_mail_task(self, email):
    logger.info("Sent Confirmation Email")
    user = User.objects.filter(email = email)
    email_subject = 'Activation Mail'
    message = 'This is a message from Celery testing processes!'
    send_mail(
        subject = email_subject,
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [email,],
        fail_silently = True,
    )
    return "Confirm email sent to user"
    
@shared_task(
    bind = True, name = "send_all_mail_task",
    track_started = True, soft_time_limit = 20
)
def send_all_mail_task(self, email):
    logger.info("Sent All Email")
    users = User.objects.exclude(email = email).all()
    try:
        for user in users:
            mail_subject = 'To All Creator!'
            message = 'This is an email from admin using Celery Beat to all you guys!'
            to_email = user.email
            send_mail(
                subject = mail_subject,
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [to_email,],
                fail_silently = True,
            )
        return "All email have sent to all creators"
    except SoftTimeLimitExceeded:
        return 'Task ran out of time'