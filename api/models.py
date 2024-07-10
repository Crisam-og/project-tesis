from django.db import models
from django.db import models
from crum import get_current_request
from datetime import datetime
from django.forms.models import model_to_dict

from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_client = models.BooleanField(default=False)

    def get_group_session(self):
        try:
            request = get_current_request()
            if request is None:
                raise Exception("No current request found")

            groups = self.groups.all()
            print(f"Groups for user {self.username}: {groups}")

            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0].id # Guardar el ID del grupo
                    print(f"Group set in session: {request.session['group']}")
                    return groups[0]
                else:
                    print(f"Group already in session: {request.session['group']}")
                    group_id = request.session['group']
                    group = groups.get(id=group_id)
                    return group
            else:
                print(f"No groups found for user {self.username}")
                return None
        except Exception as e:
            print(f"Error in get_group_session: {e}")
            return None 

# class Client(CustomUser):
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         verbose_name = 'Client'
#         verbose_name_plural = 'Clients'

class Distrito(models.Model):
    nombre_distrito = models.CharField(max_length=50,unique=True)

class Reporte(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='reportes/', null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    lat = models.FloatField()
    long = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        fila = self.cliente.nombre
        return fila
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente_id'] = self.cliente_id.toJSON()
        item['distrito_id'] = self.distrito_id.toJSON()

        return item


