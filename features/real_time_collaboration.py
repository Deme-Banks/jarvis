"""
Real-time Collaboration Features
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import threading
import time


class RealTimeCollaboration:
    """Real-time collaboration features"""
    
    def __init__(self, session_file: str = "./memory/collaboration.json"):
        self.session_file = session_file
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        self.active_sessions = {}
        self.shared_resources = {}
        self.lock = threading.Lock()
    
    def create_session(self, session_id: str, participants: List[str]) -> Dict:
        """Create collaboration session"""
        with self.lock:
            self.active_sessions[session_id] = {
                'participants': participants,
                'created': datetime.now().isoformat(),
                'shared_commands': [],
                'shared_results': []
            }
            self._save_sessions()
        
        return {
            'success': True,
            'session_id': session_id,
            'participants': participants
        }
    
    def share_command(self, session_id: str, command: str, user: str) -> Dict:
        """Share command in session"""
        if session_id not in self.active_sessions:
            return {'success': False, 'error': 'Session not found'}
        
        with self.lock:
            entry = {
                'command': command,
                'user': user,
                'timestamp': datetime.now().isoformat()
            }
            self.active_sessions[session_id]['shared_commands'].append(entry)
            self._save_sessions()
        
        return {'success': True, 'command': entry}
    
    def share_result(self, session_id: str, result: str, command: str) -> Dict:
        """Share result in session"""
        if session_id not in self.active_sessions:
            return {'success': False, 'error': 'Session not found'}
        
        with self.lock:
            entry = {
                'result': result,
                'command': command,
                'timestamp': datetime.now().isoformat()
            }
            self.active_sessions[session_id]['shared_results'].append(entry)
            self._save_sessions()
        
        return {'success': True, 'result': entry}
    
    def get_session_updates(self, session_id: str, since: Optional[str] = None) -> Dict:
        """Get session updates since timestamp"""
        if session_id not in self.active_sessions:
            return {'success': False, 'error': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        updates = {
            'commands': [],
            'results': []
        }
        
        if since:
            since_dt = datetime.fromisoformat(since)
            for cmd in session['shared_commands']:
                if datetime.fromisoformat(cmd['timestamp']) > since_dt:
                    updates['commands'].append(cmd)
            for res in session['shared_results']:
                if datetime.fromisoformat(res['timestamp']) > since_dt:
                    updates['results'].append(res)
        else:
            updates['commands'] = session['shared_commands'][-10:]
            updates['results'] = session['shared_results'][-10:]
        
        return {
            'success': True,
            'updates': updates,
            'timestamp': datetime.now().isoformat()
        }
    
    def _save_sessions(self):
        """Save sessions to file"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.active_sessions, f, indent=2)
        except:
            pass
