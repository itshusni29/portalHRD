from django.urls import path, include

urlpatterns = [
    path('form_hard_copy/', include('apps.forms.formHardCopy.urls', namespace='formHardCopy')),  # Include URLs from formHardCopy
    path('sumbangan/', include('apps.forms.sumbangan.urls')),  # Include URLs from sumbangan if needed
]
