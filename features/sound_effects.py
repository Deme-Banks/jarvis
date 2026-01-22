"""
Sound Effects - Audio feedback for actions
"""
import os
import platform
from typing import Dict, Optional


class SoundEffects:
    """Sound effects system"""
    
    def __init__(self):
        self.sounds_enabled = True
        self.sound_library = {
            "success": "sounds/success.wav",
            "error": "sounds/error.wav",
            "notification": "sounds/notification.wav",
            "command": "sounds/command.wav",
            "startup": "sounds/startup.wav",
            "shutdown": "sounds/shutdown.wav"
        }
    
    def play_sound(self, sound_name: str) -> Dict:
        """Play a sound effect"""
        if not self.sounds_enabled:
            return {"message": "Sounds disabled"}
        
        sound_path = self.sound_library.get(sound_name)
        if not sound_path or not os.path.exists(sound_path):
            # Use system beep as fallback
            return self._play_system_beep()
        
        try:
            system = platform.system()
            if system == "Windows":
                import winsound
                winsound.PlaySound(sound_path, winsound.SND_FILENAME)
            elif system == "Darwin":  # macOS
                os.system(f"afplay {sound_path}")
            else:  # Linux
                os.system(f"aplay {sound_path}")
            
            return {"success": True, "sound": sound_name}
        except Exception as e:
            return {"error": str(e)}
    
    def _play_system_beep(self) -> Dict:
        """Play system beep"""
        try:
            system = platform.system()
            if system == "Windows":
                import winsound
                winsound.Beep(1000, 200)
            elif system == "Darwin":  # macOS
                os.system("say beep")
            else:  # Linux
                os.system("echo -e '\a'")
            
            return {"success": True, "sound": "system_beep"}
        except Exception as e:
            return {"error": str(e)}
    
    def enable_sounds(self):
        """Enable sound effects"""
        self.sounds_enabled = True
    
    def disable_sounds(self):
        """Disable sound effects"""
        self.sounds_enabled = False
    
    def add_sound(self, name: str, file_path: str):
        """Add custom sound"""
        self.sound_library[name] = file_path
