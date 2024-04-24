# components/routing.py
from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns = [
    path('wc/sc/', MyConsumer.as_asgi()),
]


# Use daphne in development, for the great runserver integration.
# Use uvicorn in production, because I’m already using gunicorn.