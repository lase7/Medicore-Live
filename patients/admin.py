from django.contrib import admin
from .models import PatientRecord

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'blood_type', 'created_at')
    search_fields = ('full_name', 'emergency_contact_name')
    list_filter = ('blood_type',)