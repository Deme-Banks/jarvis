"""
Load Environment Variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file"""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Load .env file
    env_file = project_root / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✓ Loaded environment variables from {env_file}")
    else:
        # Try to load from .env.example as fallback
        env_example = project_root / '.env.example'
        if env_example.exists():
            print(f"⚠ .env file not found. Using .env.example as template.")
            print(f"  Please copy .env.example to .env and add your API keys.")
        else:
            print("⚠ No .env file found. Using system environment variables.")
    
    # Verify OpenAI key is set
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        # Mask the key for display
        masked_key = openai_key[:7] + "..." + openai_key[-4:] if len(openai_key) > 11 else "***"
        print(f"✓ OpenAI API key loaded: {masked_key}")
    else:
        print("⚠ OpenAI API key not found in environment variables")
    
    return {
        "openai_key_set": bool(openai_key),
        "env_file_exists": env_file.exists()
    }


if __name__ == '__main__':
    load_environment()
