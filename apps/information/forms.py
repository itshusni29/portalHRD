

from django import forms
from .models import JadwalBusM, Pengumuman


# =============================
# Forms: Manajemen Jadwal Bus
# =============================
class JadwalBusF(forms.ModelForm):
    # Form untuk model JadwalBusM.
    class Meta:
        model = JadwalBusM
        fields = "__all__"



# =============================
# Forms: Manajemen Jadwal Bus
# =============================

class PengumumanForm(forms.ModelForm):
    # Form untuk model Pengumuman.
    class Meta:
        model = Pengumuman
        fields = "__all__"
        widgets = {
            'created_at': forms.TextInput(attrs={'type': 'date'}),
        }
