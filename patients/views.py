from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PatientRecord

# --- 1. DEFINE THE CHECK HERE ---
def is_doctor_or_admin(user):
    """
    Returns True if the user is a registered Doctor OR a Superuser.
    If False, they are blocked from the dashboard.
    """
    return user.is_authenticated and (user.role == 'DOCTOR' or user.is_superuser)

# --- 2. APPLY THE CHECK HERE ---
@login_required
@user_passes_test(is_doctor_or_admin, login_url='login') # <--- This applies the check
def doctor_dashboard(request):
    query = request.GET.get('q')
    patients = []

    if query:
        # Smart Search: Check if query has numbers (Date) or just text (Name)
        if any(char.isdigit() for char in query):
            patients = PatientRecord.objects.filter(
                Q(full_name__icontains=query) | 
                Q(date_of_birth__icontains=query)
            ).order_by('-created_at')
        else:
            patients = PatientRecord.objects.filter(
                full_name__icontains=query
            ).order_by('-created_at')

    context = {
        'patients': patients,
        'search_query': query
    }
    return render(request, 'patients/doctor_dashboard.html', context)

# --- 3. OTHER VIEWS (Keep these as they were) ---

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(PatientRecord, id=patient_id)
    
    # Check if invoice relation exists to avoid crashes
    try:
        invoices = patient.invoices.all().order_by('-issued_date')
    except AttributeError:
        invoices = []

    context = {
        'patient': patient,
        'invoices': invoices,
    }
    return render(request, 'patients/patient_detail.html', context)

@login_required
def patient_portal(request):
    # Ensure only patients can see this
    if getattr(request.user, 'role', '') != 'PATIENT':
        return redirect('doctor_dashboard') # Send doctors away from portal

    try:
        patient_record = request.user.medical_profile
        invoices = patient_record.invoices.all().order_by('-issued_date')
        
        context = {
            'patient': patient_record,
            'invoices': invoices
        }
        return render(request, 'patients/patient_portal.html', context)
        
    except Exception as e:
        return render(request, 'patients/patient_portal.html', {'error': "Medical Record Not Linked."})