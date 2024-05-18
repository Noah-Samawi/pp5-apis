from django.urls import path

from tags import views

urlpatterns = [
    path("tags/", views.TagList.as_view(), name="tag-list"),
]
