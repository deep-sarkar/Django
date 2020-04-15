from django.urls import path
from .views import RegisterAPIView, activate


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<surl>/', activate, name='activate'),
]