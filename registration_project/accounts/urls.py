from django.urls import path
from .views import (RegisterAPIView, activate, LoginAPIView, 
                LogoutView, ChangePassword, Forgotpassword, reset_password, ActivateNewPassword, Home )


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<surl>/', activate, name='activate'),
    path('login/',LoginAPIView.as_view(), name='login'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgotpassword/', Forgotpassword.as_view(), name='forgotpassword'),
    path('resetpassword/<surl>/',reset_password, name='resetpassword'),
    path('activatenewpassword/<user_reset>/',ActivateNewPassword.as_view(), name='activatenewpassword'),
    path('', Home.as_view(), name='home'),
]