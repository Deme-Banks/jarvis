"""
Scheduled Task System
"""
import schedule
import time
import threading
from typing import Dict, List, Callable, Optional
from datetime import datetime
import json
import os


class ScheduledTasks:
    """Scheduled task management"""
    
    def __init__(self, tasks_file: str = "./memory/scheduled_tasks.json"):
        self.tasks_file = tasks_file
        os.makedirs(os.path.dirname(tasks_file), exist_ok=True)
        self.tasks = {}
        self.running = False
        self.scheduler_thread = None
        self._load_tasks()
    
    def _load_tasks(self):
        """Load scheduled tasks"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = {}
    
    def _save_tasks(self):
        """Save scheduled tasks"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, name: str, schedule_str: str, func: Callable, *args, **kwargs) -> bool:
        """Add scheduled task"""
        # Parse schedule string
        # Format: "daily", "hourly", "10:30", "every 5 minutes", etc.
        
        if schedule_str == "daily":
            schedule.every().day.do(func, *args, **kwargs)
        elif schedule_str == "hourly":
            schedule.every().hour.do(func, *args, **kwargs)
        elif schedule_str.startswith("every "):
            # "every 5 minutes", "every 2 hours"
            parts = schedule_str.split()
            if len(parts) >= 3:
                interval = int(parts[1])
                unit = parts[2]
                if unit.startswith("minute"):
                    schedule.every(interval).minutes.do(func, *args, **kwargs)
                elif unit.startswith("hour"):
                    schedule.every(interval).hours.do(func, *args, **kwargs)
        elif ":" in schedule_str:
            # Time like "10:30"
            schedule.every().day.at(schedule_str).do(func, *args, **kwargs)
        else:
            return False
        
        self.tasks[name] = {
            'schedule': schedule_str,
            'created': datetime.now().isoformat(),
            'enabled': True
        }
        self._save_tasks()
        
        return True
    
    def remove_task(self, name: str) -> bool:
        """Remove scheduled task"""
        if name in self.tasks:
            del self.tasks[name]
            self._save_tasks()
            # Note: schedule library doesn't have easy removal, would need to clear and re-add
            return True
        return False
    
    def start(self):
        """Start scheduler"""
        if self.running:
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
    
    def _run_scheduler(self):
        """Run scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def list_tasks(self) -> List[Dict]:
        """List all scheduled tasks"""
        return [
            {
                'name': name,
                'schedule': task['schedule'],
                'enabled': task.get('enabled', True),
                'created': task.get('created')
            }
            for name, task in self.tasks.items()
        ]
