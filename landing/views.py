from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Eventually we will return a proper HTML template.
    # For now, let's just return a simple security check.
    return HttpResponse("""
        <div style='font-family: sans-serif; text-align: center; padding: 50px;'>
            <h1 style='color: #2c3e50;'>MediCore MHR System</h1>
            <p style='color: #27ae60;'>✔ Secure Environment Active</p>
            <p>System Status: <strong>Operational</strong></p>
        </div>
    """)
