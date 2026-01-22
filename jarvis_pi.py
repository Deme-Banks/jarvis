"""
JARVIS Voice Assistant - Raspberry Pi Main Entry Point
"""
import time
import threading
from typing import Optional
from voice.audio_pi import PiAudioCapture, PiAudioOutput
from voice.stt_pi import PiSTT, WakeWordDetector
from voice.tts_pi import PiTTS
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM
import config_pi as config
from prompts.voice_jarvis import VOICE_JARVIS_PROMPT


class JarvisPi:
    """Main JARVIS system for Raspberry Pi"""
    
    def __init__(self):
        # Initialize components
        self.audio_capture = PiAudioCapture()
        self.audio_output = PiAudioOutput()
        self.stt = PiSTT()
        self.tts = PiTTS()
        self.wake_detector = WakeWordDetector(config.PiConfig.WAKE_WORD)
        
        # Initialize LLM
        self.llm = LocalLLM()
        if not self.llm.check_available():
            print("Warning: Local LLM not available")
            if config.PiConfig.FALLBACK_TO_CLOUD:
                print("Falling back to cloud...")
                # Would initialize cloud LLM here
            else:
                raise RuntimeError("No LLM available")
        
        self.orchestrator = PiOrchestrator(self.llm)
        
        # State
        self.is_listening = False
        self.is_speaking = False
        self.interrupted = False
        self.context_memory = []
    
    def start(self):
        """Start JARVIS system"""
        print("JARVIS starting...")
        
        # Validate config
        if not config.PiConfig.validate():
            print("Configuration validation failed")
            return
        
        # Start audio
        self.audio_capture.start_stream()
        self.audio_output.start_stream()
        
        print(f"JARVIS ready. Say '{config.PiConfig.WAKE_WORD}' to activate.")
        print("Press Ctrl+C to exit")
        
        # Main loop
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def _main_loop(self):
        """Main listening loop"""
        audio_buffer = b''
        silence_frames = 0
        max_silence = 10  # frames of silence before processing
        
        while True:
            # Read audio chunk
            chunk = self.audio_capture.read_chunk()
            
            # Check for wake word (simplified - use proper wake word detection)
            # In production, use dedicated wake word detection thread
            
            # Detect speech
            if self.audio_capture.is_speech(chunk):
                audio_buffer += chunk
                silence_frames = 0
            else:
                silence_frames += 1
                
                # If we have audio and silence detected, process
                if audio_buffer and silence_frames >= max_silence:
                    self._process_audio(audio_buffer)
                    audio_buffer = b''
                    silence_frames = 0
    
    def _process_audio(self, audio_data: bytes):
        """Process captured audio"""
        # Transcribe
        text = self.stt.transcribe(audio_data)
        if not text or len(text.strip()) < 2:
            return
        
        print(f"You: {text}")
        
        # Get response from orchestrator
        response = self.orchestrator.process(
            text,
            context={"memory": self.context_memory[-5:]}
        )
        
        # Update memory
        self.context_memory.append({"user": text, "assistant": response})
        if len(self.context_memory) > config.PiConfig.CONTEXT_MEMORY_SIZE:
            self.context_memory = self.context_memory[-config.PiConfig.CONTEXT_MEMORY_SIZE:]
        
        print(f"JARVIS: {response}")
        
        # Speak response
        self._speak(response)
    
    def _speak(self, text: str):
        """Speak text with interruption handling"""
        self.is_speaking = True
        self.interrupted = False
        
        # Generate audio
        audio_data = self.tts.speak(text)
        
        # Play audio (with interruption check)
        if not self.interrupted:
            self.audio_output.play_audio(audio_data)
        
        self.is_speaking = False
    
    def interrupt(self):
        """Interrupt current speech"""
        if self.is_speaking:
            self.interrupted = True
            self.audio_output.stop()
            self.tts.stop()
            print("Interrupted")
    
    def cleanup(self):
        """Cleanup resources"""
        self.audio_capture.cleanup()
        self.audio_output.cleanup()


def main():
    """Main entry point"""
    jarvis = JarvisPi()
    jarvis.start()


if __name__ == "__main__":
    main()
