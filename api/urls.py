from django.contrib import admin
from django.urls import path
from .views import RegisterClientAPIView, LoginClientAPIView, DistritoAPIView, RegisterDistritoAPIView

urlpatterns = [
    path('register/client/', RegisterClientAPIView.as_view(), name='register_client_api'),
    path('login/client/', LoginClientAPIView.as_view(), name='login_client_api'),
    path('get/distrito/', DistritoAPIView.as_view(), name='get_distrito_api'),
    path('register/distrito/', RegisterDistritoAPIView.as_view(), name='register_distrito_api'),
]