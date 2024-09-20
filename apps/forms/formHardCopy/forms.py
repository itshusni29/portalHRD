from django import forms
from ..models import FormHardcopy

# Form for FormHardcopy model
class FormHardcopyForm(forms.ModelForm):
    class Meta:
        model = FormHardcopy
        fields = "__all__"
