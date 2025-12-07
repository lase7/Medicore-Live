import google.generativeai as genai
from django.conf import settings

def query_gemmacare(user_query, patient_context=None):
    # Check for API Key
    if not hasattr(settings, 'GEMINI_API_KEY'):
        return "Error: API Key missing."

    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    system_instruction = "You are GemmaCare, a medical AI assistant. Start responses with 'Disclaimer: I am an AI.'."
    
    # Build Context
    context_str = ""
    if patient_context:
        context_str = f"Patient Info: {patient_context}"

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(f"{system_instruction}\n{context_str}\nQuery: {user_query}")
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"