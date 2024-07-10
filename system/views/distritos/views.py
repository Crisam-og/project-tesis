from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from api.models import *
from system.forms.distritos.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from api.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class DistritoListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Distrito
    template_name = 'distrito/list.html'
    permission_required = 'view_distrito'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de distritos'
        context['create_url'] = reverse_lazy('distrito_create')
        return context

class DistritoCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Distrito
    form_class = DistritoForm 
    template_name = 'distrito/create.html' 
    success_url = reverse_lazy('distrito_list')
    permission_required = 'add_distrito'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No hay registros'
            
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar nuevo Distrito'
        context['entity'] = 'Distrito'
        context ['icon'] = 'fas fa-plus'
        context['list_url'] = reverse_lazy('distrito_list')
        context['action'] = 'add'

        return context
    
class DistritoUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Distrito
    form_class = DistritoForm
    template_name = 'distrito/create.html'
    success_url = reverse_lazy('distrito_list')
    permission_required = 'change_distrito'
    url_redirect = success_url
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save() 
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No hay registros'
            
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del Distrito'
        context['entity'] = 'Ddistritos'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('distrito_list')
        context['action'] = 'edit'

        return context

class DistritoDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Distrito
    template_name = 'distrito/delete.html'
    success_url = reverse_lazy('distrito_list')
    permission_required = 'delete_distrito'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de Distritos'
        context['entity'] = 'Distritos'
        context['list_url'] = reverse_lazy('distrito_list')
        return context