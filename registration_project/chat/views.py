from django.shortcuts import render
from django.http import JsonResponse

from . models import GroupChat, GroupMembers
import json

def chat_home(request):
    return render(request, 'chat/chat_home.html')


def create_room(request):
	room_name = request.POST.get('room_name')
	username = request.user.username
	queryset = GroupChat.objects.filter(room_name=room_name)

	if queryset.count() == 0:
		chat_room = GroupChat.objects.create(room_name=room_name, owner=username)
		chat_room_members = GroupMembers.objects.create(room_name=room_name, member=username, isAuthorised = True)
		chat_room.save()
		chat_room_members.save()
		return render(request, 'chat/room_general_message.html',{
			'message':'Room created. Please go back and join room'
		})

	else:
		return render(request, 'chat/room_general_message.html',{
			'message':'Room with this name already exists, please try with different name'
		})

