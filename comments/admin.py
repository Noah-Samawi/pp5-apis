from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "post", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("owner__username", "post__title", "content")
    list_per_page = (
        20  # Set the number of items displayed per page in the admin list view
    )
    # Mark fields as read-only if needed
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("owner", "post", "content")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        # Override the save_model method if you need to
        # perform any additional actions
        # when saving a comment, such as setting the owner.
        if not obj.owner:
            obj.owner = request.user
        obj.save()
