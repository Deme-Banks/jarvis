"""
Voice Emotion Detection
"""
import os
import numpy as np
from typing import Dict, Optional
import requests


class EmotionDetector:
    """Voice emotion detection"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    def detect_emotion_from_audio(self, audio_path: str) -> Dict:
        """Detect emotion from audio file"""
        if not self.openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            # Transcribe audio first
            transcription = self._transcribe_audio(audio_path)
            if not transcription:
                return {"error": "Could not transcribe audio"}
            
            # Analyze emotion from transcription and audio features
            emotion = self._analyze_emotion(transcription, audio_path)
            
            return {
                "success": True,
                "emotion": emotion.get("primary"),
                "confidence": emotion.get("confidence"),
                "emotions": emotion.get("all"),
                "transcription": transcription
            }
        except Exception as e:
            return {"error": str(e)}
    
    def detect_emotion_from_text(self, text: str) -> Dict:
        """Detect emotion from text"""
        try:
            # Simple emotion detection based on keywords
            emotions = {
                "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing"],
                "sad": ["sad", "depressed", "unhappy", "disappointed", "terrible"],
                "angry": ["angry", "mad", "furious", "annoyed", "frustrated"],
                "neutral": ["okay", "fine", "alright", "sure"],
                "surprised": ["wow", "surprised", "shocked", "unexpected"]
            }
            
            text_lower = text.lower()
            emotion_scores = {}
            
            for emotion, keywords in emotions.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                emotion_scores[emotion] = score
            
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            total_score = sum(emotion_scores.values())
            confidence = emotion_scores[primary_emotion] / total_score if total_score > 0 else 0.5
            
            return {
                "success": True,
                "emotion": primary_emotion,
                "confidence": confidence,
                "emotions": emotion_scores
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Transcribe audio using Whisper"""
        try:
            url = "https://api.openai.com/v1/audio/transcriptions"
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            with open(audio_path, "rb") as f:
                files = {"file": f}
                data = {"model": "whisper-1"}
                
                response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                return result.get("text")
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def _analyze_emotion(self, text: str, audio_path: str) -> Dict:
        """Analyze emotion from text and audio"""
        # Text-based emotion
        text_emotion = self.detect_emotion_from_text(text)
        
        # Audio-based features (simplified)
        # In production, would analyze pitch, tone, speed, etc.
        audio_features = {
            "pitch": "medium",  # Would analyze from audio
            "speed": "normal",   # Would analyze from audio
            "volume": "medium"   # Would analyze from audio
        }
        
        return {
            "primary": text_emotion.get("emotion", "neutral"),
            "confidence": text_emotion.get("confidence", 0.5),
            "all": text_emotion.get("emotions", {}),
            "audio_features": audio_features
        }
