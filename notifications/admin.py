from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "message",
        "created_at",
        "read",
        "notification_type",
        "related_object_id",
    )
    list_filter = ("created_at", "read", "notification_type")
    search_fields = ("recipient__username", "message")
    list_per_page = (
        20  # Set the number of items displayed per page in the admin list view
    )
    readonly_fields = (
        "created_at",
        "related_object_id",
    )  # Mark some fields as read-only

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "recipient",
                    "message",
                    "notification_type",
                    "related_object_id",
                )
            },
        ),
        (
            "Status",
            {
                "fields": ("read",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )