
from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = (
        ("comment", "Comment"),
        ("like", "Like"),
        ("follower", "Follower"),
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    related_object_id = models.PositiveIntegerField()
