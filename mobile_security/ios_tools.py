"""
iOS Security Testing Tools
WARNING: For authorized testing and educational purposes only.
"""
import os
import subprocess
import tempfile
from typing import Dict, List, Optional
from datetime import datetime


class iOSTestingTools:
    """iOS security testing tools for authorized penetration testing"""
    
    def __init__(self):
        self.tools_available = self._check_tools()
    
    def _check_tools(self) -> Dict:
        """Check available iOS testing tools"""
        tools = {}
        
        # Check for libimobiledevice
        try:
            result = subprocess.run(['idevice_id', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            tools['libimobiledevice'] = result.returncode == 0
        except:
            tools['libimobiledevice'] = False
        
        # Check for frida
        try:
            result = subprocess.run(['frida', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            tools['frida'] = result.returncode == 0
        except:
            tools['frida'] = False
        
        # Check for objection
        try:
            result = subprocess.run(['objection', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            tools['objection'] = result.returncode == 0
        except:
            tools['objection'] = False
        
        return tools
    
    def create_pin_brute_force_script(self, max_attempts: int = 10) -> Dict:
        """Create PIN brute force script (for authorized testing)"""
        code = f'''"""
Educational iOS PIN Brute Force - FOR AUTHORIZED TESTING ONLY
WARNING: Use only on devices you own or have explicit authorization to test.
Illegal without proper authorization.
"""
import subprocess
import time

def brute_force_pin(device_id, max_attempts={max_attempts}):
    """
    Attempt to brute force PIN (educational only)
    Note: iOS has lockout mechanisms that will prevent this in practice
    """
    pins = [f"{{i:04d}}" for i in range(10000)]  # 0000-9999
    
    for i, pin in enumerate(pins[:max_attempts]):
        print(f"Attempting PIN: {{pin}}")
        
        # Use libimobiledevice to attempt unlock
        # Note: This is simplified - real implementation would use device APIs
        try:
            # In real scenario, would use ideviceenterrecovery or similar
            # This is for educational demonstration only
            result = subprocess.run(
                ['ideviceenterrecovery', device_id],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"Success! PIN: {{pin}}")
                return pin
            
            # Rate limiting - iOS locks after failed attempts
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {{e}}")
            break
    
    print("Brute force failed or device locked")
    return None

# Usage (for authorized testing only)
if __name__ == "__main__":
    device_id = "YOUR_DEVICE_ID"  # Get with: idevice_id -l
    brute_force_pin(device_id)
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"ios_pin_brute_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'pin_brute_force',
            'file': filepath,
            'max_attempts': max_attempts,
            'warning': 'Educational only. Use only on devices you own. iOS has lockout mechanisms. Illegal without authorization.'
        }
    
    def create_backup_extractor(self) -> Dict:
        """Create iOS backup extraction tool"""
        code = '''"""
Educational iOS Backup Extractor - FOR AUTHORIZED TESTING ONLY
WARNING: Use only on backups you own or have authorization to analyze.
"""
import os
import plistlib
import sqlite3
from pathlib import Path

def extract_backup(backup_path):
    """
    Extract data from iOS backup
    Requires: libimobiledevice or iTunes backup
    """
    backup_dir = Path(backup_path)
    
    # Find Info.plist
    info_plist = backup_dir / "Info.plist"
    if not info_plist.exists():
        print("Info.plist not found")
        return None
    
    # Read backup info
    with open(info_plist, 'rb') as f:
        info = plistlib.load(f)
    
    print(f"Device: {info.get('Display Name', 'Unknown')}")
    print(f"iOS Version: {info.get('Product Version', 'Unknown')}")
    print(f"Backup Date: {info.get('Last Backup Date', 'Unknown')}")
    
    # Extract files
    manifest_db = backup_dir / "Manifest.db"
    if manifest_db.exists():
        conn = sqlite3.connect(manifest_db)
        cursor = conn.cursor()
        
        # Get file list
        cursor.execute("SELECT fileID, domain, relativePath FROM Files")
        files = cursor.fetchall()
        
        print(f"\\nFound {len(files)} files in backup")
        
        # Extract interesting files
        interesting_domains = [
            'AppDomain-com.apple.mobilephone',
            'AppDomain-com.apple.mobilesafari',
            'AppDomain-com.apple.mobilemail'
        ]
        
        for file_id, domain, rel_path in files:
            if any(domain.startswith(d) for d in interesting_domains):
                print(f"Found: {domain}/{rel_path}")
        
        conn.close()
    
    return info

# Usage
if __name__ == "__main__":
    backup_path = input("Enter backup path: ")
    extract_backup(backup_path)
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"ios_backup_extractor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'backup_extractor',
            'file': filepath,
            'warning': 'Educational only. Use only on backups you own. Illegal without authorization.'
        }
    
    def create_frida_hook_script(self, app_name: str) -> Dict:
        """Create Frida hooking script for iOS app analysis"""
        code = f'''"""
Educational Frida Hooking Script - FOR AUTHORIZED TESTING ONLY
WARNING: Use only on apps you own or have authorization to test.
"""
import frida
import sys

def on_message(message, data):
    if message['type'] == 'send':
        print(f"[*] {{message['payload']}}")
    else:
        print(f"[!] {{message}}")

# Connect to device
device = frida.get_usb_device()

# Attach to app
session = device.attach("{app_name}")

# Hook script
script_code = """
// Hook Objective-C methods
var className = ObjC.classes.NSString;
if (className) {{
    var method = className['- stringByAppendingString:'];
    if (method) {{
        Interceptor.attach(method.implementation, {{
            onEnter: function(args) {{
                console.log("[*] stringByAppendingString called");
                console.log("[*] Arguments: " + args[2]);
            }}
        }});
    }}
}}

// Hook Swift functions
var swiftFunction = Module.findExportByName(null, "swift_function_name");
if (swiftFunction) {{
    Interceptor.attach(swiftFunction, {{
        onEnter: function(args) {{
            console.log("[*] Swift function called");
        }}
    }});
}}

// Monitor network
var NSURLConnection = ObjC.classes.NSURLConnection;
if (NSURLConnection) {{
    var method = NSURLConnection['+ sendAsynchronousRequest:queue:completionHandler:'];
    if (method) {{
        Interceptor.attach(method.implementation, {{
            onEnter: function(args) {{
                console.log("[*] Network request detected");
            }}
        }});
    }}
}}
"""

script = session.create_script(script_code)
script.on('message', on_message)
script.load()

print(f"[*] Hooking {app_name}...")
print("[*] Press Ctrl+C to stop")

sys.stdin.read()
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"ios_frida_hook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'frida_hook',
            'file': filepath,
            'app': app_name,
            'warning': 'Educational only. Use only on apps you own. Illegal without authorization.'
        }
    
    def create_ipa_analyzer(self) -> Dict:
        """Create IPA file analyzer"""
        code = '''"""
Educational IPA Analyzer - FOR AUTHORIZED TESTING ONLY
WARNING: Use only on IPAs you own or have authorization to analyze.
"""
import zipfile
import plistlib
import os
from pathlib import Path

def analyze_ipa(ipa_path):
    """
    Analyze iOS IPA file
    """
    ipa_file = Path(ipa_path)
    
    if not ipa_file.exists():
        print(f"IPA not found: {ipa_path}")
        return None
    
    # Extract IPA (it's a zip file)
    extract_dir = ipa_file.parent / f"{ipa_file.stem}_extracted"
    extract_dir.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(ipa_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Find app bundle
    payload_dir = extract_dir / "Payload"
    if payload_dir.exists():
        app_bundles = list(payload_dir.glob("*.app"))
        if app_bundles:
            app_bundle = app_bundles[0]
            
            # Read Info.plist
            info_plist = app_bundle / "Info.plist"
            if info_plist.exists():
                with open(info_plist, 'rb') as f:
                    info = plistlib.load(f)
                
                print(f"App Name: {info.get('CFBundleName', 'Unknown')}")
                print(f"Bundle ID: {info.get('CFBundleIdentifier', 'Unknown')}")
                print(f"Version: {info.get('CFBundleVersion', 'Unknown')}")
                print(f"Minimum iOS: {info.get('MinimumOSVersion', 'Unknown')}")
                
                # Check for security features
                if info.get('NSAppTransportSecurity'):
                    print("\\n[*] App Transport Security configured")
                
                # Check entitlements
                entitlements = app_bundle / "archived-expanded-entitlements.xcent"
                if entitlements.exists():
                    with open(entitlements, 'rb') as f:
                        ents = plistlib.load(f)
                    print(f"\\n[*] Entitlements: {list(ents.keys())}")
                
                # List binaries
                binaries = list(app_bundle.rglob("*"))
                binaries = [b for b in binaries if os.access(b, os.X_OK) and b.is_file()]
                print(f"\\n[*] Found {len(binaries)} executable files")
                
                return info
    
    return None

# Usage
if __name__ == "__main__":
    ipa_path = input("Enter IPA path: ")
    analyze_ipa(ipa_path)
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"ios_ipa_analyzer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'ipa_analyzer',
            'file': filepath,
            'warning': 'Educational only. Use only on IPAs you own. Illegal without authorization.'
        }
