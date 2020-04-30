from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Message
from django.contrib.auth.decorators import login_required
import json


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
    body_data    = json.loads(request.body.decode('utf-8'))
    receiver     = body_data['receiver']
    queryset     = Message.objects.filter(sender=username, receiver=receiver)
    if queryset.count() != 1:
        queryset = Message.objects.filter(sender=receiver, receiver=username)
        if queryset.count() != 1:
            message_obj = Message.objects.create(sender=username, receiver=receiver, body="chat")
            stream = str(username)+str(receiver)
            message_obj.save() 
        else:
            stream = str(queryset[0].sender) + str(queryset[0].receiver)
    else:
        print("hello")
        stream = str(queryset[0].sender) + str(queryset[0].receiver)
        print(stream)
    response_data = {
        'data': stream
    }
    return JsonResponse(response_data)


