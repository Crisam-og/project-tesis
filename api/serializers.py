from rest_framework import serializers
from .models import User, Distrito, Reporte
from django.utils.text import slugify

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nombre','apellidos','email', 'password', 'phone_number', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Generar username único basado en el correo electrónico
        username = slugify(validated_data['email'].split('@')[0])

        user = User(
            username=username,
            nombre=validated_data['nombre'],
            apellidos=validated_data['apellidos'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            is_client=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = ['id', 'nombre_distrito']

class ReporteSerializer(serializers.ModelSerializer):
    cliente = ClientSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='cliente'
    )
    distrito = DistritoSerializer(read_only=True)
    distrito_id = serializers.PrimaryKeyRelatedField(
        queryset=Distrito.objects.all(),
        write_only=True,
        source='distrito'
    )

    class Meta:
        model = Reporte
        fields = ['id', 'cliente', 'cliente_id', 'imagen', 'descripcion', 'direccion', 
                  'distrito', 'distrito_id', 'lat', 'long', 'created_at']

    def create(self, validated_data):
        return Reporte.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance