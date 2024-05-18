from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "name", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("owner__username", "name", "content")
    list_per_page = (
        20  # Set the number of items displayed per page in the admin list view
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "owner",
                    "name",
                    "content",
                    "image",
                    "facebook_link",
                    "twitter_link",
                    "linkedin_link",
                )
            },
        ),
        (
            "Status",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
