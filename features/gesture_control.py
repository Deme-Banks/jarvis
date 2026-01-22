"""
Gesture Control - Alternative input method
"""
import os
from typing import Dict, Optional
try:
    import cv2
    import mediapipe as mp
    CV_AVAILABLE = True
except ImportError:
    CV_AVAILABLE = False
    mp = None


class GestureController:
    """Gesture control for JARVIS"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands if CV_AVAILABLE else None
        self.hands = self.mp_hands.Hands() if self.mp_hands else None
        self.gesture_map = {
            "thumbs_up": "confirm",
            "thumbs_down": "cancel",
            "open_palm": "stop",
            "fist": "activate",
            "point": "select"
        }
    
    def detect_gesture(self, image_path: str) -> Dict:
        """Detect gesture from image"""
        if not CV_AVAILABLE:
            return {"error": "OpenCV and MediaPipe not available"}
        
        if not os.path.exists(image_path):
            return {"error": "Image file not found"}
        
        try:
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            results = self.hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                # Simplified gesture detection
                # In production, would use more sophisticated ML
                gesture = self._classify_gesture(results.multi_hand_landmarks[0])
                
                return {
                    "success": True,
                    "gesture": gesture,
                    "command": self.gesture_map.get(gesture, "unknown")
                }
            else:
                return {"success": False, "message": "No hand detected"}
        except Exception as e:
            return {"error": str(e)}
    
    def _classify_gesture(self, landmarks) -> str:
        """Classify gesture from landmarks"""
        # Simplified classification
        # In production, would use trained ML model
        return "thumbs_up"  # Placeholder
    
    def map_gesture_to_command(self, gesture: str) -> Optional[str]:
        """Map gesture to JARVIS command"""
        return self.gesture_map.get(gesture)
