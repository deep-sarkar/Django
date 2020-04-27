
from django.urls import path
from .views import create_room, delete_room, chat_home, approve_request, join_room, pending_request

urlpatterns = [
    path('', chat_home, name='chat_home'),
    path('create_room/',create_room, name='create_room'),
    path('delete_room/', delete_room, name='delete_room'),
    path('join_room/', join_room, name='join_room'),
    path('pending_request/', pending_request, name='pending_request'),
    path('approve_request/', approve_request, name='approve_request'),
]