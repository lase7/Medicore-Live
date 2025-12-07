from django.db import models
from patients.models import PatientRecord

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]

    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, default="Consultation Fee")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    issued_date = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.patient.full_name} ({self.status})"