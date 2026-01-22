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
            "greeting": "Hello! I'm JARVIS, ready to assist.",
            "goodbye": "Goodbye! Have a great day.",
            "thanks": "You're welcome! Happy to help.",
            "what can you do": "I can help with cybersecurity testing, malware analysis, DDoS testing, USB deployment, and much more. What would you like to do?",
            "help": "I can help with: creating payloads, running security tests, deploying to USB, learning from interactions, and more. Just ask!",
            "status": "All systems operational. Ready for commands.",
            "time": self._get_time_response(),
            "who are you": "I'm JARVIS, an AI assistant for cybersecurity testing and automation. I help with authorized security testing and learning.",
            "capabilities": "I can create malware payloads, run DDoS tests, deploy to USB, learn from interactions, recognize emotions, and much more.",
            "learning": "I learn from every interaction, remember your preferences, and improve over time. Ask 'what have you learned' to see my progress.",
            "usb": "I can detect USB drives, deploy payloads, create packages, and clean USB drives. Say 'detect USB' to start.",
            "malware": "I can create various payloads: keyloggers, reverse shells, RATs, credential harvesters, and more. What would you like to create?",
            "security": "I provide cybersecurity testing tools for authorized use. All tools include safety warnings and are for educational purposes.",
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
            "usb": "usb",
            "malware": "malware",
            "payload": "malware",
            "security": "security",
            "cyber": "security",
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
