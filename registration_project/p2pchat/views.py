from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Message 
from django.contrib.auth.decorators import login_required
import json

'''
Exceptions
'''
from .exceptions import EmptyMessageError





User = get_user_model()


@login_required(login_url='/login/')
def p2phome(request):
    return render(request, 'p2p/home.html')

def contact_list(request):
    username     = request.user.username
    queryset = User.objects.exclude(username=username)
    all_contacts = [item.username for name, item in enumerate(queryset)]
    response_data = {
		'data': all_contacts
    }
    return JsonResponse(response_data)

def get_stream(request):
    username     = request.user.username
    try:
        body_data    = json.loads(request.body.decode('utf-8'))
        receiver     = body_data['receiver']
    except json.JSONDecodeError:
        return HttpResponse("Something went wrong. Please try after sometime.")
    queryset     = Message.objects.filter(sender=username, receiver=receiver)
    if queryset.count() == 0:
        queryset     = Message.objects.filter(sender = receiver, receiver = username)
        if queryset.count() == 0:
            stream = username + receiver
            message_obj = Message.objects.create(stream=stream, sender=username, receiver=receiver,  body="chat")
            message_obj.save() 
            response_data = {
            'data': stream
            }
            return JsonResponse(response_data)
    stream = queryset[0].stream
    response_data = {
            'data': stream
        }
    return JsonResponse(response_data)


def chat_room(request, stream):
    stream_name = stream
    return render(request, "p2p/chat_room.html",{
        "stream":stream_name
    })

def save_message(request):
    try:
        body_data    = json.loads(request.body.decode('utf-8'))
        user         = body_data['user']
        message      = body_data['message']
        stream       = body_data['stream']
        other_user   = stream.replace(user,'')
    except json.JSONDecodeError:
        return HttpResponse("Getting some problem to save data.")
    if message == "":
        raise EmptyMessageError("Message body is empty")
    message_obj  = Message.objects.create(sender=user, receiver=other_user, stream=stream, body=message)
    message_obj.save()
    response_data = {
        'status_code': 200
    }
    return JsonResponse(response_data)

def get_message(request):
    username     = request.user.username
    try:
        body_data    = json.loads(request.body.decode('utf-8'))
        stream       = body_data['stream']
    except json.JSONDecodeError:
        return HttpResponse("Getting some issue in fetching message. Please try after sometime.")
    messages     = Message.objects.filter(stream=stream)
    all_message  = [[item.sender,item.body] for message, item in enumerate(messages)]
    response_data = {
        "data":all_message,
        "user": username
    }
    return JsonResponse(response_data)

