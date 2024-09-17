from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileField
import os
from .models import JadwalBusM, PengumumanM, MenuKantinM, Grafik

# ======================================================================================================================
# Forms: Manajemen Jadwal Bus
# ======================================================================================================================
class JadwalBusF(forms.ModelForm):
    # Form untuk model JadwalBusM.
    class Meta:
        model = JadwalBusM
        fields = "__all__"

# ======================================================================================================================
# Forms: Manajemen Pengumuman
# ======================================================================================================================
class PengumumanF(forms.ModelForm):
    # Form untuk model Pengumuman.
    class Meta:
        model = PengumumanM
        fields = "__all__"
        widgets = {
            'created_at': forms.TextInput(attrs={'type': 'date'}),
        }

# ======================================================================================================================
# Forms: Manajemen Menu Kantin
# ======================================================================================================================
def validate_file_extension(value):
    # Validasi ekstensi file untuk MenuKantinF
    allowed_extensions = [".xlsx", ".csv"]
    file_extension = os.path.splitext(value.name)[1]

    if file_extension not in allowed_extensions:
        raise ValidationError("Only XLSX or CSV files are allowed.")

class MenuKantinF(ModelForm):
    # Form untuk model MenuKantinM
    file = FileField(validators=[validate_file_extension])

    class Meta:
        model = MenuKantinM
        fields = "__all__"


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search')



# ======================================================================================================================
# Forms: Manajemen Indexs Kehadiran
# ======================================================================================================================

class GrafikForm(forms.ModelForm):
    class Meta:
        model = Grafik
        fields = ['nama', 'januari', 'februari', 'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'november', 'desember']

