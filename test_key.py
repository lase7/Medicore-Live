import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Load the .env file
load_dotenv()

# 2. Get the key
key = os.getenv("GOOGLE_API_KEY")
print(f"🔑 Key found: {key}")

if not key:
    print("❌ ERROR: No key found in .env file!")
else:
    # 3. Test the connection
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, are you working?")
        print(f"✅ SUCCESS! AI says: {response.text}")
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")