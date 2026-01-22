"""
Feedback Loop System - Continuous improvement
"""
from typing import Dict, Optional
from learning.memory import MemorySystem
from learning.adaptive_learning import AdaptiveLearner
from learning.llm_learning import LLMLearner
from learning.emotion_recognition import EmotionRecognizer
from learning.predictive import PredictiveSystem
from learning.advanced_patterns import AdvancedPatternRecognizer
from llm.local_llm import LocalLLM


class FeedbackLoop:
    """Continuous learning and improvement system"""
    
    def __init__(self, memory: MemorySystem, llm: LocalLLM):
        self.memory = memory
        self.adaptive_learner = AdaptiveLearner(memory, llm)
        self.llm_learner = LLMLearner(memory, llm)
        self.emotion_recognizer = EmotionRecognizer(memory)
        self.predictive_system = PredictiveSystem(memory)
        self.pattern_recognizer = AdvancedPatternRecognizer(memory)
        self.improvement_count = 0
    
    def process_interaction(self, user_input: str, assistant_response: str,
                           user_feedback: Optional[str] = None) -> Dict:
        """Process interaction and learn from it"""
        # Determine success from feedback or implicit signals
        success = self._determine_success(user_input, assistant_response, user_feedback)
        
        # Learn from interaction
        self.adaptive_learner.learn_from_interaction(
            user_input, 
            assistant_response, 
            success
        )
        
        # Process explicit feedback
        if user_feedback:
            self.adaptive_learner.improve_from_feedback(user_input, user_feedback)
        
        # Periodic deep learning (every 10 interactions)
        if len(self.memory.conversations) % 10 == 0:
            self.llm_learner.learn_from_conversations()
        
        return {
            "learned": True,
            "success": success,
            "total_interactions": len(self.memory.conversations)
        }
    
    def _determine_success(self, user_input: str, response: str, 
                          feedback: Optional[str]) -> bool:
        """Determine if interaction was successful"""
        if feedback:
            return "good" in feedback.lower() or "correct" in feedback.lower() or \
                   "thanks" in feedback.lower()
        
        # Implicit success signals
        success_signals = [
            "thanks", "thank you", "good", "perfect", "yes", "correct"
        ]
        
        # Check if user continues conversation (implicit success)
        # This is a simplified check
        return len(response) > 20  # Longer responses often mean more helpful
    
    def improve_next_response(self, user_input: str, base_response: str) -> str:
        """Improve response using learned patterns"""
        # Detect emotion
        emotion, confidence = self.emotion_recognizer.get_primary_emotion(user_input)
        self.emotion_recognizer.track_emotion_history(user_input)
        
        # Adaptive improvement
        improved = self.adaptive_learner.adapt_response(user_input, base_response)
        
        # Adapt to emotion
        improved = self.emotion_recognizer.adapt_response_to_emotion(emotion, improved)
        
        # Predictive improvements
        predicted_style = self.predictive_system.predict_response_style(user_input)
        if predicted_style["length"] == "short" and len(improved) > 100:
            improved = improved.split(". ")[0] + "."
        elif predicted_style["length"] == "long":
            suggestions = self.predictive_system.suggest_actions()
            if suggestions:
                improved += f" [Suggestions: {', '.join(suggestions[:2])}]"
        
        # LLM-based improvement (if enabled)
        if self.improvement_count % 5 == 0:  # Every 5th response
            try:
                improved = self.llm_learner.improve_response(user_input, improved)
            except:
                pass
        
        self.improvement_count += 1
        return improved
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learning progress"""
        insights = self.adaptive_learner.generate_learning_insights()
        
        return {
            "total_interactions": len(self.memory.conversations),
            "learned_preferences": len(self.memory.preferences),
            "knowledge_topics": len(self.memory.knowledge),
            "learned_patterns": len(self.memory.patterns),
            "user_style": self.memory.analyze_user_style(),
            "improvement_count": self.improvement_count
        }
    
    def reset_learning(self):
        """Reset all learned data (use with caution)"""
        self.memory.conversations = []
        self.memory.preferences = {}
        self.memory.knowledge = {}
        self.memory.patterns = {}
        self.improvement_count = 0
