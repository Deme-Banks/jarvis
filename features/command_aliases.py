"""
Command Aliases and Macros
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class CommandAliases:
    """Command aliases and macros"""
    
    def __init__(self, aliases_file: str = "./memory/aliases.json"):
        self.aliases_file = aliases_file
        os.makedirs(os.path.dirname(aliases_file), exist_ok=True)
        self.aliases = self._load_aliases()
        self.macros = self._load_macros()
        self._add_default_aliases()
    
    def _load_aliases(self) -> Dict:
        """Load aliases"""
        if os.path.exists(self.aliases_file):
            try:
                with open(self.aliases_file, 'r') as f:
                    data = json.load(f)
                    return data.get('aliases', {})
            except:
                return {}
        return {}
    
    def _load_macros(self) -> Dict:
        """Load macros"""
        if os.path.exists(self.aliases_file):
            try:
                with open(self.aliases_file, 'r') as f:
                    data = json.load(f)
                    return data.get('macros', {})
            except:
                return {}
        return {}
    
    def _save(self):
        """Save aliases and macros"""
        with open(self.aliases_file, 'w') as f:
            json.dump({
                'aliases': self.aliases,
                'macros': self.macros
            }, f, indent=2)
    
    def _add_default_aliases(self):
        """Add default aliases if not present"""
        default_aliases = {
            "kl": "create keylogger",
            "rs": "create reverse shell",
            "ddos": "run ddos test",
            "scan": "scan network",
            "usb": "deploy payload to usb",
            "sysinfo": "get system information",
            "perf": "show performance metrics",
            "ai code": "generate code",
            "ai malware": "AI generate malware",
            "ios crack": "create iOS PIN brute force",
            "android crack": "create Android PIN brute force",
            "img": "generate image",
            "video": "analyze video",
            "github": "github commit",
            "jira": "jira create issue",
            "cal": "calendar create event",
            "pt": "run penetration test",
            "threat": "check threat intelligence",
            "theme": "change theme"
        }
        
        for alias, command in default_aliases.items():
            if alias not in self.aliases:
                self.aliases[alias] = command
        
        self._save()
        """Add default aliases"""
        defaults = {
            'kl': 'create a keylogger',
            'rs': 'create a reverse shell',
            'rat': 'create a RAT',
            'scan': 'scan network 192.168.1.0/24',
            'test': 'test TCP flood on localhost',
            'health': 'check system health',
            'stats': 'show statistics',
            'backup': 'create backup',
            'help': 'what can you do'
        }
        
        for alias, command in defaults.items():
            if alias not in self.aliases:
                self.aliases[alias] = command
        
        self._save()
    
    def expand_alias(self, command: str) -> str:
        """Expand alias in command"""
        words = command.split()
        expanded = []
        
        for word in words:
            if word in self.aliases:
                expanded.append(self.aliases[word])
            else:
                expanded.append(word)
        
        return ' '.join(expanded)
    
    def add_alias(self, alias: str, command: str):
        """Add alias"""
        self.aliases[alias.lower()] = command
        self._save()
    
    def remove_alias(self, alias: str):
        """Remove alias"""
        if alias.lower() in self.aliases:
            del self.aliases[alias.lower()]
            self._save()
    
    def create_macro(self, name: str, commands: List[str]):
        """Create macro (sequence of commands)"""
        self.macros[name.lower()] = {
            'commands': commands,
            'created': datetime.now().isoformat()
        }
        self._save()
    
    def execute_macro(self, name: str) -> List[str]:
        """Get macro commands"""
        if name.lower() in self.macros:
            return self.macros[name.lower()]['commands']
        return []
    
    def list_aliases(self) -> Dict:
        """List all aliases"""
        return dict(self.aliases)
    
    def list_macros(self) -> Dict:
        """List all macros"""
        return dict(self.macros)
