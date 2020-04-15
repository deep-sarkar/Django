from django.urls import path
from .views import RegisterAPIView, activate, LoginAPIView, logout, ChangePassword, Forgotpassword


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<surl>/', activate, name='activate'),
    path('login/',LoginAPIView.as_view(), name='login'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword'),
    path('logout/', logout, name='logout'),
    path('forgotpassword/', Forgotpassword.as_view(), name='forgotpassword'),
]