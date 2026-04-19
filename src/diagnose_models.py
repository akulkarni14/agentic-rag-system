import os
from dotenv import load_dotenv
import google.generativeai as genai

def diagnose():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: No GEMINI_API_KEY found in .env")
        return

    print(f"Configuring with API Key found in .env...")
    genai.configure(api_key=api_key)
    
    print("\n--- Available Models ---")
    try:
        models = genai.list_models()
        count = 0
        for m in models:
            print(f"- {m.name} (Methods: {m.supported_generation_methods})")
            count += 1
        print(f"\nTotal models found: {count}")
    except Exception as e:
        print(f"ERROR listing models: {e}")

if __name__ == "__main__":
    diagnose()
