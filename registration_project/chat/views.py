from django.shortcuts import render,HttpResponse
from django.http import JsonResponse

from .models import GroupChat, GroupMembers
import json


from django.template.loader import TemplateDoesNotExist

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

def delete_room(request):
	room_name = request.POST.get('delete_room')
	username = request.user.username
	queryset = GroupChat.objects.filter(room_name=room_name)
	if queryset.count() != 1:
		return render(request, 'chat/room_general_message.html',{
			'message':'Room does not exixts...'
		})
	
	else:
		if queryset[0].owner != username:
			return render(request, 'chat/room_general_message.html',{
			'message':'You are not authorised to delete this room...'
		})

		else:
			queryset.delete()
			return render(request, 'chat/room_general_message.html',{
				'message':'Room Deleted..'
			})

def join_room(request):
	room_name = request.POST.get('join_room')
	username  = request.user.username
	queryset  = GroupChat.objects.filter(room_name=room_name)

	if queryset.count() != 1:
		return render(request, 'chat/room_general_message.html',{
			'message':'Room does not exists!!!!'
		})
	else:
		if queryset[0].owner == username:
			isOwner = True
			return render(request,'chat/room.html',{
				'room_name':room_name,
				'isOwner':isOwner
			})
		else:
			isOwner = False
			member  = GroupMembers.objects.filter(room_name=room_name, member=username)

			if member.count() == 0:
				GroupMembers.objects.create(room_name=room_name, member=username,isAuthorised=False)
				return render(request,'chat/room_general_message.html',{
					'message':'You are not a member of this group. Joining request hsa been sent to admin'
				})
			else:
				if member[0].isAuthorised:
					return render(request, 'chat/room.html',{
						'room_name':room_name,
						'isOwner':isOwner
					})
				else:
					return render(request, 'chat/room_general_message.html',{
						'message':'Your request to join has not been approved yet.'
					})

def pending_request(request):
	request_body_data = request.body.decode('utf-8')
	body_data 		  = json.loads(request_body_data)
	room_name 		  = body_data['room_name']

	unAuthorised_members = GroupMembers.objects.filter(room_name=room_name, isAuthorised=False)
	pending_request  	 = [group.member for name, group in enumerate(unAuthorised_members)]

	response_data = {
		'data': pending_request
	}
	return JsonResponse(response_data)

def approve_request(request):
	request_body_data = request.body.decode('utf-8')
	body_data 		  = json.loads(request_body_data)
	room_name 		  = body_data['room_name']
	requested_user	  = body_data['member']
	
	GroupMembers.objects.filter(room_name=room_name, member=requested_user).update(isAuthorised=True)

	response_data = {
		'status_code':200,
	}
	return JsonResponse(response_data)