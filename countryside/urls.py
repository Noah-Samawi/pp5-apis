from django.urls import path
from countryside import views

urlpatterns = [
    path('countryside/', views.CountrysideList.as_view()),
    path('countryside/<int:pk>/', views.CountrysideDetail.as_view()),
]
