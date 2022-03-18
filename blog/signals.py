from re import I
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    pre_delete, post_delete,
    m2m_changed
)
from .models import Blog

@receiver(pre_save, sender = Blog)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    else:
        instance.slug = slugify(instance.name)

@receiver(pre_delete, sender = Blog)
def pre_delete_signal(sender, instance, **kwargs):
    print(f"{instance.name} will be deleted!")

@receiver(post_delete, sender = Blog)
def post_delete_signal(sender, instance, **kwargs):
    print(f"{instance.name} is deleted!")

@receiver(m2m_changed, sender = Blog.participants.through)
def blog_participants_changed(action, model, pk_set, *args, **kwargs):
    qs = model.objects.filter(pk__in = pk_set)
    if action == 'post_add':
        print(f"{qs.count()} user has joined")
    elif action == 'post_remove':
        print(f"{qs.count()} user has left")
