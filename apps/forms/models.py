
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  



from django.db import models


# ======================================================================================================================
# Models: Manajemen Hard Copy
# ======================================================================================================================
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
    file_upload = models.FileField(upload_to="uploads/forms/all")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_form

    
    
# ======================================================================================================================
# Models: Manajemen Sumbangan
# ====================================================================================================================== 
class Sumbangan(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

# ======================================================================================================================
# Models: Manajemen Approval
# ====================================================================================================================== 
class GMApproval(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE, related_name='gm_approvals')  # Change the related_name
    approval_status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ManagerApproval(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE, related_name='manager_approvals')  # Change the related_name
    approval_status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HRDManagerApproval(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE, related_name='hrd_manager_approvals')  # Change the related_name
    approval_status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

# ======================================================================================================================
# Models: Manajemen Training Status
# ====================================================================================================================== 
class TrainingStatus(models.Model):
    STATUS_CHOICES = [
        ('submit', 'Submitted'),
        ('manager_approved', 'Approved by Manager'),
        ('manager_rejected', 'Rejected by Manager'),
        ('gm_approved', 'Approved by GM'),
        ('gm_rejected', 'Rejected by GM'),
        ('hrd_approved', 'Approved by HRD'),
        ('hrd_rejected', 'Rejected by HRD'),
        ('preparing', 'Preparing'),
        ('pending', 'Pending'),
        ('on_going', 'On Going'),
        ('canceled', 'Canceled by HRD'),
        ('evaluation', 'Evaluation'),
        ('monitoring', 'Monitoring'),
        ('completed', 'Completed'),
    ]
    training = models.ForeignKey('Training', on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', null=True)
    remarks = models.TextField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
# ======================================================================================================================
# Models: Manajemen request Training
# ====================================================================================================================== 
class Training(models.Model):
    LEVEL_CHOICES = [
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
    ]


    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requestor', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    background = models.TextField()
    participants = models.TextField(max_length=500)
    trainer = models.CharField(max_length=100)
    date = models.DateField()
    date_end = models.DateField()
    location = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    evaluation_level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    flyer = models.FileField(upload_to="uploads/forms/request_training")
   

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='manager_approvals', on_delete=models.CASCADE)
    gm = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='gm_approvals', on_delete=models.CASCADE)
    hrd_manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hrd_manager_approvals', on_delete=models.CASCADE)

    gm_approval = models.ForeignKey(GMApproval, on_delete=models.CASCADE, related_name='training_gm_approval', null=True, blank=True)
    manager_approval = models.ForeignKey(ManagerApproval, on_delete=models.CASCADE, related_name='training_manager_approval', null=True, blank=True)
    hrd_manager_approval = models.ForeignKey(HRDManagerApproval, on_delete=models.CASCADE, related_name='training_hrd_manager_approval', null=True, blank=True)
    training_status = models.ForeignKey(TrainingStatus, on_delete=models.CASCADE, related_name='trainings', null=True, blank=True)
    
    def __str__(self):
        return f"{self.topic} - {self.requestor.username}"
