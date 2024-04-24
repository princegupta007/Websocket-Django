# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email', 'password', 'user_type')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(**validated_data)
#         return user

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')

#         if username and password:
#             user = authenticate(username=username, password=password)

#             if user:
#                 if not user.is_active:
#                     raise serializers.ValidationError("User account is disabled.")
#                 refresh = RefreshToken.for_user(user)
#                 return {
#                     'user_id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                     'user_type': user.user_type,
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }
#             else:
#                 raise serializers.ValidationError("Unable to login with provided credentials.")
#         else:
#             raise serializers.ValidationError("Must include 'username' and 'password'.")


# class RefreshTokenSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     def validate(self, attrs):
#         refresh = attrs.get('refresh')

#         if refresh:
#             try:
#                 refresh_token = RefreshToken(refresh)
#                 refresh_token.verify()
#                 return {
#                     'access': str(refresh_token.access_token),
#                 }
#             except TokenError:
#                 raise serializers.ValidationError("Invalid token")
#         else:
#             raise serializers.ValidationError("Must include 'refresh' token.")


















# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'user_type', 'parent_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                refresh = RefreshToken.for_user(user)
                return {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                    'parent_admin': user.parent_admin_id,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get('refresh')

        if refresh:
            try:
                refresh_token = RefreshToken(refresh)
                refresh_token.verify()
                return {
                    'access': str(refresh_token.access_token),
                }
            except TokenError:
                raise serializers.ValidationError("Invalid token")
        else:
            raise serializers.ValidationError("Must include 'refresh' token.")
