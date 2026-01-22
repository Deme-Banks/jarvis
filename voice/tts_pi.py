"""
Raspberry Pi Text-to-Speech (Offline)
"""
import subprocess
import tempfile
import os
from typing import Optional, Callable
import config_pi as config


class PiTTS:
    """Offline Text-to-Speech for Raspberry Pi"""
    
    def __init__(self, engine: Optional[str] = None):
        self.engine = engine or config.PiConfig.TTS_ENGINE
        self.rate = config.PiConfig.TTS_RATE
    
    def speak(self, text: str, interrupt: bool = False) -> bytes:
        """Convert text to speech audio"""
        if interrupt:
            self.stop()
        
        if self.engine == "piper":
            return self._piper_tts(text)
        elif self.engine == "pyttsx3":
            return self._pyttsx3_tts(text)
        elif self.engine == "espeak":
            return self._espeak_tts(text)
        else:
            # Default to espeak (usually available on Pi)
            return self._espeak_tts(text)
    
    def _piper_tts(self, text: str) -> bytes:
        """Use Piper TTS (fast, local)"""
        try:
            import piper
            from piper import PiperVoice
            
            model_path = config.PiConfig.PIPER_MODEL_PATH
            voice = PiperVoice.load(model_path)
            
            # Generate audio
            audio_stream = voice.synthesize_stream(text)
            audio_data = b''.join(audio_stream)
            return audio_data
        except ImportError:
            print("Piper not available, falling back to espeak")
            return self._espeak_tts(text)
        except Exception as e:
            print(f"Piper TTS error: {e}")
            return self._espeak_tts(text)
    
    def _pyttsx3_tts(self, text: str) -> bytes:
        """Use pyttsx3 (system TTS)"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            
            # Save to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
            
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            # Read audio data
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            os.unlink(temp_path)
            return audio_data
        except Exception as e:
            print(f"pyttsx3 error: {e}")
            return self._espeak_tts(text)
    
    def _espeak_tts(self, text: str) -> bytes:
        """Use espeak (built-in on most Pi systems)"""
        try:
            # Generate WAV using espeak
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
            
            # espeak command
            cmd = [
                'espeak',
                '-s', str(self.rate),
                '-w', temp_path,
                text
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Read audio data
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            os.unlink(temp_path)
            return audio_data
        except Exception as e:
            print(f"espeak error: {e}")
            print("Install: sudo apt-get install espeak espeak-data")
            return b''
    
    def stop(self):
        """Stop current speech (for interruption)"""
        # Kill any running TTS processes
        try:
            subprocess.run(['pkill', '-f', 'espeak'], capture_output=True)
        except:
            pass


class StreamingTTS:
    """Streaming TTS for real-time response"""
    
    def __init__(self, tts_engine: PiTTS):
        self.tts = tts_engine
        self.is_speaking = False
    
    def speak_streaming(self, text: str, callback: Optional[Callable] = None):
        """Speak with streaming (word-by-word for interruption)"""
        # Simplified: In production, implement word-level streaming
        audio = self.tts.speak(text)
        if callback:
            callback(audio)
        return audio
