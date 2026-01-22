"""
Command Autocomplete - Smart command completion
"""
import os
import json
from typing import List, Dict, Optional
from collections import Counter


class CommandAutocomplete:
    """Command autocomplete system"""
    
    def __init__(self, history_file: str = "data/command_history.json"):
        self.history_file = history_file
        self.commands = self._load_commands()
        self.command_frequency = Counter()
        self._build_frequency()
    
    def _load_commands(self) -> List[str]:
        """Load command history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    return data.get("commands", [])
            except:
                return []
        return []
    
    def _build_frequency(self):
        """Build command frequency map"""
        for cmd in self.commands:
            words = cmd.split()
            for word in words:
                self.command_frequency[word.lower()] += 1
    
    def autocomplete(self, partial_command: str, max_suggestions: int = 5) -> List[str]:
        """Get autocomplete suggestions"""
        if not partial_command:
            # Return most common commands
            return [cmd for cmd, _ in self.command_frequency.most_common(max_suggestions)]
        
        partial_lower = partial_command.lower()
        suggestions = []
        
        # Exact matches first
        for cmd in self.commands:
            if cmd.lower().startswith(partial_lower):
                suggestions.append(cmd)
                if len(suggestions) >= max_suggestions:
                    break
        
        # Partial word matches
        if len(suggestions) < max_suggestions:
            words = partial_command.split()
            if words:
                last_word = words[-1].lower()
                for cmd in self.commands:
                    cmd_words = cmd.lower().split()
                    for cmd_word in cmd_words:
                        if cmd_word.startswith(last_word) and cmd not in suggestions:
                            suggestions.append(cmd)
                            if len(suggestions) >= max_suggestions:
                                break
        
        # Frequency-based suggestions
        if len(suggestions) < max_suggestions:
            for word, freq in self.command_frequency.most_common():
                if word.startswith(partial_lower) and word not in suggestions:
                    suggestions.append(word)
                    if len(suggestions) >= max_suggestions:
                        break
        
        return suggestions[:max_suggestions]
    
    def add_command(self, command: str):
        """Add command to history"""
        if command not in self.commands:
            self.commands.append(command)
            self._save_commands()
            self._build_frequency()
    
    def _save_commands(self):
        """Save commands to file"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump({"commands": self.commands}, f, indent=2)
    
    def get_suggestions(self, partial: str) -> Dict:
        """Get autocomplete suggestions with metadata"""
        suggestions = self.autocomplete(partial)
        return {
            "suggestions": suggestions,
            "count": len(suggestions),
            "partial": partial
        }
