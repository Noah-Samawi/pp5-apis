from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "message",
            "created_at",
            "read",
            "notification_type",
            "related_object_id",
        ]
        read_only_fields = [
            "id",
            "recipient",
            "created_at",
            "notification_type",
            "related_object_id",
        ]