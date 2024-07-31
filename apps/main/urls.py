from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # =============================
    # URL Configuration for Prosedur
    # =============================
    path('list_prosedur/', views.daftar_prosedur, name='daftar_prosedur'),
    path('create_prosedur/', views.buat_prosedur, name='buat_prosedur'),
    path('update_prosedur/<int:prosedur_id>/', views.ubah_prosedur, name='ubah_prosedur'),
    path('delete_prosedur/<int:prosedur_id>/', views.hapus_prosedur, name='hapus_prosedur'),
    path('download_prosedur/<int:prosedur_id>/', views.unduh_file_prosedur, name='unduh_file_prosedur'),
]

