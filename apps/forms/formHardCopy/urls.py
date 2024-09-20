from django.urls import path
from . import views

app_name = 'formHardCopy'  # Define the app name

urlpatterns = [
    path('', views.form_list, name='form_hard_copy_list'),
    path('dashboard/', views.form_list_admin, name='form_hard_copy_admin_list'),
    path('dashboard/create/', views.form_create, name='form_hard_copy_create'),
    path('dashboard/<int:pk>/update/', views.form_update, name='form_hard_copy_update'),
    path('dashboard/<int:pk>/delete/', views.form_delete, name='form_hard_copy_delete'),
    path('dashboard/<int:form_id>/download/', views.download_file, name='form_hard_copy_download'),
]
