from patients.views import doctor_dashboard, patient_detail, patient_portal
from django.contrib import admin
from django.urls import path, include  # <--- Added 'include' here
from patients.views import doctor_dashboard, patient_detail
from gemmacare.views import chat_with_gemma

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard & Patient Views
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/<int:patient_id>/', patient_detail, name='patient_detail'),
    
    # AI Chat API
    path('api/gemmacare/chat/', chat_with_gemma, name='gemma_chat'),

    # Payment URLs (The Missing Link!)
    path('payments/', include('payments.urls')), 

    # ... other paths ...
    path('portal/', patient_portal, name='patient_portal'),

    path('accounts/', include('accounts.urls')),

]
