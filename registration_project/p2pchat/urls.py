from django.urls import path
from .views import p2phome, contact_list, get_stream,chat_room,save_message

urlpatterns =[
    path('', p2phome, name='p2phome'),
    path('contact_list/', contact_list, name='contact_list'),
    path('get_stream/', get_stream, name='get_stream'),
    path('chat_room/<stream>', chat_room, name="chat_room"),
    path('save_message/', save_message, name='save_message')
]