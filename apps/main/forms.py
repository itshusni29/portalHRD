    
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
        fields = ['image', 'judulKegiatan', 'description', 'tanggal']
        
    def __init__(self, *args, **kwargs):
        super(kegiatanF, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'