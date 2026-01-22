"""
Quick Wins - Low effort, high value features
"""
import os
import random
from typing import Dict, List, Optional
from datetime import datetime
from utils.cache_optimizer import SmartCache


class QuickActions:
    """Quick action sets for common tasks"""
    
    def __init__(self):
        self.action_sets: Dict[str, List[str]] = {
            "security_scan": [
                "scan network",
                "check vulnerabilities",
                "analyze logs",
                "generate security report"
            ],
            "daily_backup": [
                "backup data",
                "verify backup",
                "clean old backups",
                "notify completion"
            ],
            "system_check": [
                "get system information",
                "check disk space",
                "check memory usage",
                "show performance metrics"
            ]
        }
        self.cache = SmartCache()
    
    def execute_action_set(self, set_name: str) -> Dict:
        """Execute a quick action set"""
        if set_name not in self.action_sets:
            return {"error": f"Action set '{set_name}' not found"}
        
        actions = self.action_sets[set_name]
        results = []
        
        for action in actions:
            # In production, would execute actual commands
            results.append({
                "action": action,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "success": True,
            "set_name": set_name,
            "results": results
        }
    
    def create_custom_set(self, set_name: str, actions: List[str]) -> Dict:
        """Create a custom action set"""
        self.action_sets[set_name] = actions
        return {"success": True, "set_name": set_name}


class CommandTemplates:
    """Pre-filled command templates"""
    
    def __init__(self):
        self.templates: Dict[str, Dict] = {
            "create_keylogger": {
                "command": "create keylogger",
                "params": {
                    "output": "keylog.txt",
                    "stealth": True
                }
            },
            "network_scan": {
                "command": "scan network",
                "params": {
                    "target": "192.168.1.0/24",
                    "ports": "1-1000"
                }
            },
            "system_info": {
                "command": "get system information",
                "params": {}
            }
        }
    
    def get_template(self, template_name: str) -> Dict:
        """Get a command template"""
        return self.templates.get(template_name, {})
    
    def create_template(self, name: str, command: str, params: Dict = None) -> Dict:
        """Create a new template"""
        self.templates[name] = {
            "command": command,
            "params": params or {}
        }
        return {"success": True, "template": name}


class SmartSuggestions:
    """Smart command suggestions based on context"""
    
    def __init__(self):
        self.cache = SmartCache()
        self.suggestion_history: List[str] = []
    
    def get_suggestions(self, partial_command: str, context: Dict = None) -> List[str]:
        """Get command suggestions"""
        suggestions = []
        
        # Common commands
        common = [
            "create keylogger",
            "scan network",
            "get system information",
            "show performance metrics",
            "deploy payload to usb",
            "run ddos test",
            "generate code",
            "analyze video"
        ]
        
        # Filter by partial match
        for cmd in common:
            if partial_command.lower() in cmd.lower():
                suggestions.append(cmd)
        
        # Add context-based suggestions
        if context:
            if context.get("time_of_day") == "morning":
                suggestions.append("daily backup")
            if context.get("security_mode"):
                suggestions.extend([
                    "security scan",
                    "check vulnerabilities",
                    "analyze logs"
                ])
        
        return suggestions[:5]  # Return top 5


class SoundThemes:
    """Sound effect themes"""
    
    def __init__(self):
        self.themes: Dict[str, Dict[str, str]] = {
            "classic": {
                "success": "classic_success.wav",
                "error": "classic_error.wav",
                "notification": "classic_notification.wav"
            },
            "modern": {
                "success": "modern_success.wav",
                "error": "modern_error.wav",
                "notification": "modern_notification.wav"
            },
            "cyber": {
                "success": "cyber_success.wav",
                "error": "cyber_error.wav",
                "notification": "cyber_notification.wav"
            }
        }
        self.current_theme = "classic"
    
    def set_theme(self, theme_name: str) -> Dict:
        """Set sound theme"""
        if theme_name not in self.themes:
            return {"error": f"Theme '{theme_name}' not found"}
        
        self.current_theme = theme_name
        return {"success": True, "theme": theme_name}
    
    def get_sound(self, sound_type: str) -> Optional[str]:
        """Get sound file for type"""
        theme = self.themes.get(self.current_theme, {})
        return theme.get(sound_type)
