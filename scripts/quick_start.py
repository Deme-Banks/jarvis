"""
Quick Start Script for JARVIS
"""
import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if dependencies are installed"""
    print("Checking dependencies...")
    
    required = ['vosk', 'pyaudio', 'requests', 'flask']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements_pi.txt")
        return False
    
    return True


def setup_directories():
    """Create necessary directories"""
    print("\nSetting up directories...")
    
    directories = [
        './memory',
        './logs',
        './backups',
        './plugins',
        './config',
        './temp'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ {directory}")


def check_ollama():
    """Check if Ollama is available"""
    print("\nChecking Ollama...")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            print("✓ Ollama is running")
            models = response.json().get('models', [])
            if models:
                print(f"  Available models: {', '.join([m['name'] for m in models])}")
            else:
                print("  No models installed. Run: ollama pull llama2")
            return True
    except:
        pass
    
    print("✗ Ollama not running")
    print("  Install from: https://ollama.ai")
    print("  Or use cloud fallback")
    return False


def setup_config():
    """Setup default configuration"""
    print("\nSetting up configuration...")
    
    config_file = './config/user_config.json'
    if not os.path.exists(config_file):
        from config.configuration_manager import ConfigurationManager
        config = ConfigurationManager()
        print(f"✓ Created default configuration: {config_file}")
    else:
        print(f"✓ Configuration exists: {config_file}")


def main():
    """Main setup function"""
    print("=" * 50)
    print("JARVIS Quick Start Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠ Please install missing dependencies first")
        return False
    
    # Setup directories
    setup_directories()
    
    # Check Ollama
    check_ollama()
    
    # Setup config
    setup_config()
    
    print("\n" + "=" * 50)
    print("✓ Setup complete!")
    print("=" * 50)
    print("\nTo start JARVIS:")
    print("  python jarvis_pi.py")
    print("\nTo access web dashboard:")
    print("  python -m web.dashboard")
    print("\nTo use API:")
    print("  python -m api.rest_api")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
