from django.db import models
from django.contrib.auth.models import User

class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=False)
    notification_frequency = models.IntegerField(choices=((1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')), default=1)

