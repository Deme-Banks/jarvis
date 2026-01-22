"""
Performance Monitoring and Analytics
"""
import time
import psutil
import os
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import json


class PerformanceMonitor:
    """Monitor system and JARVIS performance"""
    
    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.response_times = deque(maxlen=history_size)
        self.memory_usage = deque(maxlen=history_size)
        self.cpu_usage = deque(maxlen=history_size)
        self.command_counts = {}
        self.error_counts = {}
        self.start_time = time.time()
    
    def record_response_time(self, response_time: float):
        """Record response time"""
        self.response_times.append({
            'time': response_time,
            'timestamp': datetime.now().isoformat()
        })
    
    def record_command(self, command: str):
        """Record command execution"""
        command_type = self._classify_command(command)
        self.command_counts[command_type] = self.command_counts.get(command_type, 0) + 1
    
    def record_error(self, error_type: str):
        """Record error"""
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
    
    def _classify_command(self, command: str) -> str:
        """Classify command type"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ["create", "make", "generate"]):
            return "creation"
        elif any(word in command_lower for word in ["test", "run", "execute"]):
            return "execution"
        elif any(word in command_lower for word in ["deploy", "install", "copy"]):
            return "deployment"
        elif any(word in command_lower for word in ["what", "how", "explain", "tell"]):
            return "query"
        elif any(word in command_lower for word in ["scan", "detect", "check"]):
            return "scanning"
        else:
            return "other"
    
    def get_system_stats(self) -> Dict:
        """Get current system statistics"""
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_mb': memory_info.rss / (1024 * 1024),
                'memory_percent': process.memory_percent(),
                'threads': process.num_threads(),
                'open_files': len(process.open_files()),
                'uptime_seconds': time.time() - self.start_time
            }
        except:
            return {}
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        if not self.response_times:
            return {}
        
        times = [r['time'] for r in self.response_times]
        
        return {
            'avg_response_time': sum(times) / len(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'total_responses': len(self.response_times),
            'commands_by_type': dict(self.command_counts),
            'errors_by_type': dict(self.error_counts)
        }
    
    def get_summary(self) -> Dict:
        """Get complete summary"""
        return {
            'system': self.get_system_stats(),
            'performance': self.get_performance_stats(),
            'uptime_hours': (time.time() - self.start_time) / 3600
        }
    
    def export_data(self, filepath: str):
        """Export monitoring data"""
        data = {
            'summary': self.get_summary(),
            'response_times': list(self.response_times),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
