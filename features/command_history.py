"""
Command History and Favorites System
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from collections import deque


class CommandHistory:
    """Command history with search and favorites"""
    
    def __init__(self, history_file: str = "./memory/command_history.json", 
                 max_history: int = 1000):
        self.history_file = history_file
        self.max_history = max_history
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        self.history = deque(maxlen=max_history)
        self.favorites = []
        self._load_history()
    
    def _load_history(self):
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.history = deque(data.get('history', []), maxlen=self.max_history)
                    self.favorites = data.get('favorites', [])
            except:
                pass
    
    def _save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump({
                    'history': list(self.history),
                    'favorites': self.favorites
                }, f, indent=2)
        except:
            pass
    
    def add(self, command: str, response: str, success: bool = True):
        """Add command to history"""
        entry = {
            "command": command,
            "response": response[:200],  # Truncate long responses
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(entry)
        
        # Save periodically
        if len(self.history) % 10 == 0:
            self._save_history()
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent commands"""
        return list(self.history)[-limit:]
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search history"""
        query_lower = query.lower()
        matches = [
            entry for entry in self.history
            if query_lower in entry["command"].lower() or 
               query_lower in entry.get("response", "").lower()
        ]
        return matches[-limit:]
    
    def add_favorite(self, command: str, name: Optional[str] = None):
        """Add command to favorites"""
        favorite = {
            "name": name or command[:50],
            "command": command,
            "added_at": datetime.now().isoformat()
        }
        
        # Remove if already exists
        self.favorites = [f for f in self.favorites if f["command"] != command]
        self.favorites.append(favorite)
        self._save_history()
    
    def remove_favorite(self, command: str):
        """Remove from favorites"""
        self.favorites = [f for f in self.favorites if f["command"] != command]
        self._save_history()
    
    def get_favorites(self) -> List[Dict]:
        """Get all favorites"""
        return self.favorites
    
    def get_stats(self) -> Dict:
        """Get history statistics"""
        return {
            "total_commands": len(self.history),
            "favorites_count": len(self.favorites),
            "success_rate": sum(1 for e in self.history if e.get("success", False)) / max(len(self.history), 1)
        }
