from django.urls import path, include
from login.views import *
urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('account-locked/', BlockAccountView.as_view(), name='account_locked'),


]
