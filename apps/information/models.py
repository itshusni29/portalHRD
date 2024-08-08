from django.db import models

# ======================================================================================================================
# Models: Manajemen Jadwal Bus
# ======================================================================================================================
class JadwalBusM(models.Model):
    # Model untuk menangani data jadwal bus.
    titik_start = models.CharField(max_length=30)
    plant = models.CharField(max_length=2)
    via = models.TextField(max_length=255)
    seat = models.IntegerField()
    shift1 = models.CharField(max_length=5, null=True, blank=True)
    shift2 = models.CharField(max_length=5, null=True, blank=True)
    shift3 = models.CharField(max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.titik_start)

# ======================================================================================================================
# Models: Manajemen Pengumuman
# ======================================================================================================================
class PengumumanM(models.Model):
    # Model untuk menangani data pengumuman
    nama_pengumuman = models.CharField(max_length=355)
    tahun = models.CharField(max_length=5)
    file_pengumuman = models.FileField(upload_to="uploads/pengumuman")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nama_pengumuman)

# ======================================================================================================================
# Models: Manajemen Menu Kantin
# ======================================================================================================================
class MenuKantinM(models.Model):
    # Model for handling canteen menu data
    nama_menu = models.CharField(max_length=35)
    alamat_file = models.FileField(upload_to="uploads/menuKantin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nama_menu)


# ======================================================================================================================
# Models: Manajemen Indexs Kehadiran
# ======================================================================================================================

class Grafik(models.Model):
    nama = models.CharField(max_length=255)
    januari = models.FloatField()
    februari = models.FloatField()
    maret = models.FloatField()
    april = models.FloatField()
    mei = models.FloatField()
    juni = models.FloatField()
    juli = models.FloatField()
    agustus = models.FloatField()
    september = models.FloatField()
    oktober = models.FloatField()
    november = models.FloatField()
    desember = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
