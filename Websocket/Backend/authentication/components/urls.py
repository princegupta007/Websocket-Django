from django.urls import path
from .views import create_admin, create_user, DashboardView


urlpatterns = [
    path('create_admin/', create_admin, name='create_admin'),
    path('create_user/', create_user, name='create_user'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),


]