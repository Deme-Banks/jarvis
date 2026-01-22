"""
Emotion Recognition System
"""
import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
from learning.memory import MemorySystem


class EmotionRecognizer:
    """Recognize emotions from text and voice patterns"""
    
    def __init__(self, memory: MemorySystem):
        self.memory = memory
        
        # Emotion keywords
        self.emotion_keywords = {
            "happy": ["happy", "great", "excellent", "awesome", "thanks", "perfect", "good"],
            "frustrated": ["frustrated", "annoying", "wrong", "error", "failed", "broken"],
            "curious": ["what", "how", "why", "explain", "tell me", "show me"],
            "excited": ["wow", "amazing", "incredible", "fantastic", "love"],
            "neutral": [],
            "stressed": ["urgent", "quick", "hurry", "asap", "important"],
            "satisfied": ["good", "nice", "works", "correct", "right"]
        }
        
        # Emotion intensity modifiers
        self.intensity_modifiers = {
            "very": 1.5,
            "really": 1.3,
            "extremely": 2.0,
            "slightly": 0.5,
            "a bit": 0.7
        }
    
    def detect_emotion(self, text: str) -> Dict[str, float]:
        """Detect emotions from text"""
        text_lower = text.lower()
        emotions = {}
        
        # Check for emotion keywords
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                    # Check for intensity modifiers
                    for modifier, multiplier in self.intensity_modifiers.items():
                        if modifier in text_lower:
                            score *= multiplier
            
            if score > 0:
                emotions[emotion] = min(score / len(keywords), 1.0)  # Normalize
        
        # Check punctuation for intensity
        exclamation_count = text.count("!")
        question_count = text.count("?")
        
        if exclamation_count > 0:
            if "happy" in emotions or "excited" in emotions:
                emotions["excited"] = emotions.get("excited", 0) + (exclamation_count * 0.2)
            elif "frustrated" in emotions:
                emotions["frustrated"] += (exclamation_count * 0.2)
        
        if question_count > 2:
            emotions["curious"] = emotions.get("curious", 0) + 0.3
        
        # If no emotions detected, default to neutral
        if not emotions:
            emotions["neutral"] = 1.0
        
        return emotions
    
    def get_primary_emotion(self, text: str) -> Tuple[str, float]:
        """Get primary emotion and confidence"""
        emotions = self.detect_emotion(text)
        
        if not emotions:
            return ("neutral", 1.0)
        
        primary = max(emotions.items(), key=lambda x: x[1])
        return primary
    
    def adapt_response_to_emotion(self, emotion: str, base_response: str) -> str:
        """Adapt response based on detected emotion"""
        if emotion == "frustrated":
            # Be more helpful and clear
            return f"I understand the frustration. {base_response} Let me know if you need clarification."
        elif emotion == "excited":
            # Match the enthusiasm
            return f"Great! {base_response} This is exciting!"
        elif emotion == "curious":
            # Provide more detail
            return f"{base_response} Would you like me to explain further?"
        elif emotion == "stressed":
            # Be concise and direct
            return base_response.split(". ")[0] + "."  # First sentence only
        elif emotion == "happy" or emotion == "satisfied":
            # Positive reinforcement
            return f"{base_response} Glad I could help!"
        
        return base_response
    
    def track_emotion_history(self, text: str):
        """Track emotion over time"""
        emotion, confidence = self.get_primary_emotion(text)
        
        # Save to memory
        if "emotion_history" not in self.memory.preferences:
            self.memory.preferences["emotion_history"] = {"value": [], "confidence": 0}
        
        self.memory.preferences["emotion_history"]["value"].append({
            "emotion": emotion,
            "confidence": confidence,
            "timestamp": self._get_timestamp()
        })
        
        # Keep last 100 emotions
        if len(self.memory.preferences["emotion_history"]["value"]) > 100:
            self.memory.preferences["emotion_history"]["value"] = \
                self.memory.preferences["emotion_history"]["value"][-100:]
    
    def get_emotion_trends(self) -> Dict:
        """Analyze emotion trends over time"""
        if "emotion_history" not in self.memory.preferences:
            return {}
        
        history = self.memory.preferences["emotion_history"]["value"]
        if not history:
            return {}
        
        emotion_counts = Counter([e["emotion"] for e in history])
        total = len(history)
        
        trends = {
            "most_common": emotion_counts.most_common(1)[0] if emotion_counts else None,
            "distribution": {emotion: count/total for emotion, count in emotion_counts.items()},
            "recent_emotions": [e["emotion"] for e in history[-10:]],
            "average_confidence": sum(e["confidence"] for e in history) / total
        }
        
        return trends
    
    def detect_emotion_change(self) -> Optional[str]:
        """Detect significant emotion changes"""
        if "emotion_history" not in self.memory.preferences:
            return None
        
        history = self.memory.preferences["emotion_history"]["value"]
        if len(history) < 5:
            return None
        
        # Compare recent vs older emotions
        recent = [e["emotion"] for e in history[-5:]]
        older = [e["emotion"] for e in history[-10:-5]]
        
        recent_common = Counter(recent).most_common(1)[0][0]
        older_common = Counter(older).most_common(1)[0][0]
        
        if recent_common != older_common:
            return f"Emotion shifted from {older_common} to {recent_common}"
        
        return None
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def suggest_emotion_appropriate_action(self, emotion: str) -> List[str]:
        """Suggest actions appropriate for detected emotion"""
        suggestions = {
            "frustrated": [
                "Let me help troubleshoot",
                "Would you like a simpler explanation?",
                "I can break this down step by step"
            ],
            "curious": [
                "I can explain in more detail",
                "Want to explore this further?",
                "Let me show you examples"
            ],
            "excited": [
                "Great! Let's build on this",
                "Want to try something advanced?",
                "This is a perfect learning opportunity"
            ],
            "stressed": [
                "I'll keep this quick",
                "Here's the essential info",
                "Let me give you the key points"
            ]
        }
        
        return suggestions.get(emotion, [])
