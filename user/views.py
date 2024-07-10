from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from api.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class UserListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'view_user'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['list_url'] = reverse_lazy('user_list')
        context['create_url'] = reverse_lazy('user_create')
        return context
    
class UserCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = User
    form_class = UserForm 
    template_name = 'user/create.html' 
    success_url = reverse_lazy('user_list')
    permission_required = 'add_user'
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
        context['title'] = 'Registrar nuevo usuario'
        context['entity'] = 'User'
        context ['icon'] = 'fas fa-plus'
        context['list_url'] = reverse_lazy('user_list')
        context['action'] = 'add'

        return context
    
class UserUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'
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
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context ['title'] = 'Editar datos del usuario'
            context ['entity'] = 'User'
            context ['icon'] = 'fas fa-pencil-alt'
            context['list_url'] = reverse_lazy('user_list')
            context['action'] = 'edit'

            return context

class UserDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'delete_user'
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
        context['title'] = 'Eliminación de usuario'
        context['entity'] = 'User'
        context['list_url'] = reverse_lazy('user_list')
        context['delete_url'] = reverse_lazy('user_delete')

        return context
class UserChangeGroup(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            print(self.kwargs)
            group_id = self.kwargs['pk']
            request.session['group'] = group_id
            Group.objects.get(pk=group_id)  # Verifica que el grupo exista
            
        except Group.DoesNotExist:
            # Manejar el caso en que el grupo no exista
            pass
        return HttpResponseRedirect(reverse_lazy('home'))

# class UserChangeGroup(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             print(self.kwargs)
#             request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
#         except: 
#             pass
#         return HttpResponseRedirect(reverse_lazy('home'))
    
# class UserChangeGroup(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             group_id = self.kwargs['pk']
#             request.session['group_id'] = group_id
#         except Exception as e:
#             print(e)  # Para depuración, quita esto en producción
#         return HttpResponseRedirect(reverse_lazy('home'))