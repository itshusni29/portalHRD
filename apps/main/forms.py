

from django import forms
from .models import Prosedur



# =============================
# Forms: Manajemen Prosedur
# =============================
class ProsedurForm(forms.ModelForm):
    class Meta:
        model = Prosedur
        fields = "__all__"
