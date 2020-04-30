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

