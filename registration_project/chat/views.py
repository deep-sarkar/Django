from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Room, RoomMember
import json

def chat_home(request):
	return render(request, 'chat/chat_home.html')

def create_room(request):
	room_name = request.POST.get('room_name')
	username = request.user.username
	room = Room.objects.filter(room_name=room_name)

	if room is None:
		Room.objects.create(room_name=room_name, owner=username)
		RoomMember.objects.create(room_name=room_name, member=username, isAuthenticated = True)
		return render(request, 'accounts/home.html')

	else:
		return render(request, 'chat/room_error_message.html',{
			'message':'Room eith this name already exists, please try with different name'
		})