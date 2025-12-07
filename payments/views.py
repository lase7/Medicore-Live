import requests
import uuid
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # <--- ADD THIS HERE
from .models import Invoice

def create_checkout_session(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # 1. Talk to Flutterwave API
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    # 2. Build the transaction
    tx_ref = str(uuid.uuid4())
    data = {
        "tx_ref": tx_ref,
        "amount": str(invoice.amount),
        "currency": "NGN",
        "redirect_url": f"http://127.0.0.1:8000/payments/verify/{invoice_id}/",
        "customer": {
            "email": "patient@medicore.com", # In production, use invoice.patient.user.email
            "name": invoice.patient.full_name,
            "phonenumber": "08012345678"
        },
        "customizations": {
            "title": "MediCore Hospital Bill",
            "logo": "https://cdn-icons-png.flaticon.com/512/2966/2966327.png"
        }
    }

    try:
        # 3. Send Request
        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()

        if res_data['status'] == 'success':
            return redirect(res_data['data']['link']) # Go to Flutterwave
        else:
            return render(request, 'patients/doctor_dashboard.html', {'error': 'Flutterwave connection failed'})

    except Exception as e:
        return render(request, 'patients/doctor_dashboard.html', {'error': str(e)})

def verify_payment(request, invoice_id):
    """
    Flutterwave sends the user back here after payment.
    """
    status = request.GET.get('status')
    transaction_id = request.GET.get('transaction_id')

    if status == 'successful' and transaction_id:
        # Double check with server
        url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
        headers = {"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"}
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        if res_data['status'] == 'success':
            # Mark Invoice as PAID
            invoice = get_object_or_404(Invoice, id=invoice_id)
            invoice.status = 'PAID'
            invoice.save()
            messages.success(request, "Payment Successful!")
            return redirect('patient_detail', patient_id=invoice.patient.id)

    messages.error(request, "Payment Failed.")
    return redirect('patient_detail', patient_id=Invoice.objects.get(id=invoice_id).patient.id)
# patients/views.py

# In patients/views.py

@login_required
def patient_portal(request):
    if getattr(request.user, 'role', '') != 'PATIENT':
        return render(request, 'landing/index.html', {'error': "Access Denied."})

    try:
        patient_record = request.user.medical_profile
        invoices = patient_record.invoices.all().order_by('-issued_date')
        
        context = {
            'patient': patient_record,
            'invoices': invoices
        }
        return render(request, 'patients/patient_portal.html', context)
        
    except Exception as e:
        # FIX: Render the PORTAL template (not base) so we see the error message
        return render(request, 'patients/patient_portal.html', {'error': "No medical record linked to this account. Please contact the hospital."})