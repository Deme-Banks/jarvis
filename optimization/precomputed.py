"""
Pre-computed Responses for Common Queries
"""
from typing import Dict, Optional


class PrecomputedResponses:
    """Pre-computed responses for instant answers"""
    
    def __init__(self):
        self.responses = self._load_responses()
    
    def _load_responses(self) -> Dict[str, str]:
        """Load pre-computed responses"""
        return {
            "greeting": "Hello. I'm JARVIS. I can talk, write code, and edit files in this project when you ask.",
            "goodbye": "Goodbye. Call if you need me.",
            "thanks": "You're welcome.",
            "what can you do": "I run locally on Ollama. I can answer questions, explain and write code, and update files in this repo when you tell me to.",
            "help": "Ask a question, say write a Python function, or tell me to edit a file in this project. Voice needs a mic; text mode does not.",
            "status": "All systems operational. Ready for commands.",
            "time": self._get_time_response(),
            "who are you": "I'm JARVIS, your personal local assistant. I use Ollama on this machine and I can help with code.",
            "capabilities": "Chat, coding help, scoped edits to this repo, and optional voice if PyAudio is installed.",
            "learning": "I keep recent conversation context in this session. For code, name the file you want explained.",
            "error": "I encountered an error. Let me try a different approach.",
            "unknown": "I'm not sure how to help with that. Could you rephrase or ask for help?",
        }
    
    def _get_time_response(self) -> str:
        """Get current time response"""
        from datetime import datetime
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%B %d, %Y')}."
    
    def get(self, query: str) -> Optional[str]:
        """Get pre-computed response"""
        query_lower = query.lower().strip()
        
        # Direct matches
        if query_lower in self.responses:
            return self.responses[query_lower]
        
        # Pattern matches
        patterns = {
            "hello": "greeting",
            "hi": "greeting",
            "hey": "greeting",
            "bye": "goodbye",
            "exit": "goodbye",
            "quit": "goodbye",
            "thank": "thanks",
            "what can": "what can you do",
            "help me": "help",
            "how can": "help",
            "what time": "time",
            "current time": "time",
            "who are": "who are you",
            "what are": "capabilities",
            "what do": "capabilities",
            "learn": "learning",
        }
        
        for pattern, response_key in patterns.items():
            if pattern in query_lower:
                return self.responses.get(response_key)
        
        return None
    
    def add(self, key: str, response: str):
        """Add custom pre-computed response"""
        self.responses[key] = response
    
    def update_time(self):
        """Update time response"""
        self.responses["time"] = self._get_time_response()


# Global instance
_precomputed = PrecomputedResponses()


def get_precomputed(query: str) -> Optional[str]:
    """Get pre-computed response"""
    return _precomputed.get(query)
