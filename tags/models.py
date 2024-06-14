from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from mysite.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class Tag(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
