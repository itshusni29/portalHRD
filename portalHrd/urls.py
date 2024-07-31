"""
URL configuration for portalHrd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# =============================
# Project URL Configuration
# =============================

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),  # URL untuk aplikasi utama
    path('user/', include('apps.user.urls')),  # URL untuk aplikasi user
    # =============================
    # Project URL forms
    # =============================
    path('sumbangan/', include('apps.forms.sumbangan.urls')),  # URL untuk aplikasi sumbangan
    path('prosedur/', include('apps.main.urls')),  # Pastikan URL di sini sesuai dengan aplikasi prosedur
    path('information/', include('apps.information.urls')),  # URL untuk aplikasi information

]
