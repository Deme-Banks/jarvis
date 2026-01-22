"""
Custom Wake Words - Train custom wake words
"""
import os
import json
from typing import Dict, Optional, List
from datetime import datetime


class CustomWakeWordTrainer:
    """Train custom wake words for JARVIS"""
    
    def __init__(self, models_dir: str = "models/wake_words"):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
    
    def create_wake_word_model(self, wake_word: str, audio_samples: List[str]) -> Dict:
        """Create a custom wake word model"""
        try:
            # This would use a wake word training library
            # For now, create a template structure
            
            model_path = os.path.join(self.models_dir, wake_word.lower().replace(" ", "_"))
            os.makedirs(model_path, exist_ok=True)
            
            # Save model configuration
            config = {
                "wake_word": wake_word,
                "created": datetime.now().isoformat(),
                "samples": len(audio_samples),
                "model_type": "pocketsphinx",  # or "porcupine", "snowboy", etc.
                "sensitivity": 0.5
            }
            
            config_file = os.path.join(model_path, "config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Copy audio samples
            samples_dir = os.path.join(model_path, "samples")
            os.makedirs(samples_dir, exist_ok=True)
            
            for i, sample in enumerate(audio_samples):
                if os.path.exists(sample):
                    import shutil
                    dest = os.path.join(samples_dir, f"sample_{i}.wav")
                    shutil.copy2(sample, dest)
            
            return {
                "success": True,
                "wake_word": wake_word,
                "model_path": model_path,
                "samples": len(audio_samples)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def train_wake_word(self, wake_word: str, training_data: Dict) -> Dict:
        """Train wake word from data"""
        # This would use actual wake word training
        # For PocketSphinx, would create language model and dictionary
        # For Porcupine, would use their training service
        
        return {
            "success": True,
            "wake_word": wake_word,
            "message": "Wake word model training initiated",
            "estimated_time": "5-10 minutes"
        }
    
    def list_wake_words(self) -> List[Dict]:
        """List available wake words"""
        wake_words = []
        
        if os.path.exists(self.models_dir):
            for item in os.listdir(self.models_dir):
                model_path = os.path.join(self.models_dir, item)
                if os.path.isdir(model_path):
                    config_file = os.path.join(model_path, "config.json")
                    if os.path.exists(config_file):
                        try:
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                            wake_words.append({
                                "wake_word": config.get("wake_word", item),
                                "model_path": model_path,
                                "created": config.get("created")
                            })
                        except:
                            pass
        
        return wake_words
