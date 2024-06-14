from django.contrib import admin

from file_management.models import File, PermissionType, FileSystemNotificationType

admin.site.register(PermissionType)
admin.site.register(FileSystemNotificationType)

admin.site.register(File)
