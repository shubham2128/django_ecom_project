from django.urls import path, include
from home import views as home_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", home_views.homePage, name="home-page"),
    path("auth/login/", LoginView.as_view
         (template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]