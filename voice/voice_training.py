"""
Voice Training - Improve recognition accuracy
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class VoiceTrainer:
    """Voice recognition training system"""
    
    def __init__(self, training_data_file: str = "data/voice_training.json"):
        self.training_data_file = training_data_file
        self.training_data = self._load_training_data()
        self.corrections = defaultdict(list)
    
    def _load_training_data(self) -> Dict:
        """Load training data"""
        if os.path.exists(self.training_data_file):
            try:
                with open(self.training_data_file, 'r') as f:
                    return json.load(f)
            except:
                return {"corrections": {}, "patterns": {}}
        return {"corrections": {}, "patterns": {}}
    
    def _save_training_data(self):
        """Save training data"""
        os.makedirs(os.path.dirname(self.training_data_file), exist_ok=True)
        with open(self.training_data_file, 'w') as f:
            json.dump(self.training_data, f, indent=2)
    
    def add_correction(self, original: str, corrected: str, context: Optional[str] = None):
        """Add a correction to improve recognition"""
        if original not in self.training_data["corrections"]:
            self.training_data["corrections"][original] = []
        
        self.training_data["corrections"][original].append({
            "corrected": corrected,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_training_data()
    
    def get_correction(self, text: str) -> Optional[str]:
        """Get correction for text"""
        # Exact match
        if text in self.training_data["corrections"]:
            corrections = self.training_data["corrections"][text]
            if corrections:
                # Return most recent correction
                return corrections[-1]["corrected"]
        
        # Fuzzy match (simplified)
        text_lower = text.lower()
        for original, corrections in self.training_data["corrections"].items():
            if original.lower() in text_lower or text_lower in original.lower():
                if corrections:
                    return corrections[-1]["corrected"]
        
        return None
    
    def learn_pattern(self, pattern: str, replacement: str):
        """Learn a pattern for automatic correction"""
        if "patterns" not in self.training_data:
            self.training_data["patterns"] = {}
        
        self.training_data["patterns"][pattern] = replacement
        self._save_training_data()
    
    def apply_corrections(self, text: str) -> str:
        """Apply learned corrections to text"""
        # Check for exact corrections
        correction = self.get_correction(text)
        if correction:
            return correction
        
        # Apply patterns
        for pattern, replacement in self.training_data.get("patterns", {}).items():
            if pattern in text:
                text = text.replace(pattern, replacement)
        
        return text
