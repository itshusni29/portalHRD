from django.urls import path
from .views import login_view, register_view, logout_view, create_user, user_list, edit_user, delete_user

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'), 
    path('dashboard/create_user/', create_user, name='create_user'),
    path('dashboard/user_list/', user_list, name='user_list'),
    path('dashboard/edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('dashboard/delete_user/<int:user_id>/', delete_user, name='delete_user'),
]
