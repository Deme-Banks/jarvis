"""
Sound Effects Library - Audio feedback for actions
"""
import os
import platform
from typing import Dict, Optional
from pathlib import Path


class SoundEffectsLibrary:
    """Sound effects library for JARVIS"""
    
    def __init__(self, sounds_dir: str = "sounds"):
        self.sounds_dir = sounds_dir
        self.sounds: Dict[str, str] = {}
        os.makedirs(sounds_dir, exist_ok=True)
        self._initialize_sounds()
    
    def _initialize_sounds(self):
        """Initialize sound effects"""
        self.sounds = {
            "success": "success.wav",
            "error": "error.wav",
            "notification": "notification.wav",
            "command": "command.wav",
            "startup": "startup.wav",
            "shutdown": "shutdown.wav",
            "alert": "alert.wav",
            "confirm": "confirm.wav",
            "cancel": "cancel.wav",
            "processing": "processing.wav"
        }
    
    def play_sound(self, sound_name: str) -> bool:
        """Play a sound effect"""
        if sound_name not in self.sounds:
            return False
        
        sound_file = os.path.join(self.sounds_dir, self.sounds[sound_name])
        
        if not os.path.exists(sound_file):
            # Use system beep as fallback
            self._system_beep()
            return False
        
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif platform.system() == "Darwin":  # macOS
                os.system(f"afplay {sound_file}")
            else:  # Linux
                os.system(f"aplay {sound_file}")
            return True
        except Exception as e:
            print(f"Error playing sound: {e}")
            self._system_beep()
            return False
    
    def _system_beep(self):
        """Fallback system beep"""
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(1000, 100)
            else:
                print("\a")  # ASCII bell
        except:
            pass
    
    def play_success(self):
        """Play success sound"""
        return self.play_sound("success")
    
    def play_error(self):
        """Play error sound"""
        return self.play_sound("error")
    
    def play_notification(self):
        """Play notification sound"""
        return self.play_sound("notification")
    
    def play_command(self):
        """Play command sound"""
        return self.play_sound("command")
