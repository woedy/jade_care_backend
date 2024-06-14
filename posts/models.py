import os
import random

from django.db import models
from django.db.models.signals import pre_save, post_save

from mysite import settings
from mysite.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(null=True, blank=True)
    date_published = models.DateTimeField(null=True, blank=True, verbose_name="date published")
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(post_pre_save_receiver, sender=Post)



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_post_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "posts/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')
    caption = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_post_path, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)