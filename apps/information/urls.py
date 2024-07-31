

from django.urls import path
from . import views

urlpatterns = [
    # =============================
    # URL Configuration for Jadwal Bus
    # =============================
    path('jadwal_bus/', views.jadwal_bus, name='jadwal_bus_list'),
    path('jadwal_bus/create/', views.jadwal_bus_create, name='jadwal_bus_create'),
    path('jadwal_bus/update/<int:pk>/', views.jadwal_bus_update, name='jadwal_bus_update'),
    path('jadwal_bus/delete/<int:pk>/', views.jadwal_bus_delete, name='jadwal_bus_delete'),
]
