from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tim_kami/', views.timKami, name='tim_kami'),
    path('kontak/', views.kontak, name='kontak'),
    path('search/', views.search, name='search_results'),
    path('<str:model_type>/<int:pk>/', views.formmodel_detail, name='formmodel_detail'),
    
    # URL Configuration for Prosedur
    # ======================================================================================================================
    path('list_prosedur/', views.daftar_prosedur, name='daftar_prosedur'),
    path('create_prosedur/', views.buat_prosedur, name='buat_prosedur'),
    path('update_prosedur/<int:prosedur_id>/', views.ubah_prosedur, name='ubah_prosedur'),
    path('delete_prosedur/<int:prosedur_id>/', views.hapus_prosedur, name='hapus_prosedur'),
    path('download_prosedur/<int:prosedur_id>/', views.unduh_file_prosedur, name='unduh_file_prosedur'),
    
    # URL Patterns: Aturan
    # ======================================================================================================================
    path("aturan/", views.daftar_aturan, name="aturan_list"),
    path("aturan/tambah/", views.buat_aturan, name="aturan_create"),
    path("aturan/<int:pk>/edit/", views.ubah_aturan, name="aturan_edit"),
    path("aturan/<int:pk>/hapus/", views.hapus_aturan, name="aturan_delete"),
    path("aturan/<int:pk>/unduh/", views.unduh_file_aturan, name="aturan_download"),
    
    # URL Patterns: Kegiatan
    # ======================================================================================================================
    path('kegiatan/table', views.list_kegiatan_table, name='list_kegiatan_table'),
    path('kegiatan/', views.list_kegiatan, name='list_kegiatan'),
    path('kegiatan/tambah/', views.Create_kegiatan, name='upload_kegiatan'),
    path('kegiatan/<int:id>/edit/', views.Update_kegiatan, name='edit_kegiatan'),
    path('kegiatan/<int:id>/delete/', views.Delete_kegiatan, name='delete_kegiatan'),

]
