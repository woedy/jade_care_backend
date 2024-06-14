import os
import random

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save

from mysite import settings
from mysite.utils import unique_slug_generator
from tags.models import Tag

User = settings.AUTH_USER_MODEL


###########################
# FILE
############################
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "files/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



class PermissionType(models.Model):
    read = models.BooleanField(default=True,)
    write = models.BooleanField(default=False,)
    edit = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    restrict = models.BooleanField(default=False)
    downloadable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FileSystemNotificationType(models.Model):
    upload = models.BooleanField(default=False,)
    download = models.BooleanField(default=False,)
    write = models.BooleanField(default=False,)
    edit = models.BooleanField(default=False)
    delete = models.BooleanField(default=False,)
    move = models.BooleanField(default=False,)
    copy = models.BooleanField(default=False, )
    share = models.BooleanField(default=False,)
    view = models.BooleanField(default=False,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class FileManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (Q(name__icontains=query) | Q(description__icontains=query) | Q(slug__icontains=query))

            qs = qs.filter(or_lookup).distinct()
        return qs

class File(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    file_tags = models.ManyToManyField(Tag, blank=True)

    file = models.FileField(upload_to=upload_file_path, null=True, blank=True)
    file_ext = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.CharField(max_length=255, null=True, blank=True)

    favorite = models.BooleanField(default=False, blank=True, null=True)

    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    protected = models.BooleanField(default=False)

    permissions = models.ForeignKey(PermissionType, on_delete=models.SET_NULL, null=True, blank=True)
    notification_types = models.ForeignKey(FileSystemNotificationType, on_delete=models.SET_NULL, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FileManager()

    def __str__(self):
        if self.user:
            return str(self.name) + " - " + str(self.user.email)
        return str(self.name)

def file_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(file_pre_save_receiver, sender=File)