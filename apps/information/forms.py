

from django import forms
from .models import JadwalBusM, PengumumanM, MenuKantinM


# ======================================================================================================================
# Forms: Manajemen Jadwal Bus
# ======================================================================================================================
class JadwalBusF(forms.ModelForm):
    # Form untuk model JadwalBusM.
    class Meta:
        model = JadwalBusM
        fields = "__all__"



# ======================================================================================================================
# Forms: Manajemen Jadwal Bus
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
    # Validasi ekstensi file untuk menuKantinF
    allowed_extensions = [".xlsx", ".csv"]
    file_extension = os.path.splitext(value.name)[1]

    if file_extension not in allowed_extensions:
        raise ValidationError("Only XLSX or CSV files are allowed.")


class MenuKantinF(ModelForm):
    # Form untuk model MenuKantinM

    file = FileField(validators=[validate_file_extension])

    class Meta:
        model = MenuKantinM