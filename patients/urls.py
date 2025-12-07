from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.patient_search, name='patient_search'),
]