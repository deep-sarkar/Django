from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import HttpResponse, redirect, render
from django.core.validators import validate_email

from django.template.loader import render_to_string

'''
Errors
'''
from django.core.exceptions import ValidationError


'''
Mailings
'''
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from registration_project.settings import EMAIL_HOST_USER

'''
Short-urls
'''
from django_short_url.views import get_surl
from django_short_url.models import ShortURL

from django.db.models import Q

from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import UserRegisterSerializer
from .token_handeler import generate_token

import jwt
import re

User = get_user_model()

'''
Registration View
'''
class RegisterAPIView(generics.GenericAPIView):
    permission_classes     = [permissions.AllowAny]
    serializer_class       = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response("Someone is already logged in, please logout first to register new user.")
        data = request.data
        username    = data.get('username')
        email       = data.get('email')
        password    = data.get('password')
        password2   = data.get('password2')
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse('Please enter a valid email and try again later.')
        qs = User.objects.filter(
            Q(username__iexact=username)
        )
        if qs.exists():
            return HttpResponse('This user already exists.')
        
        '''
        Password validation
        '''
        if password != password2 :
            return Response('password must match.')
        elif len(password) < 8 :
            return HttpResponse('Password must contains atleast 8 letters.')
        elif re.search('[A-Za-z]', password) == None or re.search('[0-9]', password) == None:
            return HttpResponse('Password must contain one alphabet and one number.')
        try:
            user = User.objects.create(username=username,email=email)
            user.set_password(password) 
            user.is_active = False
            user.save()  
            payload = {
                'username': username,
                'password': password,
                 }
            token = generate_token(payload)
            current_site = get_current_site(request)
            domain_name = current_site.domain
            surl = get_surl(str(token))
            final_url = surl.split("/")
            mail_subject = "Activate your account"
            msg = render_to_string(
                'accounts/email_validation.html',
                {
                    'username': username, 
                    'domain': domain_name,
                    'surl': final_url[2],
                    })
            send_mail(mail_subject, msg, EMAIL_HOST_USER,
                      [email], fail_silently=False,)
            return HttpResponse("Thankyou for registration. Please verify your email.")
        except ValueError:
            return HttpResponse("Please enter a valid detail.")
        except Exception:
            return HttpResponse("something went wrong, please try again later.")
        

'''
Activate account by token
'''
def activate(request, surl):
    try:
        token_object = ShortURL.objects.get(surl=surl)
        token = token_object.lurl
        decode = jwt.decode(token, 'SECRET')
        username = str(decode['username'])
        user = User.objects.get(username=username)
        if user is not None:
            if user.is_active :
                return HttpResponse('This user is already activated, Please login')
            else:
                user.is_active = True
                user.save()
                return HttpResponse('your account is activated,')
        return HttpResponse("invalid credentials")
    except jwt.DecodeError:
        return HttpResponse("You are trying with old actiation code, please try again later.")