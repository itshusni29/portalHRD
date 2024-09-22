

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  


# Form model for hardcopy
from django.db import models

class FormHardcopy(models.Model):
    CATEGORY_CHOICES = [
        ('HRA_IR', 'HRA & IR'),
        ('MEDICAL_WELFARE', 'Medical Welfare'),
        ('RECRUITMENT', 'Recruitment'),
        ('TRAINING', 'Training'),
    ]

    id = models.AutoField(primary_key=True)
    nama_form = models.CharField(max_length=100)
    no_form = models.CharField(max_length=51)
    category_form = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file_upload = models.FileField(upload_to="uploads/forms/request_training")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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



class Participant(models.Model):
    nik = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)  # Section of the participant
    cc = models.CharField(blank=True, max_length=255)  # Additional CC emails

    def __str__(self):
        return self.name

class Training(models.Model):
    LEVEL_CHOICES = [
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('manager_approved', 'Approved by Manager'),
        ('gm_approved', 'Approved by GM'),
        ('hrd_approved', 'Approved by HRD'),
        ('completed', 'Completed'),
        ('evaluation', 'Evaluation'),
        ('failed', 'Failed'),
        ('monitoring', 'Monitoring'),
    ]

    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requestor', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    background = models.TextField()
    target = models.CharField(max_length=200)
    participants = models.ManyToManyField(Participant)  # ManyToManyField for participants
    trainer = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    evaluation_level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    monitoring_type = models.CharField(max_length=100)
    monitoring_date = models.DateField()

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='manager_approvals', on_delete=models.CASCADE)
    gm = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='gm_approvals', on_delete=models.CASCADE)
    hrd_manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hrd_manager_approvals', on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.topic} - {self.requestor.username}"

class GMApproval(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='gm_approval')
    approval_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ManagerApproval(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='manager_approval')
    approval_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HRDManagerApproval(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='hrd_manager_approval')
    approval_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
