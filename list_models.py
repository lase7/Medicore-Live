import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("🔍 Searching for available AI models...")
print("------------------------------------------------")

try:
    # Ask Google for the list
    for m in genai.list_models():
        # Only show models that can generate text
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")

print("------------------------------------------------")