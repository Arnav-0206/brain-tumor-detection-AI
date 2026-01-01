import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"🔑 API Key: {api_key[:20]}...\n")

genai.configure(api_key=api_key)

# Test different model names
models_to_test = [
    "gemini-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
    "models/gemini-pro",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash",
]

print("🧪 Testing each model:\n")
for model_name in models_to_test:
    try:
        print(f"Testing: {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello!'")
        print(f"✅ SUCCESS! Response: {response.text[:50]}")
        print(f"   👉 USE THIS MODEL: {model_name}\n")
        break  # Stop at first working model
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ 404 - Model not found")
        elif "403" in error_msg:
            print(f"❌ 403 - Permission denied")
        else:
            print(f"❌ Error: {error_msg[:80]}")

print("\n📋 Listing ALL available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  ✅ {m.name}")
except Exception as e:
    print(f"❌ Could not list models: {e}")
