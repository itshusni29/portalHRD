

from django.db import models




# =============================
# Models: Manajemen Prosedur
# =============================
class Prosedur(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    kategori = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    file_upload = models.FileField(upload_to="uploads/prosedur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
