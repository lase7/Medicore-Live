from django.db import models
from django.conf import settings

class PatientRecord(models.Model):
    # Link to the User account (if they have portal access)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='medical_profile')
    
    # Emergency Data
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5, choices=[('A+', 'A+'), ('O+', 'O+'), ('B-', 'B-'), ('AB+', 'AB+')])
    allergies = models.TextField(help_text="Comma separated list of allergies")
    existing_conditions = models.TextField()
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.date_of_birth}"