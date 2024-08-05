from django.urls import path, include
from . import views


urlpatterns = [
    path('Form-list/', views.formList, name='formList'),  # URL Configuration for Form-list
    path('sumbangan/', include('apps.forms.sumbangan.urls')), # URL Configuration for sumbangan
]