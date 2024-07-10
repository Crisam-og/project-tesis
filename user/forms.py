from django.forms import *
from api.models import *

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = User
        fields = ('nombre','apellidos', 'email','username', 'password', 'groups')
        exclude = ['image', 'is_staff', 'is_superuser', 'is_active', 'user_permissions', 'first_name', 'last_name']
        
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre',
                    
                    }
                ),
            'apellidos': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido',
                    
                    }
                ),
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un correo',
                    'tyoe': 'email'
                    
                    }
                ),
            'username': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el username',
                    
                    }
                ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido',
                    'tyoe': 'password',
                    
                    }
                ),
            'groups': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else: 
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data