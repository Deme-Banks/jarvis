"""
System Information Utilities
"""
import platform
import psutil
import os
from typing import Dict
from datetime import datetime


class SystemInfo:
    """Get system information"""
    
    @staticmethod
    def get_full_info() -> Dict:
        """Get complete system information"""
        return {
            'platform': SystemInfo.get_platform_info(),
            'hardware': SystemInfo.get_hardware_info(),
            'python': SystemInfo.get_python_info(),
            'disk': SystemInfo.get_disk_info(),
            'memory': SystemInfo.get_memory_info(),
            'network': SystemInfo.get_network_info(),
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def get_platform_info() -> Dict:
        """Get platform information"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node()
        }
    
    @staticmethod
    def get_hardware_info() -> Dict:
        """Get hardware information"""
        try:
            return {
                'cpu_count': psutil.cpu_count(),
                'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                'cpu_percent': psutil.cpu_percent(interval=1),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
        except:
            return {}
    
    @staticmethod
    def get_python_info() -> Dict:
        """Get Python information"""
        import sys
        return {
            'version': sys.version,
            'version_info': {
                'major': sys.version_info.major,
                'minor': sys.version_info.minor,
                'micro': sys.version_info.micro
            },
            'executable': sys.executable,
            'platform': sys.platform
        }
    
    @staticmethod
    def get_disk_info() -> Dict:
        """Get disk information"""
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            return {
                'total_gb': total / (1024**3),
                'used_gb': used / (1024**3),
                'free_gb': free / (1024**3),
                'percent_used': (used / total) * 100
            }
        except:
            return {}
    
    @staticmethod
    def get_memory_info() -> Dict:
        """Get memory information"""
        try:
            mem = psutil.virtual_memory()
            return {
                'total_gb': mem.total / (1024**3),
                'available_gb': mem.available / (1024**3),
                'used_gb': mem.used / (1024**3),
                'percent': mem.percent
            }
        except:
            return {}
    
    @staticmethod
    def get_network_info() -> Dict:
        """Get network information"""
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            return {
                'hostname': hostname,
                'local_ip': local_ip
            }
        except:
            return {}
    
    @staticmethod
    def print_summary():
        """Print system summary"""
        info = SystemInfo.get_full_info()
        
        print("=" * 50)
        print("System Information")
        print("=" * 50)
        
        # Platform
        platform_info = info.get('platform', {})
        print(f"\nPlatform: {platform_info.get('system')} {platform_info.get('release')}")
        print(f"Hostname: {platform_info.get('hostname')}")
        
        # Hardware
        hardware = info.get('hardware', {})
        if hardware:
            print(f"\nCPU: {hardware.get('cpu_count')} cores")
            if hardware.get('cpu_freq'):
                print(f"CPU Frequency: {hardware.get('cpu_freq', {}).get('current', 'N/A')} MHz")
        
        # Memory
        memory = info.get('memory', {})
        if memory:
            print(f"\nMemory: {memory.get('total_gb', 0):.2f} GB total")
            print(f"Available: {memory.get('available_gb', 0):.2f} GB")
            print(f"Used: {memory.get('percent', 0):.1f}%")
        
        # Disk
        disk = info.get('disk', {})
        if disk:
            print(f"\nDisk: {disk.get('total_gb', 0):.2f} GB total")
            print(f"Free: {disk.get('free_gb', 0):.2f} GB")
            print(f"Used: {disk.get('percent_used', 0):.1f}%")
        
        # Network
        network = info.get('network', {})
        if network:
            print(f"\nNetwork: {network.get('local_ip', 'N/A')}")
        
        print("=" * 50)
