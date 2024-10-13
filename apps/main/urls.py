from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('tim_kami/', views.timKami, name='tim_kami'),
    path('kontak/', views.kontak, name='kontak'),
    path('search/', views.search, name='search_results'),
    path('<str:model_type>/<int:pk>/', views.formmodel_detail, name='formmodel_detail'),
    
    # URL Configuration for Prosedur
    # ======================================================================================================================
    path('dashboard/list_prosedur/',views.admin_prosedur, name='admin_prosedur'),
    path('list_prosedur/', views.daftar_prosedur, name='daftar_prosedur'),
    path('dashboard/create_prosedur/', views.buat_prosedur, name='buat_prosedur'),
    path('dashboard/update_prosedur/<int:prosedur_id>/', views.ubah_prosedur, name='ubah_prosedur'),
    path('dashboard/delete_prosedur/<int:prosedur_id>/', views.hapus_prosedur, name='hapus_prosedur'),
    path("prosedur/<int:pk>/unduh/", views.unduh_file_prosedur, name="prosedur_download"),

    # URL Patterns: Aturan
    # ======================================================================================================================
    path('dashboard/list_aturan/', views.admin_aturan, name='admin_aturan'),
    path("aturan/", views.daftar_aturan, name="aturan_list"),
    path("dashboard/aturan/tambah/", views.buat_aturan, name="aturan_create"),
    path("dashboard/aturan/<int:pk>/edit/", views.ubah_aturan, name="aturan_edit"),
    path("dashboard/aturan/<int:pk>/hapus/", views.hapus_aturan, name="aturan_delete"),
    path("aturan/<int:pk>/unduh/", views.unduh_file_aturan, name="aturan_download"),
    
    # URL Patterns: Kegiatan
    # ======================================================================================================================
    path('dashboard/list_kegiatan/', views.admin_kegiatan, name='admin_kegiatan'),
    path('kegiatan/', views.list_kegiatan, name='list_kegiatan'),
    path('dashboard/kegiatan/tambah/', views.Create_kegiatan, name='upload_kegiatan'),
    path('dashboard/kegiatan/<int:id>/edit/', views.Update_kegiatan, name='edit_kegiatan'),
    path('dashboard/kegiatan/<int:id>/delete/', views.Delete_kegiatan, name='delete_kegiatan'),
    
    # URL Patterns: Banner Management
    # ======================================================================================================================
    path('dashboard/list_banner/', views.admin_banner, name='admin_banner'),
    path('dashboard/banner/tambah/', views.create_banner, name='create_banner'),
    path('dashboard/banner/<int:id>/edit/', views.update_banner, name='update_banner'),
    path('dashboard/banner/<int:id>/delete/', views.delete_banner, name='delete_banner'),


]

