# authentication/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import components.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authentication.settings')

# Define the Django ASGI application
django_asgi_application = get_asgi_application()

# Define the WebSocket routing configuration
websocket_routing = URLRouter(components.routing.websocket_urlpatterns)

# Define the protocol type router to handle both HTTP and WebSocket connections
application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': websocket_routing,
})
