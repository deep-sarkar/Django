from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import HttpResponse, redirect, render
from django.core.validators import validate_email
from django.contrib.auth.models import auth
from django.views.generic import TemplateView
from django.template.loader import render_to_string

'''
Errors
'''
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from smtplib import SMTPException


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
from rest_framework.views import APIView

from .serializers import ( UserRegisterSerializer, UserLoginSerializer, 
                            ResetPasswordSerializer, EmailSerializers )
from .token_handeler import generate_token

#Custom redis cache
import redis

import jwt
import re

#Redis setting
redis_object = redis.Redis(host='localhost', port=6379,db=0)

User = get_user_model()



'''
Home Page
'''
class Home(TemplateView):
    template_name = "accounts/home.html"


'''
Registration View
'''
class RegisterAPIView(generics.GenericAPIView):
    permission_classes     = [permissions.AllowAny]
    serializer_class       = UserRegisterSerializer

    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("Someone is already logged in, please logout first to register new user.")
        data = request.data
        username    = data.get('username')
        email       = data.get('email')
        password    = data.get('password')
        password2   = data.get('password2')
        try:
            validate_email(email)
        except ValidationError:
            return Response('validated_email')
        qs = User.objects.filter(
            Q(username__iexact=username)
        )
        if qs.exists():
            return HttpResponse('user_exists')
        
        '''
        Password validation
        '''
        if password != password2 :
            return HttpResponse('password_not_matched')
        elif len(password) < 8 :
            return HttpResponse('check_password')
        elif re.search('[A-Za-z]', password) == None or re.search('[0-9]', password) == None:
            return HttpResponse('check_password')
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
            return HttpResponse("success")
        except ValueError:
            return HttpResponse("valueError")
        except SMTPException:
                return Response('Bad request, please try again later.')
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

'''
Login View
'''
class LoginAPIView(generics.GenericAPIView):
    permission_classes     = [permissions.AllowAny]
    serializer_class       = UserLoginSerializer

    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("your are already loged in, please logout first for login again")
        else:    
            try:
                data = request.data
                username = data.get('username')
                password = data.get('password')
                queryset = User.objects.filter(
                    Q(username__iexact=username)|
                    Q(email__iexact=username)
                )
                print(username)
                print(password)
                if queryset.count() == 1:
                    user_obj = queryset.first()
                    if user_obj.check_password(password):
                        if user_obj.is_active:
                            payload = {
                                'username': username,
                                'password': password,
                            }
                            print(payload)
                            token = generate_token(payload)
                            print('token',token)
                            redis_object.set(username,token)
                            print('token',token)
                            auth.login(request, user_obj)
                            return Response('success')
                        return HttpResponse("verify_email")
                return HttpResponse('password_error')
            except Exception:
                return HttpResponse("Something went wrong, please try again later")

'''
Password reset View
'''
class ChangePassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def get(self, request):
        return render(request, 'accounts/changepassword.html')

    def post(self, request, *args, **kwargs):
        try:
            username = self.request.user.username
            data = request.data
            print(username)
            new_password = data.get('new_password')
            new_password_confirm = data.get('new_password_confirm')
            if new_password != new_password_confirm :
                return HttpResponse('password_must_match')
            elif len(new_password) < 8 :
                return HttpResponse('Password must contains atleast 8 letters.')
            elif re.search('[A-Za-z]', new_password) == None or re.search('[0-9]', new_password) == None:
                return HttpResponse('enter_valid_password')
            else:
                user_count = User.objects.filter(username=username).count()
                if user_count == 1:
                    user = User.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    return HttpResponse("success")
                return HttpResponse("please Login First")
        except Exception as e:
            return HttpResponse(e,"Something went wrong, please try again later")
            

'''
Default logout from auth
'''
def logout(request):
    try:
        username = request.user.username
        print(str(username))
        token = redis_object.get(username)
        print(token)
        decode = jwt.decode(token, 'SECRET')
        username = str(decode['username'])
        user = User.objects.get(username=username)
        if user.is_authenticated:
            redis_object.delete(username)
            auth.logout(request)
            token = redis_object.get(username)
            print(token)
            return render(request, 'accounts/home.html')
        return HttpResponse('User does not exist')
    except Exception:
        return Response("Something went wrong, please try again later")


'''
Forgot password view
'''
class Forgotpassword(generics.GenericAPIView):
    serializer_class = EmailSerializers

    def get(self, request):
        return render(request, 'accounts/forgot_password.html')

    def post(self, request):
        email = request.data['email']
        if email == "":
            return HttpResponse('enter_email')
        else:
            try:
                validate_email(email)
            except ValidationError:
                return HttpResponse('enter_valid_email')
            try:
                user = User.objects.filter(email=email)
                username = user.values()[0]['username'] #Fetch username still if user is not logedin
                payload = {
                        'username': username,
                        }
                token = generate_token(payload)
                current_site = get_current_site(request)
                domain_name = current_site.domain
                surl = get_surl(str(token))
                final_url = surl.split("/")
                mail_subject = "Reset Your password by clicking below link"
                msg = render_to_string(
                    'accounts/reset_password.html',
                    {
                        'username': username, 
                        'domain': domain_name,
                        'surl': final_url[2],
                        })
                send_mail(mail_subject, msg, EMAIL_HOST_USER,
                        [email], fail_silently=False)
                return HttpResponse('success')
            except SMTPException:
                return Response('Bad request, please try again later.')

'''
After sending link in mail, on clicking will redirect reset_password
'''
def reset_password(request, surl):
    try:
        token_object = ShortURL.objects.get(surl=surl)
        token = token_object.lurl
        decode = jwt.decode(token, 'SECRET')
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:
            return redirect('/activatenewpassword/' + str(user)+'/')
        else:
            return HttpResponse('Invalid')
    except jwt.DecodeError:
        return HttpResponse('Something went wrong')


'''
Reset and activate new password when usere request for forgot password
'''
class ActivateNewPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def get(self, request, user_reset):
        return render(request, 'accounts/reset_new_password.html')

    def post(self, request, user_reset):
        new_password = request.data['new_password']
        new_password_confirm = request.data['new_password_confirm']

        if user_reset is None:
            return HttpResponse('not a valid user.')
        if new_password != new_password_confirm :
            return Response('password_must_match')
        elif len(new_password) < 8 :
            return HttpResponse('Password must contains atleast 8 letters.')
        elif re.search('[A-Za-z]', new_password) == None or re.search('[0-9]', new_password) == None:
            return HttpResponse('enter_valid_password')
        else:
            try:
                user = User.objects.get(username=user_reset)
                user.set_password(new_password)
                user.save()
                return render(request, 'accounts/home.html')
            except ObjectDoesNotExist:
                return HttpResponse('not a valid user.')
