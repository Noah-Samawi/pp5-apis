from django.contrib import admin

from .models import Follower


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ("owner", "followed", "created_at")  # Customize as needed
    list_filter = ("created_at",)
    search_fields = ("owner__username", "followed__username")
    list_per_page = (
        20  # Set the number of items displayed per page in the admin list view
    )
    # Mark the 'created_at' field as read-only
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("owner", "followed")}),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
