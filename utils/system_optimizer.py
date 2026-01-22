"""
System Optimization Utilities
"""
import os
import psutil
import subprocess
from typing import Dict, List, Optional
import platform


class SystemOptimizer:
    """System optimization utilities"""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_system_health(self) -> Dict:
        """Get comprehensive system health"""
        health = {
            'cpu': self._get_cpu_health(),
            'memory': self._get_memory_health(),
            'disk': self._get_disk_health(),
            'network': self._get_network_health(),
            'overall': 'healthy'
        }
        
        # Determine overall health
        issues = []
        if health['cpu']['usage'] > 90:
            issues.append('high_cpu')
        if health['memory']['percent'] > 90:
            issues.append('high_memory')
        if health['disk']['percent_used'] > 90:
            issues.append('low_disk_space')
        
        if issues:
            health['overall'] = 'warning'
            health['issues'] = issues
        else:
            health['overall'] = 'healthy'
        
        return health
    
    def _get_cpu_health(self) -> Dict:
        """Get CPU health"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'usage': cpu_percent,
                'cores': cpu_count,
                'frequency_mhz': cpu_freq.current if cpu_freq else None,
                'status': 'healthy' if cpu_percent < 80 else 'warning' if cpu_percent < 95 else 'critical'
            }
        except:
            return {'status': 'unknown'}
    
    def _get_memory_health(self) -> Dict:
        """Get memory health"""
        try:
            mem = psutil.virtual_memory()
            return {
                'total_gb': mem.total / (1024**3),
                'available_gb': mem.available / (1024**3),
                'used_gb': mem.used / (1024**3),
                'percent': mem.percent,
                'status': 'healthy' if mem.percent < 80 else 'warning' if mem.percent < 95 else 'critical'
            }
        except:
            return {'status': 'unknown'}
    
    def _get_disk_health(self) -> Dict:
        """Get disk health"""
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            return {
                'total_gb': total / (1024**3),
                'used_gb': used / (1024**3),
                'free_gb': free / (1024**3),
                'percent_used': (used / total) * 100,
                'status': 'healthy' if (used / total) < 0.8 else 'warning' if (used / total) < 0.95 else 'critical'
            }
        except:
            return {'status': 'unknown'}
    
    def _get_network_health(self) -> Dict:
        """Get network health"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'status': 'healthy'
            }
        except:
            return {'status': 'unknown'}
    
    def optimize_system(self) -> Dict:
        """Optimize system performance"""
        optimizations = []
        
        # Clear Python cache
        try:
            import py_compile
            # Clear __pycache__
            for root, dirs, files in os.walk('.'):
                if '__pycache__' in dirs:
                    cache_dir = os.path.join(root, '__pycache__')
                    import shutil
                    shutil.rmtree(cache_dir)
                    optimizations.append('Cleared Python cache')
        except:
            pass
        
        # Suggest optimizations
        health = self.get_system_health()
        
        if health['memory']['percent'] > 80:
            optimizations.append('Consider clearing memory or restarting JARVIS')
        
        if health['disk']['percent_used'] > 80:
            optimizations.append('Consider cleaning up old logs and cache files')
        
        if health['cpu']['usage'] > 80:
            optimizations.append('High CPU usage detected. Close unnecessary processes')
        
        return {
            'success': True,
            'optimizations': optimizations,
            'health': health
        }
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations"""
        recommendations = []
        health = self.get_system_health()
        
        # Memory recommendations
        if health['memory']['percent'] > 70:
            recommendations.append("Reduce cache size in config")
            recommendations.append("Disable unused agents")
        
        # CPU recommendations
        if health['cpu']['usage'] > 70:
            recommendations.append("Use smaller LLM models")
            recommendations.append("Reduce parallel processing")
        
        # Disk recommendations
        if health['disk']['percent_used'] > 70:
            recommendations.append("Clean up old logs")
            recommendations.append("Remove unused models")
        
        return recommendations
