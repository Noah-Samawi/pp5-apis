from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "owner")
    search_fields = ("owner__username", "title", "content")
    list_per_page = (
        20  # Set the number of items displayed per page in the admin list view
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {"fields": (
                "owner", "title", "content", "image", "image_filter", "tag"
            )},
        ),
        (
            "Status",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
