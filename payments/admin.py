from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'amount', 'status', 'issued_date')
    list_filter = ('status', 'issued_date')
    search_fields = ('patient__full_name',)