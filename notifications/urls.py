
from django.urls import path

from notifications import views

urlpatterns = [
    path(
        "notifications/",
        views.NotificationListView.as_view(),
        name="notification-list"
    ),
    path(
        "notifications/<int:pk>/",
        views.NotificationUpdateView.as_view(),
        name="notification-detail",
    ),
]
