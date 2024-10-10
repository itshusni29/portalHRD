from django.urls import path
from .views import (
    request_training_list,
    request_training_user,
    create_training,
    fetch_user_details,
    manager_training_list,
    gm_training_list,
    hrd_training_list,  
    admin_request_training_list,
    admin_request_training_view,
    admin_delete_training,
)

app_name = 'permintaan_training'

urlpatterns = [
    path('list', request_training_list, name='request_training_list'), # This is the URL for the public list view
    path('admin/lists', admin_request_training_list, name='admin_request_training_list'), # This is the URL for the admin list view
    path('create', request_training_user, name='request_training_user'), # This is the URL for create training form
    path('admin/create', create_training, name='create_training'),
    path('fetch_user_details', fetch_user_details, name='fetch_user_details'), # This is the URL for fetching user details
    path('manager/approval/list', manager_training_list, name='manager_request_training_list'), # This is the URL for the manager list view and approval
    path('gm/approval/list', gm_training_list, name='gm_request_training_list'), # This is the URL for the GM list view and approval
    path('manager_hrd/approval/list', hrd_training_list, name='hrd_request_training_list'),  # This is the URL for the HRD Manager list view and approval
    path('admin/request_training/<int:training_id>/', admin_request_training_view, name='admin_request_training_view'), # This is the URL for the admin view
    path('trainings/<int:training_id>/delete/', admin_delete_training, name='admin_delete_training'), # This is the URL for the admin delete view

]

