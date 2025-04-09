from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Define WebSocket route and link it to the NotificationConsumer
    re_path(r'ws/notifications/(?P<user_id>\w+)/$', consumers.NotificationConsumer.as_asgi()),
]
