from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:invoice_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('verify/<int:invoice_id>/', views.verify_payment, name='verify_payment'),
]