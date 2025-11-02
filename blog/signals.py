# blog/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post


@receiver(pre_save, sender=Post)
def ensure_slug(sender, instance: Post, **kwargs):
    if not instance.slug:
        base = slugify(instance.title) or "post"
        instance.slug = base
