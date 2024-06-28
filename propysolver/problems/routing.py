from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/pybot/', consumers.ChatConsumer.as_asgi()),
]