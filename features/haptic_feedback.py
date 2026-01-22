"""
Haptic Feedback - Physical feedback for actions
"""
import os
import platform
from typing import Dict, Optional


class HapticFeedback:
    """Haptic feedback system"""
    
    def __init__(self):
        self.enabled = True
        self.system = platform.system()
    
    def trigger_haptic(self, intensity: str = "medium", pattern: str = "single") -> Dict:
        """Trigger haptic feedback"""
        if not self.enabled:
            return {"message": "Haptic feedback disabled"}
        
        try:
            if self.system == "Windows":
                # Windows haptic feedback (if supported)
                # Would use Windows API for haptic devices
                return {"success": True, "system": "windows", "intensity": intensity}
            elif self.system == "Darwin":  # macOS
                # macOS haptic feedback
                os.system("osascript -e 'tell application \"System Events\" to key code 63'")
                return {"success": True, "system": "macos", "intensity": intensity}
            else:  # Linux
                # Linux haptic feedback (if supported)
                return {"success": True, "system": "linux", "intensity": intensity}
        except Exception as e:
            return {"error": str(e)}
    
    def enable(self):
        """Enable haptic feedback"""
        self.enabled = True
    
    def disable(self):
        """Disable haptic feedback"""
        self.enabled = False
    
    def set_pattern(self, pattern: str):
        """Set haptic pattern"""
        patterns = {
            "single": 1,
            "double": 2,
            "triple": 3,
            "long": 1
        }
        return patterns.get(pattern, 1)
