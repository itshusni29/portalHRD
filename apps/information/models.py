

from django.db import models


# =============================
# Models: Manajemen Jadwal Bus
# =============================
class JadwalBusM(models.Model):
    # Model untuk menangani data jadwal bus.
    id = models.AutoField(primary_key=True)
    titik_start = models.CharField(max_length=30)
    plant = models.CharField(max_length=2)
    via = models.TextField(max_length=255)
    seat = models.IntegerField()
    shift1 = models.CharField(max_length=5, null=True, blank=True)
    shift2 = models.CharField(max_length=5, null=True, blank=True)
    shift3 = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return str(self.titik_start)


# =============================
# Models: Manajemen Pengumuman
# =============================
class Pengumuman(models.Model):
    # Model untuk menangani data pengumuman
    id = models.AutoField(primary_key=True)
    nama_pengumuman = models.CharField(max_length=355)
    tahun = models.CharField(max_length=5)
    file_pengumuman = models.FileField(upload_to="uploads/pengumuman")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nama_pengumuman)
