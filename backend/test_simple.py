import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\nListing available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"AVAILABLE: {m.name}")
            
            # Try to use the first one we find
            try:
                print(f"  Testing {m.name}...")
                model = genai.GenerativeModel(m.name)
                response = model.generate_content("Say hello")
                print(f"  SUCCESS! Response: {response.text[:50]}")
                print(f"\n*** USE THIS MODEL: {m.name} ***\n")
                break
            except Exception as e:
                print(f"  FAILED: {str(e)[:100]}")
                
except Exception as e:
    print(f"Error listing models: {e}")
