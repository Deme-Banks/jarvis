"""
Advanced Pattern Recognition System
"""
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
from learning.memory import MemorySystem
import json


class AdvancedPatternRecognizer:
    """Advanced pattern recognition using ML-like techniques"""
    
    def __init__(self, memory: MemorySystem):
        self.memory = memory
        self.pattern_cache = {}
    
    def extract_intent_patterns(self, limit: int = 100) -> Dict[str, List[str]]:
        """Extract intent patterns from conversations"""
        if not self.memory.conversations:
            return {}
        
        recent = self.memory.conversations[-limit:]
        intent_patterns = defaultdict(list)
        
        for conv in recent:
            user_input = conv["user"].lower()
            
            # Extract intent
            intent = self._classify_intent(user_input)
            
            # Extract key phrases
            phrases = self._extract_phrases(user_input)
            intent_patterns[intent].extend(phrases)
        
        # Get most common patterns per intent
        result = {}
        for intent, phrases in intent_patterns.items():
            counter = Counter(phrases)
            result[intent] = [phrase for phrase, count in counter.most_common(10)]
        
        return result
    
    def _classify_intent(self, text: str) -> str:
        """Classify intent from text"""
        text_lower = text.lower()
        
        intent_keywords = {
            "create": ["create", "make", "generate", "build", "new"],
            "execute": ["run", "execute", "start", "launch", "do"],
            "query": ["what", "how", "why", "when", "where", "tell me", "explain"],
            "modify": ["change", "modify", "update", "edit", "alter"],
            "delete": ["delete", "remove", "clear", "erase"],
            "test": ["test", "check", "verify", "validate"],
            "attack": ["attack", "ddos", "flood", "hack", "exploit"]
        }
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
        return "general"
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        # Simple phrase extraction (can be enhanced with NLP)
        words = text.split()
        phrases = []
        
        # Extract 2-3 word phrases
        for i in range(len(words) - 1):
            phrase = " ".join(words[i:i+2])
            if len(phrase) > 3:
                phrases.append(phrase)
        
        return phrases
    
    def predict_next_action(self, current_input: str) -> Optional[str]:
        """Predict next likely action based on patterns"""
        intent = self._classify_intent(current_input)
        patterns = self.extract_intent_patterns()
        
        if intent in patterns and patterns[intent]:
            # Return most common pattern for this intent
            return patterns[intent][0]
        
        return None
    
    def find_similar_conversations(self, query: str, limit: int = 5) -> List[Dict]:
        """Find similar past conversations"""
        if not self.memory.conversations:
            return []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        similarities = []
        
        for conv in self.memory.conversations:
            conv_text = conv["user"].lower()
            conv_words = set(conv_text.split())
            
            # Simple similarity (Jaccard)
            intersection = len(query_words & conv_words)
            union = len(query_words | conv_words)
            similarity = intersection / union if union > 0 else 0
            
            if similarity > 0.2:  # Threshold
                similarities.append((similarity, conv))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        return [conv for _, conv in similarities[:limit]]
    
    def detect_anomalies(self) -> List[Dict]:
        """Detect anomalous patterns in conversations"""
        if len(self.memory.conversations) < 10:
            return []
        
        anomalies = []
        
        # Analyze conversation lengths
        lengths = [len(c["user"]) for c in self.memory.conversations]
        avg_length = sum(lengths) / len(lengths)
        
        for i, conv in enumerate(self.memory.conversations):
            length = len(conv["user"])
            
            # Anomaly: unusually long or short
            if length > avg_length * 2 or length < avg_length * 0.3:
                anomalies.append({
                    "type": "length_anomaly",
                    "conversation": conv,
                    "index": i,
                    "reason": f"Length {length} vs average {avg_length:.1f}"
                })
        
        return anomalies
    
    def generate_response_template(self, intent: str) -> Optional[str]:
        """Generate response template based on learned patterns"""
        patterns = self.extract_intent_patterns()
        
        if intent in patterns:
            # Find successful responses for this intent
            successful_responses = []
            for conv in self.memory.conversations:
                if self._classify_intent(conv["user"].lower()) == intent:
                    successful_responses.append(conv["assistant"])
            
            if successful_responses:
                # Return most common response pattern
                return successful_responses[-1]  # Most recent successful
        
        return None
    
    def learn_sequence_patterns(self) -> Dict[str, List[str]]:
        """Learn sequential patterns (what comes after what)"""
        if len(self.memory.conversations) < 2:
            return {}
        
        sequences = defaultdict(list)
        
        for i in range(len(self.memory.conversations) - 1):
            current = self.memory.conversations[i]
            next_conv = self.memory.conversations[i + 1]
            
            current_intent = self._classify_intent(current["user"].lower())
            next_intent = self._classify_intent(next_conv["user"].lower())
            
            sequences[current_intent].append(next_intent)
        
        # Get most common sequences
        result = {}
        for intent, next_intents in sequences.items():
            counter = Counter(next_intents)
            result[intent] = [intent for intent, count in counter.most_common(3)]
        
        return result
