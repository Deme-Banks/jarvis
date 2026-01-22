"""
Adaptive Learning System - Learns from interactions and improves
"""
from typing import Dict, List, Optional, Tuple
from learning.memory import MemorySystem
from llm.local_llm import LocalLLM
import re


class AdaptiveLearner:
    """Adaptive learning system that improves over time"""
    
    def __init__(self, memory: MemorySystem, llm: Optional[LocalLLM] = None):
        self.memory = memory
        self.llm = llm
    
    def learn_from_interaction(self, user_input: str, assistant_response: str, 
                              success: bool = True):
        """Learn from a single interaction"""
        # Save conversation
        self.memory.save_conversation(user_input, assistant_response)
        
        # Extract preferences
        self._extract_preferences(user_input, assistant_response)
        
        # Learn patterns
        self._learn_patterns(user_input, assistant_response, success)
        
        # Extract knowledge
        self._extract_knowledge(user_input, assistant_response)
    
    def _extract_preferences(self, user_input: str, response: str):
        """Extract and learn user preferences"""
        user_lower = user_input.lower()
        
        # Learn response style preference
        if "shorter" in user_lower or "brief" in user_lower:
            self.memory.learn_preference("response_style", "brief")
        elif "detailed" in user_lower or "explain" in user_lower:
            self.memory.learn_preference("response_style", "detailed")
        
        # Learn voice preference
        if "slower" in user_lower:
            self.memory.learn_preference("speech_rate", "slow")
        elif "faster" in user_lower:
            self.memory.learn_preference("speech_rate", "fast")
        
        # Learn topic preferences
        if any(word in user_lower for word in ["security", "cyber", "hack"]):
            self.memory.learn_preference("favorite_topic", "cybersecurity")
        elif any(word in user_lower for word in ["automate", "script", "code"]):
            self.memory.learn_preference("favorite_topic", "automation")
    
    def _learn_patterns(self, user_input: str, response: str, success: bool):
        """Learn patterns from interactions"""
        if not success:
            return
        
        # Extract intent
        intent = self._extract_intent(user_input)
        
        # Learn successful patterns
        self.memory.learn_pattern(intent, response[:100])  # First 100 chars as pattern
    
    def _extract_intent(self, text: str) -> str:
        """Extract intent from user input"""
        text_lower = text.lower()
        
        # Intent patterns
        intents = {
            "create": ["create", "make", "generate", "build"],
            "run": ["run", "execute", "start", "launch"],
            "test": ["test", "check", "verify"],
            "explain": ["explain", "what is", "how does", "tell me"],
            "search": ["find", "search", "look for"],
            "attack": ["attack", "ddos", "flood", "test security"]
        }
        
        for intent, keywords in intents.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
        return "general"
    
    def _extract_knowledge(self, user_input: str, response: str):
        """Extract knowledge from interactions"""
        # Look for factual statements
        if "is" in user_input.lower() or "are" in user_input.lower():
            # Extract facts
            facts = self._extract_facts(user_input, response)
            for topic, fact in facts:
                self.memory.add_knowledge(topic, fact, "conversation")
    
    def _extract_facts(self, user_input: str, response: str) -> List[Tuple[str, str]]:
        """Extract facts from conversation"""
        facts = []
        
        # Simple fact extraction patterns
        # "X is Y" pattern
        is_pattern = r"(\w+)\s+is\s+([^\.]+)"
        matches = re.findall(is_pattern, user_input + " " + response)
        for match in matches:
            facts.append((match[0], f"{match[0]} is {match[1]}"))
        
        return facts
    
    def adapt_response(self, user_input: str, base_response: str) -> str:
        """Adapt response based on learned preferences"""
        # Get user preferences
        response_style = self.memory.get_preference("response_style", "normal")
        
        # Adapt based on style
        if response_style == "brief":
            # Make response shorter
            sentences = base_response.split(". ")
            if len(sentences) > 2:
                base_response = ". ".join(sentences[:2]) + "."
        elif response_style == "detailed":
            # Add more context if available
            context = self.memory.get_recent_context(3)
            if context:
                base_response += " [Based on previous interactions]"
        
        # Check for learned patterns
        intent = self._extract_intent(user_input)
        best_pattern = self.memory.get_best_pattern(intent)
        if best_pattern and len(base_response) < 50:
            # Use learned pattern if response is too short
            base_response = best_pattern
        
        # Add relevant knowledge
        knowledge = self._get_relevant_knowledge(user_input)
        if knowledge:
            base_response += f" [Note: {knowledge}]"
        
        return base_response
    
    def _get_relevant_knowledge(self, user_input: str) -> Optional[str]:
        """Get relevant knowledge from knowledge base"""
        # Extract keywords
        keywords = [word for word in user_input.lower().split() if len(word) > 4]
        
        for keyword in keywords:
            knowledge = self.memory.get_knowledge(keyword)
            if knowledge:
                return knowledge[0]["information"]
        
        return None
    
    def generate_learning_insights(self) -> Dict:
        """Generate insights about what has been learned"""
        user_style = self.memory.analyze_user_style()
        preferences = self.memory.preferences
        
        insights = {
            "total_interactions": len(self.memory.conversations),
            "user_style": user_style,
            "learned_preferences": {
                k: v["value"] for k, v in preferences.items()
            },
            "knowledge_topics": list(self.memory.knowledge.keys()),
            "top_patterns": dict(sorted(
                self.memory.patterns.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10])
        }
        
        return insights
    
    def improve_from_feedback(self, user_input: str, feedback: str):
        """Learn from explicit feedback"""
        if "wrong" in feedback.lower() or "incorrect" in feedback.lower():
            # Learn what not to do
            intent = self._extract_intent(user_input)
            self.memory.learn_pattern(f"{intent}_wrong", feedback)
        elif "good" in feedback.lower() or "correct" in feedback.lower():
            # Reinforce correct behavior
            intent = self._extract_intent(user_input)
            recent = self.memory.get_recent_context(1)
            if recent:
                self.memory.learn_pattern(intent, recent[0]["assistant"])
