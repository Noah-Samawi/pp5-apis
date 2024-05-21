from django.urls import path
from wanderers import views


urlpatterns = [
    path('wanderers/', views.WandererList.as_view()),
    path('wanderers/<int:pk>/', views.WandererDetail.as_view()),
]
