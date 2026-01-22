# Mobile Security Testing Guide

## Overview

JARVIS includes security testing tools for both iOS and Android devices. These tools are for **authorized penetration testing and educational purposes only**.

⚠️ **WARNING**: Use only on devices you own or have explicit authorization to test. Illegal without proper authorization.

## iOS Tools

### PIN Brute Force
```
"Create iOS PIN brute force script"
"Generate iPhone PIN cracker"
```

### Backup Extractor
```
"Create iOS backup extractor"
"Make iPhone backup analyzer"
```

### Frida Hooks
```
"Create iOS Frida hook for app com.example.app"
"Generate iPhone app hooking script"
```

### IPA Analyzer
```
"Create iOS IPA analyzer"
"Analyze iPhone app package"
```

## Android Tools

### PIN/Pattern Brute Force
```
"Create Android PIN brute force"
"Generate Android pattern cracker"
```

### APK Analyzer
```
"Create Android APK analyzer"
"Analyze Android app package"
```

### Frida Hooks
```
"Create Android Frida hook for package com.example.app"
"Generate Android app hooking script"
```

### ADB Exploits
```
"Create Android ADB backup exploit"
"Generate Android ADB shell script"
"Create Android logcat monitor"
```

## Voice Commands

### iOS
```
"Jarvis, create iOS PIN brute force"
"Jarvis, generate iPhone backup extractor"
"Jarvis, create iOS Frida hook for app com.apple.mobilesafari"
"Jarvis, analyze iOS IPA"
```

### Android
```
"Jarvis, create Android PIN brute force"
"Jarvis, generate Android APK analyzer"
"Jarvis, create Android Frida hook for package com.android.chrome"
"Jarvis, create Android ADB backup exploit"
```

## Required Tools

### iOS
- **libimobiledevice**: Device communication
  ```bash
  # macOS/Linux
  brew install libimobiledevice
  # or
  apt-get install libimobiledevice-utils
  ```

- **Frida**: Dynamic instrumentation
  ```bash
  pip install frida-tools
  ```

- **Objection**: Runtime mobile exploration
  ```bash
  pip install objection
  ```

### Android
- **ADB**: Android Debug Bridge
  ```bash
  # Install Android SDK Platform Tools
  # Download from: https://developer.android.com/studio/releases/platform-tools
  ```

- **Frida**: Dynamic instrumentation
  ```bash
  pip install frida-tools
  ```

- **APKTool**: APK reverse engineering
  ```bash
  # Download from: https://ibotpeaches.github.io/Apktool/
  ```

- **aapt**: Android Asset Packaging Tool (part of Android SDK)

## Usage Examples

### iOS PIN Brute Force
```python
from mobile_security import iOSTestingTools

ios = iOSTestingTools()
result = ios.create_pin_brute_force_script(max_attempts=10)
print(f"Script: {result['file']}")
```

### Android APK Analysis
```python
from mobile_security import AndroidTestingTools

android = AndroidTestingTools()
result = android.create_apk_analyzer()
print(f"Analyzer: {result['file']}")
```

### Frida Hooking
```python
# iOS
result = ios.create_frida_hook_script("com.example.app")

# Android
result = android.create_frida_hook_script("com.example.app")
```

## Security Notes

⚠️ **IMPORTANT**:
- All tools include warnings
- Use only on devices you own
- Get authorization before testing
- iOS/Android have lockout mechanisms
- Brute force will lock devices after attempts
- Use in isolated test environments
- Follow responsible disclosure

## Legal and Ethical

**ALLOWED**:
- ✅ Testing your own devices
- ✅ Authorized penetration testing
- ✅ Security research with permission
- ✅ Educational purposes
- ✅ Bug bounty programs (with authorization)

**NOT ALLOWED**:
- ❌ Testing without authorization
- ❌ Accessing others' devices
- ❌ Bypassing security for malicious purposes
- ❌ Production systems without permission
- ❌ Violating terms of service

## Best Practices

1. **Always get authorization** before testing
2. **Use isolated test devices** only
3. **Review generated code** before running
4. **Understand lockout mechanisms** (devices will lock)
5. **Follow responsible disclosure** for vulnerabilities
6. **Document your testing** for authorized work

## Troubleshooting

### "Tool not found"
- Install required tools (ADB, Frida, etc.)
- Check PATH environment variable
- Verify tool installation

### "Device not detected"
- Enable USB debugging (Android)
- Trust computer (iOS)
- Check USB connection
- Verify device drivers

### "Permission denied"
- Check device authorization
- Enable developer mode
- Grant necessary permissions
- Use authorized devices only

---

**Remember: Use responsibly and only for authorized security testing!**
