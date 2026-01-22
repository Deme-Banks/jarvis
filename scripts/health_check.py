"""
Health Check Script for JARVIS
"""
import sys
import os
import time
from pathlib import Path


def check_system():
    """Check system health"""
    print("System Health Check")
    print("=" * 50)
    
    checks = []
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        checks.append(True)
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        checks.append(False)
    
    # Check directories
    required_dirs = ['./memory', './logs', './config']
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory: {directory}")
            checks.append(True)
        else:
            print(f"✗ Directory missing: {directory}")
            checks.append(False)
    
    # Check dependencies
    print("\nChecking dependencies...")
    deps = {
        'vosk': 'vosk',
        'pyaudio': 'pyaudio',
        'requests': 'requests',
        'flask': 'flask',
        'psutil': 'psutil'
    }
    
    for name, module in deps.items():
        try:
            __import__(module)
            print(f"✓ {name}")
            checks.append(True)
        except ImportError:
            print(f"✗ {name} - MISSING")
            checks.append(False)
    
    # Check Ollama
    print("\nChecking Ollama...")
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            print("✓ Ollama is running")
            checks.append(True)
        else:
            print("✗ Ollama not responding")
            checks.append(False)
    except:
        print("✗ Ollama not running")
        checks.append(False)
    
    # Check disk space
    print("\nChecking disk space...")
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free / (1024**3)
        if free_gb > 1:
            print(f"✓ Free space: {free_gb:.2f} GB")
            checks.append(True)
        else:
            print(f"⚠ Low disk space: {free_gb:.2f} GB")
            checks.append(False)
    except:
        print("✗ Could not check disk space")
        checks.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    print(f"Health Score: {passed}/{total} ({passed*100//total}%)")
    
    if passed == total:
        print("✓ All checks passed!")
        return True
    else:
        print("⚠ Some checks failed")
        return False


if __name__ == "__main__":
    success = check_system()
    sys.exit(0 if success else 1)
