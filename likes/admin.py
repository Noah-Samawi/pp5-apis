from django.contrib import admin

from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("owner__username", "post__title")  # Adjust as needed
    list_per_page = (
        20  # Set the number of items displayed per page in the admin list view
    )
    # Mark the 'created_at' field as read-only
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("owner", "post")}),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
