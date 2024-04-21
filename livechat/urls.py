from django.urls import path, include
from livechat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('chat/', chat_views.chatPage , name='LiveChat'),
    path("", chat_views.chatPage, name="chat-page"),
    path("auth/login/", LoginView.as_view
         (template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]