from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from api.models import *
from system.forms.distritos.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from api.mixin import *
import requests
from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class ReporteListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Reporte
    template_name = 'reportes/list.html'
    success_url = reverse_lazy('reporte_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Reportes'
        context['entity'] = 'Reportes'
        context['list_url'] = self.success_url
        return context
    
# class ReporteViewSet(viewsets.ModelViewSet):
#     queryset = Reporte.objects.all()
#     serializer_class = ReporteSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(cliente=self.request.user)   


def getAPI(request):
    # URL de productos
    URL_API = "https://cristhianog25.pythonanywhere.com/api/get/reporte/"

    # Realizar la solicitud GET a la API
    response = requests.get(URL_API)

    if response.status_code == 200:
        # se utiliza el método json() para extraer los datos en formato JSON de la respuesta y se almacenan en la variable productos
        reportes = response.json()
        
        for reporte in reportes:
            print(reporte)
        
        return HttpResponse(reportes) or []
    
def obtener_reportes(request):
    URL_API = "https://cristhianog25.pythonanywhere.com/api/get/reporte/"
    try:
        # Intenta realizar la solicitud GET a la API
        response = requests.get(URL_API)
        if response.status_code == 200:
            # se utiliza el método json() para extraer los datos en formato JSON de la respuesta y se almacenan en la variable productos
            reportes = response.json()
        else:
            # En caso de un código de respuesta no exitoso, manejar de acuerdo a tus necesidades
            print(f"Error en la solicitud: {response.status_code}")
            reportes = []
    except requests.RequestException as e:
        # Manejar errores de solicitud, por ejemplo, problemas de red
        print(f"Error en la solicitud: {e}")
        reportes = []

    return render(request, 'reportes/list_2.html', {'reportes': reportes})         
    
    