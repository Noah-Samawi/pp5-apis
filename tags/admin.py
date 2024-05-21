from django.contrib import admin
from .models import Tags

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'post', 'created_at')
    search_fields = ('owner__username', 'post__title')
    list_filter = ('created_at',)
