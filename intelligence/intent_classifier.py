"""
Advanced Intent Classification using ML-like Techniques
"""
from typing import Dict, List, Tuple
from collections import Counter
import re


class IntentClassifier:
    """Advanced intent classification"""
    
    def __init__(self):
        # Intent patterns with weights
        self.intent_patterns = {
            "create": {
                "keywords": ["create", "make", "generate", "build", "new"],
                "weight": 1.0
            },
            "execute": {
                "keywords": ["run", "execute", "start", "launch", "do"],
                "weight": 1.0
            },
            "query": {
                "keywords": ["what", "how", "why", "when", "where", "tell me", "explain"],
                "weight": 1.2
            },
            "modify": {
                "keywords": ["change", "modify", "update", "edit", "alter"],
                "weight": 1.0
            },
            "delete": {
                "keywords": ["delete", "remove", "clear", "erase"],
                "weight": 1.0
            },
            "test": {
                "keywords": ["test", "check", "verify", "validate"],
                "weight": 1.0
            },
            "attack": {
                "keywords": ["attack", "ddos", "flood", "hack", "exploit"],
                "weight": 1.5
            },
            "deploy": {
                "keywords": ["deploy", "install", "put", "copy to"],
                "weight": 1.0
            },
            "learn": {
                "keywords": ["learn", "remember", "save", "store"],
                "weight": 1.0
            },
            "help": {
                "keywords": ["help", "assist", "guide", "how to"],
                "weight": 1.2
            }
        }
    
    def classify(self, text: str) -> Tuple[str, float]:
        """Classify intent with confidence score"""
        text_lower = text.lower()
        scores = {}
        
        for intent, pattern in self.intent_patterns.items():
            score = 0
            keywords = pattern["keywords"]
            weight = pattern["weight"]
            
            for keyword in keywords:
                # Exact match
                if keyword == text_lower:
                    score += 10 * weight
                # Word match
                elif f" {keyword} " in f" {text_lower} ":
                    score += 5 * weight
                # Partial match
                elif keyword in text_lower:
                    score += 2 * weight
            
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return ("general", 0.0)
        
        # Get highest scoring intent
        best_intent = max(scores.items(), key=lambda x: x[1])
        confidence = min(best_intent[1] / 10.0, 1.0)  # Normalize to 0-1
        
        return (best_intent[0], confidence)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text"""
        entities = {
            "ip_addresses": [],
            "urls": [],
            "ports": [],
            "file_paths": [],
            "commands": []
        }
        
        # IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        entities["ip_addresses"] = re.findall(ip_pattern, text)
        
        # URLs
        url_pattern = r'https?://[^\s]+'
        entities["urls"] = re.findall(url_pattern, text)
        
        # Ports
        port_pattern = r':(\d{1,5})\b'
        entities["ports"] = re.findall(port_pattern, text)
        
        # File paths (simple)
        path_pattern = r'[A-Za-z]:\\[^\s]+|/[^\s]+'
        entities["file_paths"] = re.findall(path_pattern, text)
        
        # Commands (quoted strings)
        command_pattern = r'"([^"]+)"'
        entities["commands"] = re.findall(command_pattern, text)
        
        return entities
    
    def get_intent_context(self, text: str) -> Dict:
        """Get full intent context"""
        intent, confidence = self.classify(text)
        entities = self.extract_entities(text)
        
        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "original_text": text
        }
