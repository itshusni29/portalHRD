

from django.db import models




# =============================
# Models: Manajemen Prosedur
# =============================
class Prosedur(models.Model):
     # Model untuk menangani data Prosedur perusahaan.
    nama = models.CharField(max_length=100)
    kategori = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    file_upload = models.FileField(upload_to="uploads/prosedur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama



# =============================
# Models: Manajemen Aturan
# =============================

class Aturan(models.Model):
    # Model untuk menangani data aturan perusahaan.
    judul = models.CharField(max_length=255)
    kategori = models.CharField(max_length=30)
    deskripsi = models.TextField(blank=True, null=True)
    file_pdf = models.FileField(upload_to="uploads/aturan_pdfs/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul
