from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.consumers 
import p2pchat.consumers

from django.urls import re_path

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', chat.consumers.ChatConsumer),
            re_path(r'ws/chat/(?P<stream>\w+)/$', chat.consumers.ChatConsumer),
        ])
    ),
})