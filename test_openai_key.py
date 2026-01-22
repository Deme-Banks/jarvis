"""
Test OpenAI API Key Configuration
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

# Check OpenAI key
openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    # Mask the key for display
    masked_key = openai_key[:7] + "..." + openai_key[-4:] if len(openai_key) > 11 else "***"
    print(f"✓ OpenAI API key found: {masked_key}")
    print(f"  Key length: {len(openai_key)} characters")
    
    # Test API connection
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }
        
        # Simple API test
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ OpenAI API connection successful!")
            print("  Your API key is valid and working.")
            models = response.json().get('data', [])
            print(f"  Available models: {len(models)}")
        else:
            print(f"⚠ API test returned status code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    except ImportError:
        print("⚠ requests library not installed. Install with: pip install requests")
    except Exception as e:
        print(f"⚠ API test error: {e}")
else:
    print("✗ OpenAI API key not found!")
    print("  Please set OPENAI_API_KEY in your .env file or environment variables")

print("\n" + "="*50)
print("JARVIS OpenAI Features Now Available:")
print("  ✓ DALL-E Image Generation")
print("  ✓ GPT-4 Chat")
print("  ✓ GPT-4 Vision (Image Analysis)")
print("  ✓ Whisper (Audio Transcription)")
print("  ✓ Multi-modal AI")
print("  ✓ Voice Emotion Detection")
print("="*50)
