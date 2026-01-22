"""
Setup API Keys - Quick setup script
"""
import os
from pathlib import Path


def setup_openai_key(api_key: str):
    """Setup OpenAI API key"""
    project_root = Path(__file__).parent
    env_file = project_root / '.env'
    
    # Read existing .env if it exists
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Update or add OpenAI key
    if "OPENAI_API_KEY=" in env_content:
        # Replace existing key
        lines = env_content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith("OPENAI_API_KEY="):
                new_lines.append(f"OPENAI_API_KEY={api_key}")
            else:
                new_lines.append(line)
        env_content = '\n'.join(new_lines)
    else:
        # Add new key
        if env_content and not env_content.endswith('\n'):
            env_content += '\n'
        env_content += f"OPENAI_API_KEY={api_key}\n"
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✓ OpenAI API key configured in {env_file}")
    print(f"  Key: {api_key[:7]}...{api_key[-4:]}")
    
    # Also set as environment variable for current session
    os.environ["OPENAI_API_KEY"] = api_key
    print("✓ OpenAI API key set in current session")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        setup_openai_key(api_key)
        print("\n✓ Setup complete! OpenAI API key is now configured.")
        print("  You can now use DALL-E image generation, GPT-4 Vision, and other OpenAI features.")
    else:
        print("Usage: python setup_api_keys.py <your_openai_api_key>")
        print("\nExample:")
        print("  python setup_api_keys.py sk-proj-...")
