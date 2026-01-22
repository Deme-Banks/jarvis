"""
Quick Actions Menu - Fast action access
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class QuickActionsMenu:
    """Quick actions menu system"""
    
    def __init__(self, actions_file: str = "config/quick_actions.json"):
        self.actions_file = actions_file
        self.actions = self._load_actions()
        self._add_default_actions()
    
    def _load_actions(self) -> Dict:
        """Load quick actions"""
        if os.path.exists(self.actions_file):
            try:
                with open(self.actions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_actions(self):
        """Save quick actions"""
        os.makedirs(os.path.dirname(self.actions_file), exist_ok=True)
        with open(self.actions_file, 'w') as f:
            json.dump(self.actions, f, indent=2)
    
    def _add_default_actions(self):
        """Add default quick actions"""
        defaults = {
            "create_keylogger": {
                "name": "Create Keylogger",
                "command": "create keylogger",
                "category": "security",
                "icon": "🔒"
            },
            "scan_network": {
                "name": "Scan Network",
                "command": "scan network",
                "category": "security",
                "icon": "🌐"
            },
            "generate_image": {
                "name": "Generate Image",
                "command": "generate image",
                "category": "ai",
                "icon": "🎨"
            },
            "github_commit": {
                "name": "GitHub Commit",
                "command": "github commit",
                "category": "integration",
                "icon": "💻"
            },
            "system_info": {
                "name": "System Info",
                "command": "get system information",
                "category": "system",
                "icon": "💻"
            }
        }
        
        for key, action in defaults.items():
            if key not in self.actions:
                self.actions[key] = action
        
        self._save_actions()
    
    def add_action(self, key: str, name: str, command: str,
                   category: str = "general", icon: str = "⚡") -> Dict:
        """Add a quick action"""
        self.actions[key] = {
            "name": name,
            "command": command,
            "category": category,
            "icon": icon,
            "created": datetime.now().isoformat()
        }
        
        self._save_actions()
        return {"success": True, "action": key}
    
    def get_actions_by_category(self, category: Optional[str] = None) -> Dict:
        """Get actions grouped by category"""
        if category:
            return {
                category: [
                    action for key, action in self.actions.items()
                    if action.get("category") == category
                ]
            }
        
        categories = {}
        for key, action in self.actions.items():
            cat = action.get("category", "general")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(action)
        
        return categories
    
    def execute_action(self, action_key: str) -> Dict:
        """Execute a quick action"""
        if action_key not in self.actions:
            return {"error": f"Action '{action_key}' not found"}
        
        action = self.actions[action_key]
        command = action["command"]
        
        return {
            "success": True,
            "action": action_key,
            "command": command,
            "message": f"Executing: {action['name']}"
        }
