from django.urls import path
from . import views

app_name = 'information'

urlpatterns = [
   
    path('komite/', views.komite, name='komite'),
    # ======================================================================================================================
    # URL Configuration for Pengumuman
    # ======================================================================================================================
    path('dashboard/pengumuman/', views.admin_pengumuman, name='admin_pengumuman'),
    path('pengumuman/', views.pengumuman_list, name='pengumuman_list'),
    path('dashboard/pengumuman/create/', views.pengumuman_create, name='pengumuman_create'),
    path('dashboard/pengumuman/update/<int:pk>/', views.pengumuman_update, name='pengumuman_update'),
    path('dashboard/pengumuman/delete/<int:pk>/', views.pengumuman_delete, name='pengumuman_delete'),
    path('pengumuman/download/<int:pengumuman_id>/', views.file_pengumuman_download, name='file_pengumuman_download'),

    # ======================================================================================================================
    # URL Configuration for Jadwal Bus
    # ======================================================================================================================
    path('dashboard/jadwal_bus/', views.admin_jadwalbus, name='admin_jadwalbus'),
    path('jadwal_bus/', views.jadwal_bus, name='jadwal_bus_list'),
    path('dashboard/jadwal_bus/create/', views.jadwal_bus_create, name='jadwal_bus_create'),
    path('dashboard/jadwal_bus/update/<int:pk>/', views.jadwal_bus_update, name='jadwal_bus_update'),
    path('dashboard/jadwal_bus/delete/<int:pk>/', views.jadwal_bus_delete, name='jadwal_bus_delete'),

    # ======================================================================================================================
    # URL Configuration for Menu Kantin
    # ======================================================================================================================
    path('dashboard/menu_kantin/', views.admin_menukantin, name='admin_menukantin'),
    path('menu_kantin/', views.menuKantin, name='menuKantin'),
    path('dashboard/menu_kantin/upload/', views.upload_csv, name='upload_csv'),
    path('dashboard/menu_kantin/delete/<int:file_id>/', views.delete_csv, name='delete_csv'),
    
    # ======================================================================================================================
    # URL Configuration for Grafik
    # ======================================================================================================================
    path('kehadiran/', views.kehadiran, name='kehadiran'),
    path('dashboard/kehadiran/list', views.grafik_list, name='grafik_list'),
    path('dashboard/kehadiran/new/', views.grafik_create, name='grafik_create'),
    path('dashboard/kehadiran/<int:pk>/edit/', views.grafik_update, name='grafik_update'),
    path('dashboard/kehadiran/<int:pk>/delete/', views.grafik_delete, name='grafik_delete'),
]

