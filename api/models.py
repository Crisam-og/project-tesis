from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_client = models.BooleanField(default=False)

# class Client(CustomUser):
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         verbose_name = 'Client'
#         verbose_name_plural = 'Clients'

# class Distrito(models.Model):
#     nombre_distrito = models.CharField(max_length=50)
        
# class Reporte(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     fecha = models.DateField()
#     descripcion = models.TextField()
    