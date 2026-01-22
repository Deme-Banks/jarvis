"""
Raspberry Pi Speech-to-Text (Offline)
"""
import json
from typing import Optional
import config_pi as config

try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("Warning: Vosk not available. Install: pip install vosk")


class PiSTT:
    """Offline Speech-to-Text using Vosk"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or config.PiConfig.VOSK_MODEL_PATH
        self.model = None
        self.recognizer = None
        
        if VOSK_AVAILABLE:
            self._load_model()
    
    def _load_model(self):
        """Load Vosk model"""
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(
                self.model,
                config.PiConfig.SAMPLE_RATE
            )
            self.recognizer.SetWords(True)
        except Exception as e:
            print(f"Error loading Vosk model: {e}")
            print(f"Download model from: https://alphacephei.com/vosk/models")
            raise
    
    def transcribe(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio to text"""
        if not self.recognizer:
            return None
        
        try:
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                return result.get("text", "").strip()
            else:
                # Partial result
                partial = json.loads(self.recognizer.PartialResult())
                return partial.get("partial", "").strip()
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def finalize(self) -> Optional[str]:
        """Get final transcription result"""
        if not self.recognizer:
            return None
        
        try:
            result = json.loads(self.recognizer.FinalResult())
            return result.get("text", "").strip()
        except:
            return None


class WakeWordDetector:
    """Wake word detection using PocketSphinx (offline)"""
    
    def __init__(self, wake_word: str = "jarvis"):
        self.wake_word = wake_word.lower()
        self.detector = None
        
        try:
            import pocketsphinx
            from pocketsphinx import LiveSpeech, get_model_path
            
            model_path = get_model_path()
            self.detector = LiveSpeech(
                verbose=False,
                sampling_rate=16000,
                buffer_size=2048,
                no_search=False,
                full_utt=False,
                hmm=model_path,
                lm=model_path,
                dic=model_path
            )
        except ImportError:
            print("Warning: PocketSphinx not available")
            print("Install: sudo apt-get install pocketsphinx pocketsphinx-en-us")
        except Exception as e:
            print(f"Wake word detector error: {e}")
    
    def detect(self, audio_data: bytes) -> bool:
        """Detect wake word in audio"""
        # Simplified: In production, use PocketSphinx properly
        # This is a placeholder
        return False
    
    def listen_for_wake_word(self) -> Generator[bool, None, None]:
        """Continuously listen for wake word"""
        if not self.detector:
            yield False
            return
        
        try:
            for phrase in self.detector:
                text = str(phrase).lower()
                if self.wake_word in text:
                    yield True
                else:
                    yield False
        except:
            yield False
