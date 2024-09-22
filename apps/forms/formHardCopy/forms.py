from django import forms
from ..models import FormHardcopy

class FormHardcopyForm(forms.ModelForm):
    class Meta:
        model = FormHardcopy
        fields = "__all__"
        widgets = {
            'category_form': forms.Select(choices=FormHardcopy.CATEGORY_CHOICES)
        }
