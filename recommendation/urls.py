from django.urls import path
from recommendation import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
