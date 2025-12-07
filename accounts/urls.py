from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The Login Page
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    # The Logout Action (Redirects back to login)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # The Traffic Controller (Where they go after login)
    path('redirect/', views.role_based_redirect, name='role_redirect'),
]