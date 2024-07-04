from django.contrib import admin
from django.urls import path
from .views import RegisterClientAPIView, LoginClientAPIView

urlpatterns = [
    path('register/client/', RegisterClientAPIView.as_view(), name='register_client_api'),
    path('login/client/', LoginClientAPIView.as_view(), name='login_client_api'),
]