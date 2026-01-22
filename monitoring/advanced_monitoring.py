"""
Advanced Monitoring and Alerting
"""
import os
import time
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime
import psutil


class AdvancedMonitor:
    """Advanced system monitoring"""
    
    def __init__(self):
        # Add optimized caching
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
        self.metrics = {}
        self.alerts = []
        self.alert_callbacks: List[Callable] = []
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self, interval: int = 5):
        """Start monitoring system"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def _monitor_loop(self, interval: int):
        """Monitoring loop"""
        while self.monitoring:
            try:
                # CPU metrics
                self.metrics['cpu'] = {
                    'percent': psutil.cpu_percent(interval=1),
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                }
                
                # Memory metrics
                memory = psutil.virtual_memory()
                self.metrics['memory'] = {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                }
                
                # Disk metrics
                disk = psutil.disk_usage('/')
                self.metrics['disk'] = {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent
                }
                
                # Network metrics
                net_io = psutil.net_io_counters()
                self.metrics['network'] = {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                }
                
                # Check alerts
                self._check_alerts()
                
                time.sleep(interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(interval)
    
    def _check_alerts(self):
        """Check for alert conditions"""
        alerts_triggered = []
        
        # CPU alert
        if self.metrics.get('cpu', {}).get('percent', 0) > 90:
            alerts_triggered.append({
                'type': 'high_cpu',
                'value': self.metrics['cpu']['percent'],
                'threshold': 90
            })
        
        # Memory alert
        if self.metrics.get('memory', {}).get('percent', 0) > 90:
            alerts_triggered.append({
                'type': 'high_memory',
                'value': self.metrics['memory']['percent'],
                'threshold': 90
            })
        
        # Disk alert
        if self.metrics.get('disk', {}).get('percent', 0) > 95:
            alerts_triggered.append({
                'type': 'low_disk',
                'value': self.metrics['disk']['percent'],
                'threshold': 95
            })
        
        # Trigger callbacks
        for alert in alerts_triggered:
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    print(f"Alert callback error: {e}")
    
    def register_alert_callback(self, callback: Callable):
        """Register alert callback"""
        self.alert_callbacks.append(callback)
    
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics
        }
    
    def get_health_score(self) -> Dict:
        """Calculate system health score"""
        cpu_score = 100 - self.metrics.get('cpu', {}).get('percent', 0)
        memory_score = 100 - self.metrics.get('memory', {}).get('percent', 0)
        disk_score = 100 - self.metrics.get('disk', {}).get('percent', 0)
        
        overall_score = (cpu_score + memory_score + disk_score) / 3
        
        return {
            "overall_score": round(overall_score, 2),
            "cpu_score": round(cpu_score, 2),
            "memory_score": round(memory_score, 2),
            "disk_score": round(disk_score, 2),
            "status": "healthy" if overall_score > 70 else "warning" if overall_score > 50 else "critical"
        }
