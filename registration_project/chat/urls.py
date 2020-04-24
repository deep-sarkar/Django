
from django.urls import path

from .views import chat_home, create_room

urlpatterns = [
    path('', chat_home, name='chat_home'),
    path('create_room/', create_room, name='create_room'),
]