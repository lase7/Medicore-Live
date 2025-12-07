from django.urls import path
from . import views

urlpatterns = [
    # This matches the link in your button: {% url 'analyze_patient' patient.id %}
    path('analyze/<int:patient_id>/', views.analyze_patient, name='analyze_patient'),
]