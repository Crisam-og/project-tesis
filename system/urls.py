from django.urls import path, include
from system.views.distritos.views import *
from system.views.reportes.views import *

from system.views.home.views import *

from django.conf import settings
from django.contrib.staticfiles.urls import static
#E:\Workspace\app\inv\system\views
urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'), 
    path('reporte/list/', ReporteListView.as_view(), name='reporte_list'), 
    path('distrito/list/', DistritoListView.as_view(), name='distrito_list'), 
    path('distrito/add/', DistritoCreateView.as_view(), name='distrito_create'),  
    path('distrito/edit/<int:pk>/', UpdateView.as_view(), name='distrito_update'),  
    path('distrito/delete/<int:pk>/', DeleteView.as_view(), name='distrito_delete'), 
    path('api/get/reporte/', getAPI, name='api'), 


 ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
