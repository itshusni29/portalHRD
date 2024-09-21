# apps/forms/permintaan_training/urls.py
from django.urls import path
from .views import create_training, training_list

urlpatterns = [
    path('create-training/', create_training, name='create_training'),  # URL for creating a training
    path('training-list/', training_list, name='training_list'),  # URL for the training list
]
