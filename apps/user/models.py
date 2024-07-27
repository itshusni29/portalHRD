from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    class Occupation(models.TextChoices):
        MANAGER = 'manager', 'Manager'
        GENERAL_MANAGER = 'general_manager', 'General Manager'
        DIRECTOR = 'director', 'Director'
        GENERAL_FOREMAN = 'general_foreman', 'General Foreman'
        STAFF = 'staff', 'Staff'
        OPERATOR = 'operator', 'Operator'

    class Department(models.TextChoices):
        HR = 'hr', 'Human Resources'
        IT = 'it', 'Information Technology'
        FINANCE = 'finance', 'Finance'
        SALES = 'sales', 'Sales'
        OTHER = 'other', 'Other'

    class Section(models.TextChoices):
        ADMINISTRATION = 'administration', 'Administration'
        DEVELOPMENT = 'development', 'Development'
        ACCOUNTING = 'accounting', 'Accounting'
        MARKETING = 'marketing', 'Marketing'
        SUPPORT = 'support', 'Support'
        OTHER = 'other', 'Other'

    base_role = Role.USER
    role = models.CharField(max_length=20, choices=Role.choices, default=base_role)
    occupation = models.CharField(max_length=20, choices=Occupation.choices, default=Occupation.STAFF)
    department = models.CharField(max_length=20, choices=Department.choices, default=Department.OTHER)
    section = models.CharField(max_length=20, choices=Section.choices, default=Section.OTHER)
    nik = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
