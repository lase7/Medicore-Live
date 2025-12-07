from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # This configures how the User list looks
    list_display = ['username', 'email', 'role', 'is_staff']
    
    # This adds our custom 'role' field to the edit page
    fieldsets = UserAdmin.fieldsets + (
        ('MediCore Roles', {'fields': ('role', 'phone_number', 'is_biometric_active')}),
    )
    
    # This allows you to edit these fields when creating a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'email')}),
    )