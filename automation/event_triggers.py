"""
Event Triggers - React to system events
"""
import os
import time
import threading
from typing import Dict, List, Callable, Optional
from datetime import datetime
import psutil


class EventTriggerSystem:
    """System event trigger system"""
    
    def __init__(self):
        self.triggers: Dict[str, List[Callable]] = {}
        self.running = False
        self.monitor_thread = None
    
    def register_trigger(self, event_type: str, callback: Callable):
        """Register a callback for an event type"""
        if event_type not in self.triggers:
            self.triggers[event_type] = []
        self.triggers[event_type].append(callback)
    
    def trigger_event(self, event_type: str, data: Dict):
        """Trigger an event"""
        if event_type in self.triggers:
            for callback in self.triggers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event callback: {e}")
    
    def start_monitoring(self):
        """Start monitoring system events"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
    
    def _monitor_loop(self):
        """Monitor loop for system events"""
        last_cpu = 0
        last_memory = 0
        
        while self.running:
            try:
                # CPU monitoring
                cpu_percent = psutil.cpu_percent(interval=1)
                if cpu_percent > 80 and last_cpu <= 80:
                    self.trigger_event("high_cpu", {"cpu_percent": cpu_percent})
                last_cpu = cpu_percent
                
                # Memory monitoring
                memory_percent = psutil.virtual_memory().percent
                if memory_percent > 80 and last_memory <= 80:
                    self.trigger_event("high_memory", {"memory_percent": memory_percent})
                last_memory = memory_percent
                
                # Disk monitoring
                disk_percent = psutil.disk_usage('/').percent
                if disk_percent > 90:
                    self.trigger_event("low_disk", {"disk_percent": disk_percent})
                
                time.sleep(5)
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)
