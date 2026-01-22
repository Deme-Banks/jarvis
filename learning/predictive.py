"""
Predictive Response System
"""
from typing import Dict, List, Optional
from learning.memory import MemorySystem
from learning.advanced_patterns import AdvancedPatternRecognizer


class PredictiveSystem:
    """Predictive response and action system"""
    
    def __init__(self, memory: MemorySystem):
        self.memory = memory
        self.pattern_recognizer = AdvancedPatternRecognizer(memory)
    
    def predict_next_request(self, current_input: str) -> List[str]:
        """Predict likely next requests"""
        intent = self.pattern_recognizer._classify_intent(current_input)
        sequences = self.pattern_recognizer.learn_sequence_patterns()
        
        predictions = []
        
        if intent in sequences:
            next_intents = sequences[intent]
            for next_intent in next_intents:
                # Generate example requests for each intent
                examples = self._generate_examples(next_intent)
                predictions.extend(examples)
        
        return predictions[:3]  # Top 3 predictions
    
    def _generate_examples(self, intent: str) -> List[str]:
        """Generate example requests for an intent"""
        examples = {
            "create": [
                "Create a keylogger",
                "Make a reverse shell",
                "Generate a network scanner"
            ],
            "execute": [
                "Run TCP flood test",
                "Execute the script",
                "Start the attack"
            ],
            "query": [
                "What is a DDoS attack?",
                "How does encryption work?",
                "Explain network security"
            ],
            "test": [
                "Test the connection",
                "Check for vulnerabilities",
                "Verify the system"
            ]
        }
        
        return examples.get(intent, [])
    
    def suggest_actions(self, context: Optional[Dict] = None) -> List[str]:
        """Suggest actions based on context and history"""
        suggestions = []
        
        # Get recent context
        recent = self.memory.get_recent_context(5)
        
        if not recent:
            # Default suggestions
            return [
                "Create a security test",
                "Run a network scan",
                "Check system status"
            ]
        
        # Analyze recent patterns
        last_intent = None
        if recent:
            last_conv = recent[-1]
            last_intent = self.pattern_recognizer._classify_intent(
                last_conv["user"].lower()
            )
        
        # Suggest based on patterns
        if last_intent == "create":
            suggestions.append("Test what you created")
            suggestions.append("Run the created tool")
        elif last_intent == "test":
            suggestions.append("Review test results")
            suggestions.append("Create a follow-up test")
        elif last_intent == "query":
            suggestions.append("Ask for more details")
            suggestions.append("Request an example")
        
        # Add common suggestions
        user_style = self.memory.analyze_user_style()
        if user_style.get("favorite_topics"):
            topics = user_style["favorite_topics"]
            if topics:
                top_topic = topics[0][0]
                suggestions.append(f"Learn more about {top_topic}")
        
        return suggestions[:5]
    
    def predict_response_style(self, user_input: str) -> Dict:
        """Predict preferred response style for this input"""
        style = {
            "length": "normal",
            "detail": "medium",
            "tone": "professional"
        }
        
        # Check learned preferences
        preferred_style = self.memory.get_preference("response_style", "normal")
        if preferred_style == "brief":
            style["length"] = "short"
        elif preferred_style == "detailed":
            style["length"] = "long"
            style["detail"] = "high"
        
        # Analyze input for clues
        input_lower = user_input.lower()
        if "quick" in input_lower or "fast" in input_lower:
            style["length"] = "short"
        elif "detailed" in input_lower or "explain" in input_lower:
            style["length"] = "long"
            style["detail"] = "high"
        
        return style
    
    def proactive_suggestions(self) -> List[str]:
        """Generate proactive suggestions based on learning"""
        suggestions = []
        
        # Time-based suggestions
        from datetime import datetime
        hour = datetime.now().hour
        
        if 9 <= hour <= 12:
            suggestions.append("Good morning! Ready to start security testing?")
        elif 13 <= hour <= 17:
            suggestions.append("Afternoon session - time for some penetration testing")
        elif 18 <= hour <= 22:
            suggestions.append("Evening - perfect for learning new security concepts")
        
        # Pattern-based suggestions
        user_style = self.memory.analyze_user_style()
        if user_style.get("command_ratio", 0) > 0.5:
            suggestions.append("You prefer commands - try: 'Create a new payload'")
        
        # Knowledge-based suggestions
        if len(self.memory.knowledge) > 0:
            topics = list(self.memory.knowledge.keys())[:3]
            suggestions.append(f"Want to explore: {', '.join(topics)}?")
        
        return suggestions
