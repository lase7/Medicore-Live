from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER_ADMIN = 'ADMIN', 'Super Admin'
        DOCTOR = 'DOCTOR', 'Doctor'
        PATIENT = 'PATIENT', 'Patient'

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.PATIENT)
    is_biometric_active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def is_doctor(self):
        return self.role == self.Roles.DOCTOR