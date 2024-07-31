# apps/forms/sumbangan/forms.py

from django import forms
from apps.forms.models import Sumbangan

class SumbanganForm(forms.ModelForm):
    class Meta:
        model = Sumbangan
        fields = ['name', 'amount', 'message']
