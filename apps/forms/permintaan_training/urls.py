from django.urls import path
from .views import (
    request_training_list,
    admin_request_training_list,
    request_training_user,
    create_training,
    fetch_user_details,
    manager_training_list,
    gm_training_list,
    hrd_training_list,  # Updated URL for HRD approval
)

app_name = 'permintaan_training'

urlpatterns = [
    path('request_training/', request_training_list, name='request_training_list'),
    path('dashboard/request_training/', admin_request_training_list, name='admin_request_training_list'),
    path('request_training_user/', request_training_user, name='request_training_user'),
    path('dashboard/create_training/', create_training, name='create_training'),
    path('fetch_user_details/', fetch_user_details, name='fetch_user_details'),
    path('dashboard/list_form_request_training_manager', manager_training_list, name='manager_request_training_list'),
    path('dashboard/list_form_request_training_gm', gm_training_list, name='gm_request_training_list'),
    path('dashboard/list_form_request_training_hrd', hrd_training_list, name='hrd_request_training_list'),  # HRD approval URL
]
