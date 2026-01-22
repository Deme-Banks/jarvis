"""
Auto-completion System for Commands
"""
from typing import List, Optional
from features.command_history import CommandHistory
from intelligence.intent_classifier import IntentClassifier
from learning.memory import MemorySystem


class AutoComplete:
    """Auto-completion for commands"""
    
    def __init__(self, history: CommandHistory, memory: MemorySystem):
        self.history = history
        self.memory = memory
        self.intent_classifier = IntentClassifier()
    
    def complete(self, partial_command: str, limit: int = 5) -> List[str]:
        """Complete partial command"""
        partial_lower = partial_command.lower().strip()
        
        completions = []
        
        # 1. Check history
        history_matches = self.history.search(partial_command, limit=limit)
        for entry in history_matches:
            cmd = entry["command"]
            if cmd not in completions:
                completions.append(cmd)
        
        # 2. Check learned patterns
        intent_context = self.intent_classifier.get_intent_context(partial_command)
        intent = intent_context["intent"]
        
        # Common completions based on intent
        intent_completions = {
            "create": [
                "create a keylogger",
                "create a reverse shell",
                "create a RAT",
                "create a credential harvester"
            ],
            "deploy": [
                "deploy to USB",
                "deploy keylogger to USB",
                "deploy with autorun"
            ],
            "test": [
                "test TCP flood",
                "test on localhost",
                "test for 30 seconds"
            ],
            "query": [
                "what is",
                "how does",
                "explain",
                "tell me about"
            ]
        }
        
        if intent in intent_completions:
            for completion in intent_completions[intent]:
                if partial_lower in completion.lower() and completion not in completions:
                    completions.append(completion)
        
        # 3. Check favorites
        favorites = self.history.get_favorites()
        for fav in favorites:
            cmd = fav["command"]
            if partial_lower in cmd.lower() and cmd not in completions:
                completions.append(cmd)
        
        return completions[:limit]
    
    def suggest_next_word(self, current_words: List[str]) -> List[str]:
        """Suggest next word based on current words"""
        if not current_words:
            return ["create", "run", "test", "deploy", "what", "how"]
        
        last_word = current_words[-1].lower()
        
        # Common next words
        next_words = {
            "create": ["a", "an", "keylogger", "reverse", "shell", "RAT"],
            "deploy": ["to", "on", "keylogger", "payload"],
            "test": ["TCP", "UDP", "HTTP", "on", "localhost"],
            "run": ["a", "TCP", "flood", "test"],
            "what": ["is", "are", "can", "does"],
            "how": ["does", "to", "can", "do"]
        }
        
        return next_words.get(last_word, [])
