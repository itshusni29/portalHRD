# apps/forms/sumbangan/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.sumbangan_create, name='sumbangan_create'),
    path('list-all/', views.sumbangan_list, name='list-all'),
]
