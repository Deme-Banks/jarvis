"""
Expanded Voice Shortcuts - More shortcuts and macros
"""
from typing import Dict, List
from features.command_aliases import CommandAliases


class ExpandedVoiceShortcuts:
    """Expanded voice shortcuts library"""
    
    def __init__(self):
        self.aliases = CommandAliases()
        self._add_expanded_shortcuts()
    
    def _add_expanded_shortcuts(self):
        """Add expanded shortcuts"""
        expanded = {
            # Security shortcuts
            "secure": "security scan",
            "hack": "run penetration test",
            "crack": "create brute force",
            "exploit": "scan for vulnerabilities",
            
            # System shortcuts
            "info": "get system information",
            "stats": "show performance metrics",
            "health": "system health check",
            "clean": "clean temporary files",
            
            # Network shortcuts
            "ping": "test connectivity",
            "trace": "trace route",
            "whois": "whois lookup",
            "dns": "dns lookup",
            
            # Development shortcuts
            "code": "generate code",
            "build": "build project",
            "test": "run tests",
            "deploy": "deploy application",
            
            # AI shortcuts
            "think": "analyze with AI",
            "learn": "train model",
            "predict": "make prediction",
            "generate": "generate content",
            
            # Automation shortcuts
            "auto": "create automation",
            "schedule": "schedule task",
            "workflow": "create workflow",
            "trigger": "set trigger",
            
            # Collaboration shortcuts
            "share": "share with team",
            "collab": "start collaboration",
            "workspace": "create workspace",
            "team": "team commands",
            
            # Integration shortcuts
            "github": "github action",
            "jira": "jira ticket",
            "slack": "slack message",
            "discord": "discord message",
            
            # Quick actions
            "quick": "run quick action",
            "template": "use template",
            "macro": "execute macro",
            "batch": "batch operation"
        }
        
        for shortcut, command in expanded.items():
            if shortcut not in self.aliases.aliases:
                self.aliases.add_alias(shortcut, command)
    
    def get_all_shortcuts(self) -> Dict[str, str]:
        """Get all shortcuts"""
        return self.aliases.aliases.copy()
    
    def count_shortcuts(self) -> int:
        """Count total shortcuts"""
        return len(self.aliases.aliases)
