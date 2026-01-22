"""
Persistent Memory and Learning System
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict
import pickle


class MemorySystem:
    """Persistent memory system for learning"""
    
    def __init__(self, memory_dir: str = "./memory"):
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)
        
        self.conversations_file = os.path.join(memory_dir, "conversations.json")
        self.preferences_file = os.path.join(memory_dir, "preferences.json")
        self.knowledge_file = os.path.join(memory_dir, "knowledge.json")
        self.patterns_file = os.path.join(memory_dir, "patterns.pkl")
        
        self.conversations = self._load_conversations()
        self.preferences = self._load_preferences()
        self.knowledge = self._load_knowledge()
        self.patterns = self._load_patterns()
    
    def _load_conversations(self) -> List[Dict]:
        """Load conversation history"""
        if os.path.exists(self.conversations_file):
            try:
                with open(self.conversations_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _load_preferences(self) -> Dict:
        """Load user preferences"""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _load_knowledge(self) -> Dict:
        """Load knowledge base"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _load_patterns(self) -> Dict:
        """Load learned patterns"""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'rb') as f:
                    return pickle.load(f)
            except:
                return defaultdict(int)
        return defaultdict(int)
    
    def save_conversation(self, user_input: str, assistant_response: str, 
                         context: Optional[Dict] = None):
        """Save conversation to memory"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response,
            "context": context or {}
        }
        self.conversations.append(conversation)
        
        # Keep last 1000 conversations
        if len(self.conversations) > 1000:
            self.conversations = self.conversations[-1000:]
        
        self._save_conversations()
    
    def learn_preference(self, key: str, value: Any):
        """Learn user preference"""
        self.preferences[key] = {
            "value": value,
            "learned_at": datetime.now().isoformat(),
            "confidence": self.preferences.get(key, {}).get("confidence", 0) + 1
        }
        self._save_preferences()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get learned preference"""
        if key in self.preferences:
            return self.preferences[key]["value"]
        return default
    
    def add_knowledge(self, topic: str, information: str, source: str = "user"):
        """Add knowledge to knowledge base"""
        if topic not in self.knowledge:
            self.knowledge[topic] = []
        
        self.knowledge[topic].append({
            "information": information,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "confidence": 1.0
        })
        
        # Remove duplicates and keep most recent
        seen = set()
        unique_knowledge = []
        for item in reversed(self.knowledge[topic]):
            info_hash = hash(item["information"])
            if info_hash not in seen:
                seen.add(info_hash)
                unique_knowledge.insert(0, item)
        self.knowledge[topic] = unique_knowledge[:10]  # Keep top 10
        
        self._save_knowledge()
    
    def get_knowledge(self, topic: str) -> List[Dict]:
        """Get knowledge about a topic"""
        return self.knowledge.get(topic, [])
    
    def learn_pattern(self, pattern: str, outcome: str):
        """Learn pattern from interactions"""
        pattern_key = f"{pattern}->{outcome}"
        self.patterns[pattern_key] += 1
        self._save_patterns()
    
    def get_best_pattern(self, pattern: str) -> Optional[str]:
        """Get best outcome for a pattern"""
        best_outcome = None
        best_count = 0
        
        for key, count in self.patterns.items():
            if key.startswith(f"{pattern}->"):
                if count > best_count:
                    best_count = count
                    best_outcome = key.split("->")[1]
        
        return best_outcome if best_count > 2 else None  # Need at least 3 occurrences
    
    def get_recent_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context"""
        return self.conversations[-limit:]
    
    def analyze_user_style(self) -> Dict:
        """Analyze user's communication style"""
        if not self.conversations:
            return {}
        
        # Analyze patterns
        avg_length = sum(len(c["user"]) for c in self.conversations) / len(self.conversations)
        question_count = sum(1 for c in self.conversations if "?" in c["user"])
        command_count = sum(1 for c in self.conversations if any(word in c["user"].lower() 
                            for word in ["create", "run", "make", "do", "execute"]))
        
        return {
            "avg_message_length": avg_length,
            "question_ratio": question_count / len(self.conversations),
            "command_ratio": command_count / len(self.conversations),
            "total_interactions": len(self.conversations),
            "preferred_topics": self._get_top_topics()
        }
    
    def _get_top_topics(self, limit: int = 5) -> List[str]:
        """Get most discussed topics"""
        topic_counts = defaultdict(int)
        for conv in self.conversations:
            # Simple keyword extraction
            words = conv["user"].lower().split()
            for word in words:
                if len(word) > 4:  # Filter short words
                    topic_counts[word] += 1
        
        return sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _save_conversations(self):
        """Save conversations to disk"""
        with open(self.conversations_file, 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    def _save_preferences(self):
        """Save preferences to disk"""
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def _save_knowledge(self):
        """Save knowledge to disk"""
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def _save_patterns(self):
        """Save patterns to disk"""
        with open(self.patterns_file, 'wb') as f:
            pickle.dump(dict(self.patterns), f)
