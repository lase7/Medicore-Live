from django.urls import path
from . import views

urlpatterns = [
    path('analyze/<int:patient_id>/', views.analyze_patient, name='analyze_patient'),
]
