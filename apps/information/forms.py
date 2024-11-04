from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileField
import os
from .models import JadwalBusM, PengumumanM, MenuKantinM, Grafik, MenuShift, GrafikDept

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
    
    

class MenuShiftForm(forms.ModelForm):   
    class Meta:
        model = MenuShift
        fields = ['tanggal', 'shift_1', 'shift_2', 'shift_3']
        widgets = {
            'tanggal': forms.DateInput(attrs={'class': 'form-control'}),
            'shift_1': forms.Textarea(attrs={'class': 'form-control'}),
            'shift_2': forms.Textarea(attrs={'class': 'form-control'}),
            'shift_3': forms.Textarea(attrs={'class': 'form-control'}),
        }




# ======================================================================================================================
# Forms: Manajemen Indexs Kehadiran
# ======================================================================================================================

class GrafikForm(forms.ModelForm):
    class Meta:
        model = Grafik
        fields = ['nama', 'januari', 'februari', 'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'november', 'desember']



class GrafikDeptForm(forms.ModelForm):
    class Meta:
        model = GrafikDept
        fields = [
            'nama',
            'prod_preparation_aluminium', 'prod_preparation_steel',
            'head_cylinder_piston_production_ged3', 'gear_axle_production_ged4',
            'crank_shaft_production_ged5', 'quality_assurance', 'finance',
            'die_casting_wheel_gedung2', 'tools_center', 'plant_2_production',
            'production_engineering_aluminium_1', 'machining_painting_wheel_gedung1',
            'purchasing', 'mtc_operation', 'quality_engineering', 'quality_control', 'hrd',
            'general_affairs', 'gravity_die_casting_wheel_gd6', 'quality_safety_environment_qse',
            'production_engineering_aluminium_2', 'mtc_engineering', 'value_innovation',
            'production_engineering_steel_2', 'production_common', 'production_planning',
            'inventory_control', 'production_delivery_control', 'production_engineering_steel_1'
        ]
