from django.urls import path
from feedback import views

urlpatterns = [
    path('', views.feedback_submission, name='feedback-submission'),
    path('thanks/', views.feedback_thanks, name='feedback-thanks'),
    
]