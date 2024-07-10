from django.contrib import admin
from django.urls import path
from .views import *
from system.views.reportes.views import *

urlpatterns = [
    path('register/client/', RegisterClientAPIView.as_view(), name='register_client_api'),
    path('login/client/', LoginClientAPIView.as_view(), name='login_client_api'),

    path('get/distrito/', DistritoAPIView.as_view(), name='get_distrito_api'),
    path('get/cliente/', ClienteAPIView.as_view(), name='get_cliente_api'),
    path('get/reporte/', ReporteAPIView.as_view(), name='get_reporte_api'),

    path('register/distrito/', RegisterDistritoAPIView.as_view(), name='register_distrito_api'),
    path('register/reporte/', RegisterReporteAPIView.as_view(), name='register_reporte_api'),
    path('get/reportes/', obtener_reportes, name='obtener_reportes'),
    path('get/rep/', getAPI, name='getAPI'),

]