"""
Setup API Keys for Cloud LLMs
"""
import os
import sys
from pathlib import Path


def setup_openai_key():
    """Setup OpenAI API key"""
    print("\n" + "=" * 50)
    print("OpenAI (ChatGPT) API Key Setup")
    print("=" * 50)
    print("\n1. Go to: https://platform.openai.com/api-keys")
    print("2. Sign in or create account")
    print("3. Click 'Create new secret key'")
    print("4. Copy your API key\n")
    
    key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if key:
        # Set environment variable for current session
        os.environ['OPENAI_API_KEY'] = key
        
        # Save to .env file
        env_file = Path('.env')
        env_content = ""
        
        if env_file.exists():
            env_content = env_file.read_text()
            # Remove existing OPENAI_API_KEY if present
            lines = [line for line in env_content.split('\n') 
                    if not line.startswith('OPENAI_API_KEY=')]
            env_content = '\n'.join(lines)
        
        env_content += f"\nOPENAI_API_KEY={key}\n"
        env_file.write_text(env_content)
        
        print("✓ OpenAI API key saved!")
        return True
    else:
        print("Skipped OpenAI setup")
        return False


def setup_gemini_key():
    """Setup Gemini API key"""
    print("\n" + "=" * 50)
    print("Google Gemini API Key Setup")
    print("=" * 50)
    print("\n1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy your API key\n")
    
    key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if key:
        # Set environment variable for current session
        os.environ['GEMINI_API_KEY'] = key
        
        # Save to .env file
        env_file = Path('.env')
        env_content = ""
        
        if env_file.exists():
            env_content = env_file.read_text()
            # Remove existing GEMINI_API_KEY if present
            lines = [line for line in env_content.split('\n') 
                    if not line.startswith('GEMINI_API_KEY=')]
            env_content = '\n'.join(lines)
        
        env_content += f"\nGEMINI_API_KEY={key}\n"
        env_file.write_text(env_content)
        
        print("✓ Gemini API key saved!")
        return True
    else:
        print("Skipped Gemini setup")
        return False


def test_keys():
    """Test API keys"""
    print("\n" + "=" * 50)
    print("Testing API Keys")
    print("=" * 50)
    
    # Test OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("\nTesting OpenAI...")
        try:
            from llm.cloud_llm import OpenAILLM
            llm = OpenAILLM(api_key=openai_key)
            if llm.check_available():
                print("✓ OpenAI is working!")
            else:
                print("✗ OpenAI API not responding")
        except Exception as e:
            print(f"✗ OpenAI error: {e}")
    else:
        print("\nOpenAI key not set")
    
    # Test Gemini
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print("\nTesting Gemini...")
        try:
            from llm.cloud_llm import GeminiLLM
            llm = GeminiLLM(api_key=gemini_key)
            if llm.check_available():
                print("✓ Gemini is working!")
            else:
                print("✗ Gemini API not responding")
        except Exception as e:
            print(f"✗ Gemini error: {e}")
    else:
        print("\nGemini key not set")


def main():
    """Main setup function"""
    print("=" * 50)
    print("JARVIS Cloud LLM API Key Setup")
    print("=" * 50)
    print("\nThis script will help you set up API keys for:")
    print("- OpenAI (ChatGPT)")
    print("- Google Gemini")
    print("\nYou need at least one API key to use cloud LLMs.")
    
    # Load existing .env if present
    env_file = Path('.env')
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("\n✓ Loaded existing .env file")
    
    # Setup OpenAI
    setup_openai_key()
    
    # Setup Gemini
    setup_gemini_key()
    
    # Test keys
    test_keys()
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print("\nYour API keys have been saved to .env file")
    print("JARVIS will automatically use them when you start it.")
    print("\nTo start JARVIS:")
    print("  python jarvis_pi.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
