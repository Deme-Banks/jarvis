"""
Voice Shortcuts and Command Aliases
"""
from typing import Dict, Optional
import json
import os


class VoiceShortcuts:
    """Voice shortcuts and command aliases"""
    
    def __init__(self, shortcuts_file: str = "./memory/shortcuts.json"):
        self.shortcuts_file = shortcuts_file
        os.makedirs(os.path.dirname(shortcuts_file), exist_ok=True)
        self.shortcuts = self._load_shortcuts()
        self._add_default_shortcuts()
    
    def _load_shortcuts(self) -> Dict[str, str]:
        """Load shortcuts from file"""
        if os.path.exists(self.shortcuts_file):
            try:
                with open(self.shortcuts_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_shortcuts(self):
        """Save shortcuts to file"""
        with open(self.shortcuts_file, 'w') as f:
            json.dump(self.shortcuts, f, indent=2)
    
    def _add_default_shortcuts(self):
        """Add default shortcuts"""
        defaults = {
            "kl": "create a keylogger",
            "rs": "create a reverse shell",
            "rat": "create a RAT",
            "usb": "detect USB drives",
            "test": "run TCP flood test on localhost",
            "help": "what can you do",
            "stats": "what have you learned",
            "history": "show command history",
            "favs": "show favorites"
        }
        
        for shortcut, command in defaults.items():
            if shortcut not in self.shortcuts:
                self.shortcuts[shortcut] = command
        
        self._save_shortcuts()
    
    def expand(self, text: str) -> str:
        """Expand shortcuts in text"""
        words = text.split()
        expanded = []
        
        for word in words:
            if word.lower() in self.shortcuts:
                expanded.append(self.shortcuts[word.lower()])
            else:
                expanded.append(word)
        
        return ' '.join(expanded)
    
    def add_shortcut(self, shortcut: str, command: str):
        """Add custom shortcut"""
        self.shortcuts[shortcut.lower()] = command
        self._save_shortcuts()
    
    def remove_shortcut(self, shortcut: str):
        """Remove shortcut"""
        if shortcut.lower() in self.shortcuts:
            del self.shortcuts[shortcut.lower()]
            self._save_shortcuts()
    
    def list_shortcuts(self) -> Dict[str, str]:
        """List all shortcuts"""
        return dict(self.shortcuts)
