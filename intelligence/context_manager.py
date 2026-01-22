"""
Advanced Context Management
"""
from typing import Dict, List, Optional, Any
from collections import deque
from datetime import datetime
import json


class ContextManager:
    """Manage conversation and system context"""
    
    def __init__(self, max_context_size: int = 50):
        self.max_context_size = max_context_size
        self.conversation_history = deque(maxlen=max_context_size)
        self.system_context = {}
        self.active_topics = []
        self.context_cache = {}
    
    def add_to_history(self, user_input: str, assistant_response: str, 
                     metadata: Optional[Dict] = None):
        """Add to conversation history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'assistant': assistant_response,
            'metadata': metadata or {}
        }
        self.conversation_history.append(entry)
    
    def get_recent_context(self, limit: int = 5) -> List[Dict]:
        """Get recent conversation context"""
        return list(self.conversation_history)[-limit:]
    
    def get_full_context(self) -> Dict:
        """Get full context"""
        return {
            'conversation_history': list(self.conversation_history),
            'system_context': self.system_context,
            'active_topics': self.active_topics
        }
    
    def update_system_context(self, key: str, value: Any):
        """Update system context"""
        self.system_context[key] = value
    
    def get_system_context(self, key: str, default: Any = None) -> Any:
        """Get system context value"""
        return self.system_context.get(key, default)
    
    def add_topic(self, topic: str):
        """Add active topic"""
        if topic not in self.active_topics:
            self.active_topics.append(topic)
            if len(self.active_topics) > 10:
                self.active_topics.pop(0)
    
    def get_relevant_context(self, query: str) -> Dict:
        """Get relevant context for query"""
        query_lower = query.lower()
        relevant = {
            'recent_conversation': [],
            'related_topics': [],
            'system_info': {}
        }
        
        # Find relevant conversation history
        for entry in self.conversation_history:
            if (query_lower in entry['user'].lower() or 
                query_lower in entry['assistant'].lower()):
                relevant['recent_conversation'].append(entry)
        
        # Find related topics
        for topic in self.active_topics:
            if query_lower in topic.lower() or topic.lower() in query_lower:
                relevant['related_topics'].append(topic)
        
        # Add system context
        relevant['system_info'] = self.system_context.copy()
        
        return relevant
    
    def clear_context(self):
        """Clear all context"""
        self.conversation_history.clear()
        self.system_context.clear()
        self.active_topics.clear()
        self.context_cache.clear()
    
    def export_context(self, filepath: str):
        """Export context"""
        data = {
            'conversation_history': list(self.conversation_history),
            'system_context': self.system_context,
            'active_topics': self.active_topics,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
