from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class RecentActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recent_activities')
    subject = models.CharField(max_length=500, unique=False, blank=True, null=True)
    verb = models.CharField(max_length=700, unique=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

