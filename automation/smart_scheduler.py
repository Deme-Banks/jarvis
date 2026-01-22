"""
Smart Scheduler - Intelligent task scheduling - Optimized
"""
from utils.cache_optimizer import SmartCache
from refactoring.code_deduplication import CommonUtils
import os
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import threading
import time
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    schedule = None


class SmartScheduler:
    """Intelligent task scheduling system"""
    
    def __init__(self, tasks_file: str = "data/scheduled_tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = self._load_tasks()
        self.running = False
        self.scheduler_thread = None
    
    def _load_tasks(self) -> Dict:
        """Load scheduled tasks"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_tasks(self):
        """Save scheduled tasks"""
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def schedule_task(self, task_id: str, command: str, schedule_type: str,
                     schedule_value: str, enabled: bool = True) -> Dict:
        """Schedule a task"""
        task = {
            "id": task_id,
            "command": command,
            "schedule_type": schedule_type,  # daily, hourly, weekly, custom
            "schedule_value": schedule_value,  # time, interval, etc.
            "enabled": enabled,
            "created": datetime.now().isoformat(),
            "last_run": None,
            "run_count": 0
        }
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        # Register with schedule library
        self._register_schedule(task)
        
        return {"success": True, "task_id": task_id}
    
    def _register_schedule(self, task: Dict):
        """Register task with schedule library"""
        schedule_type = task["schedule_type"]
        schedule_value = task["schedule_value"]
        command = task["command"]
        
        def run_task():
            task["last_run"] = datetime.now().isoformat()
            task["run_count"] = task.get("run_count", 0) + 1
            self._save_tasks()
            # Execute command (would integrate with orchestrator)
            print(f"Executing scheduled task: {command}")
        
        if not SCHEDULE_AVAILABLE:
            return  # Schedule library not available
        
        if schedule_type == "daily":
            schedule.every().day.at(schedule_value).do(run_task)
        elif schedule_type == "hourly":
            schedule.every(int(schedule_value)).hours.do(run_task)
        elif schedule_type == "weekly":
            schedule.every().week.at(schedule_value).do(run_task)
        elif schedule_type == "minute":
            schedule.every(int(schedule_value)).minutes.do(run_task)
    
    def start_scheduler(self):
        """Start the scheduler"""
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
    
    def _scheduler_loop(self):
        """Scheduler execution loop"""
        if not SCHEDULE_AVAILABLE:
            return
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def list_tasks(self) -> List[Dict]:
        """List all scheduled tasks"""
        return list(self.tasks.values())
    
    def remove_task(self, task_id: str) -> Dict:
        """Remove a scheduled task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save_tasks()
            if SCHEDULE_AVAILABLE:
                schedule.clear(task_id)
            return {"success": True, "task_id": task_id}
        return {"error": f"Task '{task_id}' not found"}
