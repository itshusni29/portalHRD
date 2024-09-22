from django.urls import path, include

urlpatterns = [
    path('form_hard_copy/', include('apps.forms.formHardCopy.urls', namespace='formHardCopy')),
    path('sumbangan/', include('apps.forms.sumbangan.urls')),
    path('permintaan_training/', include('apps.forms.permintaan_training.urls', namespace='permintaan_training')),  # Corrected namespace
]
