from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from django.conf import settings as setting
from login.forms import CustomAuthenticationForm
from api.models import User
from django.views.generic import ListView, DetailView, TemplateView, CreateView



class LoginFormView (LoginView):
    template_name = 'login.html'
    # form_class = CustomAuthenticationForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.get_user()
        user.failed_login_attempts = 0  
        user.save()     
        login(self.request, user)
        return super().form_valid(form)
    
    # def form_invalid(self, form):
    #     username = form.cleaned_data.get('username')
    #     try:
    #         user = User.objects.get(username=username)
    #         attempt, created = User.objects.get_or_create(username=user)
    #         attempt.failed_login_attempts += 1
    #         attempt.save()

    #         if attempt.failed_login_attempts >= 3:
    #             user.is_active = False  
    #             user.save()
    #             return redirect('account_locked')

    #     except User.DoesNotExist:
    #         pass

    #     return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Cadrick | Iniciar Sesión'
        return context

class LoginFormView2 (FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
           return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Cadrick | Iniciar Sesión'
        return context
    
class LogoutRedirectView (RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    
class BlockAccountView(TemplateView):
    template_name = 'block_account.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context