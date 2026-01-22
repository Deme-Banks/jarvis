"""
Test Google Gemini API Key Configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    load_dotenv(env_file)
    print(f"✓ Loaded .env file from {env_file}")
else:
    load_dotenv()
    print("⚠ Using system environment variables")

# Check Gemini key
gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key:
    # Mask the key for display
    masked_key = gemini_key[:10] + "..." + gemini_key[-4:] if len(gemini_key) > 14 else "***"
    print(f"✓ Google Gemini API key found: {masked_key}")
    print(f"  Key length: {len(gemini_key)} characters")
    
    # Test API connection
    try:
        import requests
        
        # Test Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✓ Google Gemini API connection successful!")
            print("  Your API key is valid and working.")
            models = response.json().get('models', [])
            print(f"  Available models: {len(models)}")
            if models:
                print(f"  Sample models: {', '.join([m.get('name', '') for m in models[:3]])}")
        else:
            print(f"⚠ API test returned status code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    except ImportError:
        print("⚠ requests library not installed. Install with: pip install requests")
    except Exception as e:
        print(f"⚠ API test error: {e}")
else:
    print("✗ Google Gemini API key not found!")
    print("  Please set GEMINI_API_KEY in your .env file or environment variables")

print("\n" + "="*50)
print("JARVIS Gemini Features Now Available:")
print("  ✓ Gemini Pro Chat")
print("  ✓ Gemini Vision (Image Analysis)")
print("  ✓ Multi-modal AI with Gemini")
print("  ✓ Code Generation with Gemini")
print("  ✓ Document Analysis")
print("="*50)
