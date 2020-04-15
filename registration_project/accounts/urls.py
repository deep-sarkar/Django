from django.urls import path
from .views import RegisterAPIView, activate, LoginAPIView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<surl>/', activate, name='activate'),
    path('login/',LoginAPIView.as_view(), name='login'),
]