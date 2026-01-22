"""
Real-Time Collaboration - Team workspaces and shared commands
"""
import os
import json
import threading
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
from refactoring.code_deduplication import CommonUtils


class RealtimeCollaboration:
    """Real-time collaboration system for JARVIS"""
    
    def __init__(self, workspace_file: str = "data/workspaces.json"):
        self.workspace_file = workspace_file
        self.workspaces: Dict[str, Dict] = {}
        self.active_sessions: Dict[str, List[str]] = defaultdict(list)
        self.activity_feeds: Dict[str, List[Dict]] = defaultdict(list)
        self.comments: Dict[str, List[Dict]] = defaultdict(list)
        self.lock = threading.Lock()
        self._load_workspaces()
    
    def create_workspace(self, workspace_id: str, name: str, 
                        owner: str, description: str = "") -> Dict:
        """Create a new workspace"""
        workspace = {
            "id": workspace_id,
            "name": name,
            "owner": owner,
            "description": description,
            "members": [owner],
            "created": datetime.now().isoformat(),
            "settings": {
                "public": False,
                "allow_invites": True
            }
        }
        
        with self.lock:
            self.workspaces[workspace_id] = workspace
            self._save_workspaces()
        
        return {"success": True, "workspace_id": workspace_id}
    
    def join_workspace(self, workspace_id: str, user_id: str) -> Dict:
        """Join a workspace"""
        with self.lock:
            if workspace_id not in self.workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.workspaces[workspace_id]
            if user_id not in workspace["members"]:
                workspace["members"].append(user_id)
                self._save_workspaces()
            
            if user_id not in self.active_sessions[workspace_id]:
                self.active_sessions[workspace_id].append(user_id)
            
            # Add to activity feed
            self._add_activity(workspace_id, {
                "type": "user_joined",
                "user": user_id,
                "timestamp": datetime.now().isoformat()
            })
        
        return {"success": True, "workspace_id": workspace_id}
    
    def share_command(self, workspace_id: str, user_id: str, 
                     command: str, result: str) -> Dict:
        """Share a command with workspace"""
        with self.lock:
            if workspace_id not in self.workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            # Add to activity feed
            self._add_activity(workspace_id, {
                "type": "command_executed",
                "user": user_id,
                "command": command,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
        
        return {"success": True}
    
    def add_comment(self, workspace_id: str, user_id: str, 
                   target_id: str, comment: str) -> Dict:
        """Add a comment to an activity"""
        comment_entry = {
            "id": f"comment_{len(self.comments[target_id])}",
            "user": user_id,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        
        with self.lock:
            self.comments[target_id].append(comment_entry)
        
        return {"success": True, "comment": comment_entry}
    
    def get_activity_feed(self, workspace_id: str, limit: int = 50) -> List[Dict]:
        """Get activity feed for workspace"""
        return self.activity_feeds[workspace_id][-limit:]
    
    def get_active_users(self, workspace_id: str) -> List[str]:
        """Get active users in workspace"""
        return self.active_sessions.get(workspace_id, [])
    
    def _add_activity(self, workspace_id: str, activity: Dict):
        """Add activity to feed"""
        self.activity_feeds[workspace_id].append(activity)
        # Keep only last 1000 activities
        if len(self.activity_feeds[workspace_id]) > 1000:
            self.activity_feeds[workspace_id] = self.activity_feeds[workspace_id][-1000:]
    
    def _load_workspaces(self):
        """Load workspaces from file"""
        self.workspaces = CommonUtils.safe_json_load(self.workspace_file, {})
    
    def _save_workspaces(self):
        """Save workspaces to file"""
        CommonUtils.safe_json_save(self.workspace_file, self.workspaces)
