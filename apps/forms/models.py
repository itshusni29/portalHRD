from django.db import models


# Form model for hardcopy
class FormHardcopy(models.Model):
    id = models.AutoField(primary_key=True)
    nama_form = models.CharField(max_length=100)
    no_form = models.CharField(max_length=51)
    category_form = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.nama_form
    
    
    
class Sumbangan(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"
