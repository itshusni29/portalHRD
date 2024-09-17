
from django.db import models
from django.utils import timezone

# Model: Manajemen Prosedur
# ======================================================================================================================
class ProsedurM(models.Model):
    nama = models.CharField(max_length=100)
    kategori = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/prosedur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

# Model: Manajemen Aturan
# ======================================================================================================================
class AturanM(models.Model):
    judul = models.CharField(max_length=255)
    kategori = models.CharField(max_length=30)
    deskripsi = models.TextField(blank=True, null=True)
    file_pdf = models.FileField(upload_to="uploads/aturan/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul

# Model: Manajemen Visitor Log
# ======================================================================================================================
class Visitor(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"

    
 # Model: Manajemen Kegiatan
# ======================================================================================================================   
class kegiatanM(models.Model):
    judulKegiatan = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', default='a.jpg')
    deskripsi = models.TextField()
    tanggal = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judulKegiatan