# components/routing.py
from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns = [
    path('wc/sc/', MyConsumer.as_asgi()),  # Add this line for the missing route
]
