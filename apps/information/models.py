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
    nama_file = models.CharField(max_length=35)
    file = models.FileField(upload_to="uploads/menuKantin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nama_file)
    

class MenuShift(models.Model):
    tanggal = models.DateField()
    shift_1 = models.TextField()  # Changed to TextField
    shift_2 = models.TextField()  # Changed to TextField
    shift_3 = models.TextField()  # Changed to TextField

    def __str__(self):
        return f"{self.tanggal} - {self.shift_1}, {self.shift_2}, {self.shift_3}"




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


class GrafikDept(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Name")

    # Adding verbose_name for each department to make them more readable
    prod_preparation_aluminium = models.FloatField(null=True, blank=True, verbose_name="Prod Preparation Aluminium")
    prod_preparation_steel = models.FloatField(null=True, blank=True, verbose_name="Prod Preparation Steel")
    head_cylinder_piston_production_ged3 = models.FloatField(null=True, blank=True, verbose_name="Head Cylinder & Piston Production - GED #3")
    gear_axle_production_ged4 = models.FloatField(null=True, blank=True, verbose_name="Gear Axle Production - GED #4")
    crank_shaft_production_ged5 = models.FloatField(null=True, blank=True, verbose_name="Crank Shaft Production - GED #5")
    quality_assurance = models.FloatField(null=True, blank=True, verbose_name="Quality Assurance")
    finance = models.FloatField(null=True, blank=True, verbose_name="Finance")
    die_casting_wheel_gedung2 = models.FloatField(null=True, blank=True, verbose_name="Die Casting Wheel - Gedung #2")
    tools_center = models.FloatField(null=True, blank=True, verbose_name="Tools Center")
    plant_2_production = models.FloatField(null=True, blank=True, verbose_name="Plant-2 Production")
    production_engineering_aluminium_1 = models.FloatField(null=True, blank=True, verbose_name="Production Engineering Aluminium #1")
    machining_painting_wheel_gedung1 = models.FloatField(null=True, blank=True, verbose_name="Machining & Painting Wheel - Gedung #1")
    purchasing = models.FloatField(null=True, blank=True, verbose_name="Purchasing")
    mtc_operation = models.FloatField(null=True, blank=True, verbose_name="MTC Operation")
    quality_engineering = models.FloatField(null=True, blank=True, verbose_name="Quality Engineering")
    quality_control = models.FloatField(null=True, blank=True, verbose_name="Quality Control")
    hrd = models.FloatField(null=True, blank=True, verbose_name="HRD")
    general_affairs = models.FloatField(null=True, blank=True, verbose_name="General Affairs")
    gravity_die_casting_wheel_gd6 = models.FloatField(null=True, blank=True, verbose_name="Gravity & Die Casting Wheel - GD #6")
    quality_safety_environment_qse = models.FloatField(null=True, blank=True, verbose_name="Quality, Safety & Environment (QSE)")
    production_engineering_aluminium_2 = models.FloatField(null=True, blank=True, verbose_name="Production Engineering Aluminium #2")
    mtc_engineering = models.FloatField(null=True, blank=True, verbose_name="MTC Engineering")
    value_innovation = models.FloatField(null=True, blank=True, verbose_name="Value Innovation")
    production_engineering_steel_2 = models.FloatField(null=True, blank=True, verbose_name="Production Engineering Steel #2")
    production_common = models.FloatField(null=True, blank=True, verbose_name="Production Common")
    production_planning = models.FloatField(null=True, blank=True, verbose_name="Production Planning")
    inventory_control = models.FloatField(null=True, blank=True, verbose_name="Inventory Control")
    production_delivery_control = models.FloatField(null=True, blank=True, verbose_name="Production & Delivery Control")
    production_engineering_steel_1 = models.FloatField(null=True, blank=True, verbose_name="Production Engineering Steel #1")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.nama

