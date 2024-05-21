from django.urls import path
from tags import views

urlpatterns = [
    path('tags/', views.TagsList.as_view()),
    path('tags/<int:pk>/', views.TagsDetail.as_view()),
]
