    
from django import forms
from .models import ProsedurM, AturanM, kegiatanM



# Form: Manajemen Prosedur
# ======================================================================================================================
class ProsedurF(forms.ModelForm):
    class Meta:
        model = ProsedurM
        fields = "__all__"

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if len(nama) < 5:
            raise forms.ValidationError("Nama Prosedur harus lebih dari 5 karakter.")
        return nama

    def clean_file_upload(self):
        file = self.cleaned_data.get('file_upload')
        if file:
            if file.size > 10 * 1024 * 1024:  # Limit file size to 10 MB
                raise forms.ValidationError("Ukuran file terlalu besar, maksimal 10 MB.")
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("File harus berformat PDF.")
        return file

# Form: Manajemen Aturan
# ======================================================================================================================

class AturanF(forms.ModelForm):
    class Meta:
        model = AturanM
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

    # Validasi untuk memastikan judul unik
    def clean_judul(self):
        judul = self.cleaned_data.get("judul")
        if AturanM.objects.filter(judul=judul).exists():
            raise forms.ValidationError("Judul ini sudah digunakan, silakan pilih judul lain.")
        return judul

    # Validasi tambahan untuk kategori
    def clean_kategori(self):
        kategori = self.cleaned_data.get("kategori")
        valid_categories = ['Legal', 'Recruitment', 'Training', 'Wellfare', 'Attendance']
        if kategori not in valid_categories:
            raise forms.ValidationError("Kategori yang dipilih tidak valid.")
        return kategori

    # Validasi ukuran file
    def clean_file_pdf(self):
        file_pdf = self.cleaned_data.get('file_pdf')
        if file_pdf:
            if file_pdf.size > 5 * 1024 * 1024:  # Ukuran file tidak boleh lebih dari 5MB
                raise forms.ValidationError("Ukuran file tidak boleh lebih dari 5MB.")
            if not file_pdf.name.endswith('.pdf'):
                raise forms.ValidationError("File harus dalam format PDF.")
        return file_pdf

    # Validasi deskripsi
    def clean_deskripsi(self):
        deskripsi = self.cleaned_data.get('deskripsi')
        if len(deskripsi) < 10:
            raise forms.ValidationError("Deskripsi harus lebih dari 10 karakter.")
        return deskripsi


# Form: Search Query
# ======================================================================================================================
class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )


# Form: Manajemen Kegiatan
# ======================================================================================================================
class kegiatanF(forms.ModelForm):
    class Meta:
        model = kegiatanM
        fields = ['image', 'judulKegiatan', 'deskripsi', 'tanggal']
        
    def __init__(self, *args, **kwargs):
        super(kegiatanF, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'