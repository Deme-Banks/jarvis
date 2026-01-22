"""
Multi-User Learning System - Separate profiles for different users
"""
import os
import json
from typing import Dict, Optional
from learning.memory import MemorySystem
from datetime import datetime


class MultiUserLearning:
    """Multi-user learning with separate profiles"""
    
    def __init__(self, base_memory_dir: str = "./memory"):
        self.base_memory_dir = base_memory_dir
        self.current_user = None
        self.users_file = os.path.join(base_memory_dir, "users.json")
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """Load user profiles"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_users(self):
        """Save user profiles"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def create_user(self, user_id: str, name: Optional[str] = None) -> Dict:
        """Create a new user profile"""
        if user_id in self.users:
            return {"error": "User already exists"}
        
        user_data = {
            "name": name or user_id,
            "created_at": datetime.now().isoformat(),
            "memory_dir": os.path.join(self.base_memory_dir, f"user_{user_id}"),
            "stats": {
                "total_interactions": 0,
                "preferences_count": 0,
                "knowledge_topics": 0
            }
        }
        
        self.users[user_id] = user_data
        self._save_users()
        
        # Create user-specific memory system
        os.makedirs(user_data["memory_dir"], exist_ok=True)
        
        return {"success": True, "user": user_data}
    
    def switch_user(self, user_id: str) -> MemorySystem:
        """Switch to a user profile"""
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found. Create user first.")
        
        self.current_user = user_id
        user_data = self.users[user_id]
        memory_dir = user_data["memory_dir"]
        
        return MemorySystem(memory_dir=memory_dir)
    
    def get_user_stats(self, user_id: Optional[str] = None) -> Dict:
        """Get statistics for a user"""
        user_id = user_id or self.current_user
        if not user_id or user_id not in self.users:
            return {}
        
        user_data = self.users[user_id]
        memory = MemorySystem(memory_dir=user_data["memory_dir"])
        
        return {
            "user_id": user_id,
            "name": user_data["name"],
            "created_at": user_data["created_at"],
            "total_interactions": len(memory.conversations),
            "preferences": len(memory.preferences),
            "knowledge_topics": len(memory.knowledge),
            "patterns": len(memory.patterns),
            "user_style": memory.analyze_user_style()
        }
    
    def list_users(self) -> list:
        """List all users"""
        return list(self.users.keys())
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user profile"""
        if user_id not in self.users:
            return False
        
        # Remove user data
        user_data = self.users[user_id]
        memory_dir = user_data["memory_dir"]
        
        if os.path.exists(memory_dir):
            import shutil
            shutil.rmtree(memory_dir)
        
        del self.users[user_id]
        self._save_users()
        
        if self.current_user == user_id:
            self.current_user = None
        
        return True
    
    def identify_user(self, voice_sample: Optional[str] = None, 
                     text_pattern: Optional[str] = None) -> Optional[str]:
        """Identify user from voice or text patterns"""
        # Simple implementation - can be enhanced with voice recognition
        if text_pattern:
            # Check for user-specific patterns
            for user_id, user_data in self.users.items():
                memory = MemorySystem(memory_dir=user_data["memory_dir"])
                style = memory.analyze_user_style()
                
                # Simple pattern matching (can be enhanced)
                if style.get("avg_message_length", 0) > 0:
                    # Could use ML for better identification
                    pass
        
        return self.current_user  # Default to current user
