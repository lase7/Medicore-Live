import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .services import query_gemmacare
from patients.models import PatientRecord

@csrf_exempt
@login_required
def chat_with_gemma(request):
    """
    API Endpoint handling the AJAX chat request.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            patient_id = data.get('patient_id')

            # 1. Retrieve Patient Context securely
            context = {}
            if patient_id:
                try:
                    patient = PatientRecord.objects.get(id=patient_id)
                    context = {
                        'full_name': patient.full_name,
                        'allergies': patient.allergies,
                        'conditions': patient.existing_conditions,
                        'blood_type': patient.blood_type
                    }
                except PatientRecord.DoesNotExist:
                    pass # Continue without context if ID is invalid

            # 2. Get AI Response
            # The service layer handles the prompt engineering
            ai_response = query_gemmacare(user_message, context)
            
            return JsonResponse({'response': ai_response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # In production, you would log this to a file, not return it to the user
            return JsonResponse({'error': 'AI Service unavailable'}, status=503)
            
    return JsonResponse({'error': 'POST request required'}, status=405)