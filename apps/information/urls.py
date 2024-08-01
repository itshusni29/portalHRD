

from django.urls import path
from . import views


app_name = 'information'



urlpatterns = [
    path('kehadiran/', views.kehadiran, name='kehadiran'),
    # ======================================================================================================================
    # URL Configuration for Jadwal Bus
    # ======================================================================================================================
    path('pengumuman/', views.pengumuman_list, name='pengumuman_list'),
    path('pengumuman/create/', views.pengumuman_create, name='pengumuman_create'),
    path('pengumuman/update/<int:pk>/', views.pengumuman_update, name='pengumuman_update'),
    path('pengumuman/delete/<int:pk>/', views.pengumuman_delete, name='pengumuman_delete'),
    path('pengumuman/download/<int:pengumuman_id>/', views.file_pengumuman_download, name='file_pengumuman_download'),
    
    # ======================================================================================================================
    # URL Configuration for Jadwal Bus
    # ======================================================================================================================
    path('jadwal_bus/', views.jadwal_bus, name='jadwal_bus_list'),
    path('jadwal_bus/create/', views.jadwal_bus_create, name='jadwal_bus_create'),
    path('jadwal_bus/update/<int:pk>/', views.jadwal_bus_update, name='jadwal_bus_update'),
    path('jadwal_bus/delete/<int:pk>/', views.jadwal_bus_delete, name='jadwal_bus_delete'),
]
