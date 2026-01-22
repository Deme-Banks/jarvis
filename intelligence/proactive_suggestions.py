"""
Proactive Suggestion System
"""
from typing import List, Dict, Optional
from learning.memory import MemorySystem
from intelligence.intent_classifier import IntentClassifier
from datetime import datetime


class ProactiveSuggestions:
    """Generate proactive suggestions based on context"""
    
    def __init__(self, memory: MemorySystem):
        self.memory = memory
        self.intent_classifier = IntentClassifier()
        self.suggestion_history = []
    
    def generate_suggestions(self, current_context: Optional[Dict] = None) -> List[str]:
        """Generate proactive suggestions"""
        suggestions = []
        
        # Time-based suggestions
        suggestions.extend(self._time_based_suggestions())
        
        # Pattern-based suggestions
        suggestions.extend(self._pattern_based_suggestions())
        
        # Context-based suggestions
        if current_context:
            suggestions.extend(self._context_based_suggestions(current_context))
        
        # Learning-based suggestions
        suggestions.extend(self._learning_based_suggestions())
        
        # Remove duplicates and limit
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:5]  # Top 5
    
    def _time_based_suggestions(self) -> List[str]:
        """Time-based suggestions"""
        hour = datetime.now().hour
        suggestions = []
        
        if 9 <= hour <= 12:
            suggestions.append("Good morning! Ready to start security testing?")
        elif 13 <= hour <= 17:
            suggestions.append("Afternoon session - time for penetration testing")
        elif 18 <= hour <= 22:
            suggestions.append("Evening - perfect for learning new security concepts")
        elif hour >= 23 or hour <= 6:
            suggestions.append("Late night - consider taking a break")
        
        return suggestions
    
    def _pattern_based_suggestions(self) -> List[str]:
        """Suggestions based on usage patterns"""
        suggestions = []
        user_style = self.memory.analyze_user_style()
        
        if user_style.get("command_ratio", 0) > 0.5:
            suggestions.append("You prefer commands - try: 'Create a new payload'")
        
        if user_style.get("question_ratio", 0) > 0.5:
            suggestions.append("Ask me anything about cybersecurity!")
        
        return suggestions
    
    def _context_based_suggestions(self, context: Dict) -> List[str]:
        """Context-based suggestions"""
        suggestions = []
        
        # Check recent actions
        recent = self.memory.get_recent_context(3)
        if recent:
            last_intent = None
            if recent:
                last_conv = recent[-1]
                intent_context = self.intent_classifier.get_intent_context(
                    last_conv["user"]
                )
                last_intent = intent_context["intent"]
            
            # Suggest follow-ups
            if last_intent == "create":
                suggestions.append("Test what you created?")
                suggestions.append("Deploy it to USB?")
            elif last_intent == "test":
                suggestions.append("Review test results?")
                suggestions.append("Create a follow-up test?")
            elif last_intent == "query":
                suggestions.append("Want more details?")
                suggestions.append("See an example?")
        
        return suggestions
    
    def _learning_based_suggestions(self) -> List[str]:
        """Suggestions based on learning"""
        suggestions = []
        
        # Knowledge-based
        if len(self.memory.knowledge) > 0:
            topics = list(self.memory.knowledge.keys())[:3]
            if topics:
                suggestions.append(f"Explore: {', '.join(topics)}?")
        
        # Preference-based
        favorite_topic = self.memory.get_preference("favorite_topic")
        if favorite_topic:
            suggestions.append(f"Want to work on {favorite_topic}?")
        
        return suggestions
    
    def suggest_next_action(self, current_input: str) -> List[str]:
        """Suggest next actions based on current input"""
        intent_context = self.intent_classifier.get_intent_context(current_input)
        intent = intent_context["intent"]
        
        action_map = {
            "create": [
                "Test the created payload",
                "Deploy to USB",
                "Obfuscate the payload"
            ],
            "execute": [
                "Check the results",
                "Monitor the execution",
                "Stop the process"
            ],
            "test": [
                "Review test results",
                "Generate a report",
                "Run another test"
            ],
            "query": [
                "Get more details",
                "See an example",
                "Learn more about this"
            ]
        }
        
        return action_map.get(intent, [])
