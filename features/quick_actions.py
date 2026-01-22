"""
Quick Actions - Pre-defined action sets
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class QuickActions:
    """Quick action sets for common tasks"""
    
    def __init__(self, actions_file: str = "config/quick_actions.json"):
        self.actions_file = actions_file
        self.actions = self._load_actions()
        self._add_default_actions()
    
    def _load_actions(self) -> Dict:
        """Load quick actions"""
        default_actions = {
            "security_scan": {
                "name": "Security Scan",
                "description": "Run comprehensive security scan",
                "commands": [
                    "scan network 192.168.1.0/24",
                    "check system health",
                    "run vulnerability scan"
                ]
            },
            "daily_backup": {
                "name": "Daily Backup",
                "description": "Create daily system backup",
                "commands": [
                    "create backup",
                    "verify backup integrity"
                ]
            },
            "performance_check": {
                "name": "Performance Check",
                "description": "Check system performance",
                "commands": [
                    "show performance metrics",
                    "check system health",
                    "analyze resource usage"
                ]
            },
            "malware_test": {
                "name": "Malware Test Suite",
                "description": "Run malware testing suite",
                "commands": [
                    "create keylogger",
                    "create reverse shell",
                    "test evasion techniques"
                ]
            }
        }
        
        if os.path.exists(self.actions_file):
            try:
                with open(self.actions_file, 'r') as f:
                    custom_actions = json.load(f)
                    default_actions.update(custom_actions)
            except:
                pass
        
        return default_actions
    
    def _save_actions(self):
        """Save quick actions"""
        os.makedirs(os.path.dirname(self.actions_file), exist_ok=True)
        with open(self.actions_file, 'w') as f:
            json.dump(self.actions, f, indent=2)
    
    def _add_default_actions(self):
        """Add default quick actions"""
        # Already in _load_actions, but ensure they're saved
        self._save_actions()
    
    def create_action(self, action_id: str, name: str, description: str,
                     commands: List[str]) -> Dict:
        """Create a new quick action"""
        self.actions[action_id] = {
            "name": name,
            "description": description,
            "commands": commands,
            "created": datetime.now().isoformat()
        }
        
        self._save_actions()
        return {"success": True, "action_id": action_id}
    
    def get_action(self, action_id: str) -> Optional[Dict]:
        """Get a quick action"""
        return self.actions.get(action_id)
    
    def list_actions(self) -> List[Dict]:
        """List all quick actions"""
        return [
            {
                "id": action_id,
                "name": action["name"],
                "description": action.get("description", ""),
                "commands_count": len(action.get("commands", []))
            }
            for action_id, action in self.actions.items()
        ]
    
    def execute_action(self, action_id: str) -> List[str]:
        """Get commands for an action (to be executed)"""
        action = self.get_action(action_id)
        if action:
            return action.get("commands", [])
        return []
    
    def delete_action(self, action_id: str) -> Dict:
        """Delete a quick action"""
        if action_id in self.actions:
            del self.actions[action_id]
            self._save_actions()
            return {"success": True, "action_id": action_id}
        return {"error": f"Action '{action_id}' not found"}
