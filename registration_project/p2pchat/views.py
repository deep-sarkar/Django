from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Message 
from django.contrib.auth.decorators import login_required
import json

'''
Exceptions
'''
from .exceptions import EmptyMessageError, EmptyContactListError





User = get_user_model()






'''
Peer to Peer chat home view.
'''
@login_required(login_url='/login/')
def p2phome(request):
    return render(request, 'p2p/home.html')

'''
Fetch all the contact from User model except current user.
'''
def contact_list(request):
    username      = request.user.username
    queryset      = User.objects.exclude(username=username)
    if queryset.count() == 0:
        raise EmptyContactListError("You dont ahve any contact in your contact list.")  #Raising costom exception.
    all_contacts  = [item.username for name, item in enumerate(queryset)]        #Creating a list of username presenr in user model
    response_data = {
		'data': all_contacts
    }
    return JsonResponse(response_data)

'''
To communicate with a user, both user will need a common plateform.  get_or_create_stream() will fetch username from
both the sender and receiver and if there is any existing conversation between them, then it will fetch stream else it
will create stream.
'''
def get_or_create_stream(request):
    username     = request.user.username
    try:
        body_data    = json.loads(request.body.decode('utf-8'))       #Requesting data from frontend in json form
        receiver     = body_data['receiver']                   #Fetching receiever from json data
    except json.JSONDecodeError:
        return HttpResponse("Something went wrong. Please try after sometime.")
    queryset     = Message.objects.filter(sender=username, receiver=receiver)  #Checking for existing conversation
    if queryset.count() == 0:
        queryset     = Message.objects.filter(sender = receiver, receiver = username) #Checking for existing conversation
        if queryset.count() == 0:
            stream = username + receiver        #If conversation is not there, will create a common stream for both users
            message_obj = Message.objects.create(stream=stream, sender=username, receiver=receiver,  body="chat")
            message_obj.save() 
            response_data = {
            'data': stream
            }
            return JsonResponse(response_data)
    stream = queryset[0].stream    #If tehre is existing conversation, will fetch stream from there.
    response_data = {
            'data': stream
        }
    return JsonResponse(response_data)

'''
To enter a chat room.
'''
def chat_room(request, stream):
    stream_name = stream
    return render(request, "p2p/chat_room.html",{
        "stream":stream_name
    })

'''
save_message() will fetch message from frontend and save it to django database.
'''
def save_message(request):
    try:
        body_data    = json.loads(request.body.decode('utf-8')) #Fetching data from front-end in json formate 
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

'''
get_message() method will fetch all the message by providing sender and user and will return all message with sender name
in json form.
'''
def get_message(request):
    username     = request.user.username
    try:
        body_data    = json.loads(request.body.decode('utf-8')) #Fetching data from front-end in json formate
        stream       = body_data['stream']
    except json.JSONDecodeError:
        return HttpResponse("Getting some issue in fetching message. Please try after sometime.")
    if username in stream:
        messages     = Message.objects.filter(stream=stream)
        all_message  = [[item.sender,item.body] for message, item in enumerate(messages)]
        response_data = {
            "data":all_message,
            "user": username
        }
        return JsonResponse(response_data)
    return HttpResponse("Invalid request")

