"""
Command History Search - Search past commands
"""
import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from refactoring.code_deduplication import CommonUtils


class CommandHistorySearch:
    """Command history search system"""
    
    def __init__(self, history_file: str = "memory/command_history.json"):
        self.history_file = history_file
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        self.history: List[Dict] = []
        self._load_history()
    
    def add_command(self, command: str, response: str = "", success: bool = True):
        """Add command to history"""
        entry = {
            "command": command,
            "response": response,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(entry)
        self._save_history()
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search command history"""
        query_lower = query.lower()
        results = []
        
        for entry in reversed(self.history):
            if query_lower in entry["command"].lower():
                results.append(entry)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent commands"""
        return list(reversed(self.history[-limit:]))
    
    def get_by_date(self, date: str) -> List[Dict]:
        """Get commands by date"""
        return [
            entry for entry in self.history
            if entry["timestamp"].startswith(date)
        ]
    
    def clear_history(self):
        """Clear command history"""
        self.history = []
        self._save_history()
    
    def _load_history(self):
        """Load history from file"""
        self.history = CommonUtils.safe_json_load(self.history_file, [])
    
    def _save_history(self):
        """Save history to file"""
        CommonUtils.safe_json_save(self.history_file, self.history)
