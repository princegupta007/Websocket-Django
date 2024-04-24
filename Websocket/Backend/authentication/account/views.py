# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView
# from .models import CustomUser
# from .serializers import UserSerializer, LoginSerializer, RefreshTokenSerializer

# class UserCreateView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = RefreshTokenSerializer














# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer, RefreshTokenSerializer
from django.contrib.auth.hashers import make_password

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Manually hash the password before saving
        validated_data = serializer.validated_data
        password = validated_data['password']
        validated_data['password'] = make_password(password)
        serializer.save()

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer
