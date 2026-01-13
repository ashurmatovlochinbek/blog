from django.urls import re_path
from django.urls import path

from chat import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<int:blog_id>/', consumers.ChatConsumer.as_asgi()),
]