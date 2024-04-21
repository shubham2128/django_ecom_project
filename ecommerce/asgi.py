import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
# Import WebSocket URL patterns from both apps
from livechat.routing import websocket_urlpatterns as livechat_ws_patterns
from promotions.routing import websocket_urlpatterns as promotions_ws_patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                livechat_ws_patterns + promotions_ws_patterns
            )
        )
    ),
})
