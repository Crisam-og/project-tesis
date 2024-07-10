from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from crum import get_current_request
from django.contrib.auth.models import Group

class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect ('home')


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        if 'group' in request.session:
            group_id = request.session['group']
            try:
                group = Group.objects.get(id=group_id)
                if group.permissions.filter(codename=self.permission_required).exists():
                    return super().dispatch(request, *args, **kwargs)
                else:
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
            except Group.DoesNotExist:
                messages.error(request, 'Grupo no válido')
        else:
            messages.error(request, 'No tiene permiso para ingresar a este módulo')
        
        return HttpResponseRedirect(self.get_url_redirect())
    

# class ValidatePermissionRequiredMixin(object):
#     permission_required = ''
#     url_redirect = None

#     # def get_perms(self):
#     #     if isinstance(self.permission_required, str):
#     #         perms = (self.permission_required,)
#     #     else:
#     #         perms = self.permission_required
#     #     return perms

#     def get_url_redirect(self):
#         if self.url_redirect is None:
#             return reverse_lazy('login')
#         return self.url_redirect

#     def dispatch(self, request, *args, **kwargs):
#         request = get_current_request()
#         if 'group' in request.session:
#             group = request.session['group']
#             #group = Group.objects.get(pk=1)
#             if group.permissions.filter(codename=self.permission_required):
#                 return super().dispatch(request, *args, **kwargs)
#         messages.error(request, 'No tiene permiso para ingresar a este módulo')
#         return HttpResponseRedirect(self.get_url_redirect())

# class ValidatePermissionRequiredMixin(object):
#     permission_required = ''
#     url_redirect = None

#     def get_perms(self):
#         if isinstance(self.permission_required, str):
#             perms = (self.permission_required,)
#         else:
#             perms = self.permission_required
#         return perms

#     def get_url_redirect(self):
#         if self.url_redirect is None:
#             return reverse_lazy('login')
#         return self.url_redirect

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.has_perms(self.get_perms()):
#             return super().dispatch(request, *args, **kwargs)
#         messages.error(request, 'No tiene permiso para ingresar a este módulo')
#         return HttpResponseRedirect(self.get_url_redirect())