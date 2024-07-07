from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import User, Distrito


from .serializers import ClientSerializer, LoginSerializer, DistritoSerializer

class RegisterClientAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginClientAPIView(APIView):
   def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.check_password(password) and user.is_client:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'nombre': user.nombre,
                    'apellidos': user.apellidos,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'address': user.address,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DistritoAPIView(APIView):
    def get(self,request):
        distrito = Distrito.objects.all()
        serializer = DistritoSerializer(distrito, many = True)
        
        data = {
                'data' : serializer.data
                }
        return Response(data, status = status.HTTP_200_OK)
       

class RegisterDistritoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DistritoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Distrito registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)