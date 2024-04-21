from django.urls import path , include
from livechat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) , 
] 