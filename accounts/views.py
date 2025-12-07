from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def role_based_redirect(request):
    """
    Redirects users based on their Role.
    """
    user = request.user

    if user.is_superuser or user.role == 'DOCTOR':
        return redirect('doctor_dashboard')
    elif user.role == 'PATIENT':
        return redirect('patient_portal')
    else:
        # Fallback for users with no role
        return redirect('login')