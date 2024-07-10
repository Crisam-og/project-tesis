from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from api.models import User

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Esta cuenta está bloqueada debido a demasiados intentos fallidos."),
                code='account_locked',
            )
        super().confirm_login_allowed(user) 

    def get_invalid_login_error(self):
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
            if user.is_active:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3: 
                    user.is_active = False
                user.save()

        except User.DoesNotExist:
            pass
        return super().get_invalid_login_error(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )