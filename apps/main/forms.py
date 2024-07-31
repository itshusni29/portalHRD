

from django import forms
from .models import Prosedur, Aturan



# =============================
# Forms: Manajemen Prosedur
# =============================
class ProsedurForm(forms.ModelForm):
    class Meta:
        model = Prosedur
        fields = "__all__"


# =============================
# Forms: Manajemen Prosedur
# =============================
class AturanForm(forms.ModelForm):
    # Form untuk input dan editing data Aturan
    class Meta:
        model = Aturan
        fields = ["judul", "kategori", "deskripsi", "file_pdf"]
        widgets = {
            'deskripsi': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'judul': 'Judul Aturan',
            'kategori': 'Kategori',
            'deskripsi': 'Deskripsi',
            'file_pdf': 'File PDF',
        }
