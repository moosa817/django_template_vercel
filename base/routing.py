from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:pk>', consumers.ChatConsumer.as_asgi()),
]
