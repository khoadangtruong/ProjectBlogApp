from django.db import transaction
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from .tasks import send_confirmation_mail_task

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        print(f"{instance.username}'s profile is created! Sending confirm email")
        transaction.on_commit(lambda: send_confirmation_mail_task.delay(instance.email))
    else:
        instance.profile.save()
        print(f"{instance.username}'s profile is saved!")

