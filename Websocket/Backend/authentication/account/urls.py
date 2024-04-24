# from django.urls import path
# from .views import UserCreateView, CustomTokenObtainPairView,CustomTokenRefreshView

# urlpatterns = [
#     path('register/', UserCreateView.as_view(), name='register'),
#     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

# ]











# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import UserCreateView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    
]
