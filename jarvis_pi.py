"""
JARVIS Voice Assistant - Raspberry Pi Main Entry Point
"""
import time
import threading
from typing import Optional
from voice.audio_pi import PiAudioCapture, PiAudioOutput
from voice.stt_pi import PiSTT, WakeWordDetector
from voice.streaming_stt import StreamingSTT
from voice.tts_pi import PiTTS
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM
from llm.streaming_llm import StreamingLLM
from optimization.lazy_loader import get_lazy
from utils.error_handler import get_error_handler
from intelligence.proactive_suggestions import ProactiveSuggestions
from learning.memory import MemorySystem
from features.command_history import CommandHistory
from features.auto_complete import AutoComplete
from features.voice_shortcuts import VoiceShortcuts
import config_pi as config
from prompts.voice_jarvis import VOICE_JARVIS_PROMPT


class JarvisPi:
    """Main JARVIS system for Raspberry Pi"""
    
    def __init__(self):
        # Initialize components (lazy loading if enabled)
        if config.PiConfig.LAZY_LOADING:
            # Load only essential components immediately
            self.audio_capture = PiAudioCapture()
            self.audio_output = PiAudioOutput()
            self.stt = PiSTT()
            self.tts = PiTTS()
            self.wake_detector = WakeWordDetector(config.PiConfig.WAKE_WORD)
            
            # LLM and orchestrator loaded on first use
            self._llm = None
            self._orchestrator = None
        else:
            # Standard initialization
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
                else:
                    raise RuntimeError("No LLM available")
            
            self.orchestrator = PiOrchestrator(self.llm)
    
    @property
    def llm(self):
        """Lazy load LLM"""
        if self._llm is None:
            self._llm = LocalLLM()
            if not self._llm.check_available():
                if config.PiConfig.FALLBACK_TO_CLOUD:
                    print("Falling back to cloud...")
                else:
                    raise RuntimeError("No LLM available")
        return self._llm
    
    @property
    def orchestrator(self):
        """Lazy load orchestrator"""
        if self._orchestrator is None:
            self._orchestrator = PiOrchestrator(self.llm)
        return self._orchestrator
        
        # State
        self.is_listening = False
        self.is_speaking = False
        self.interrupted = False
        self.context_memory = []
        
        # Enhanced features
        self.streaming_stt = None
        self.streaming_llm = None
        self.error_handler = get_error_handler()
        self.memory = MemorySystem()
        self.proactive = ProactiveSuggestions(self.memory)
        self.command_history = CommandHistory()
        self.auto_complete = AutoComplete(self.command_history, self.memory)
        self.shortcuts = VoiceShortcuts()
        
        # Initialize streaming if enabled
        if config.PiConfig.ENABLE_RESPONSE_CACHE:  # Use as proxy for streaming
            self.streaming_stt = StreamingSTT(self.stt)
            self.streaming_llm = StreamingLLM(self.llm)
    
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
        max_silence = 5  # Reduced for faster response
        
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
        """Process captured audio with enhanced features"""
        try:
            # Transcribe (use streaming if available)
            if self.streaming_stt and self.streaming_stt.is_streaming:
                text = self.streaming_stt.get_text(timeout=0.5)
                if not text:
                    text = self.stt.transcribe(audio_data)
            else:
                text = self.stt.transcribe(audio_data)
            
            if not text or len(text.strip()) < 2:
                return
            
            # Expand shortcuts
            text = self.shortcuts.expand(text)
            
            print(f"You: {text}")
            
            # Check for history/favorites commands
            if text.lower().startswith("repeat"):
                # Repeat last command
                recent = self.command_history.get_recent(1)
                if recent:
                    text = recent[0]["command"]
                    print(f"Repeating: {text}")
            
            elif text.lower().startswith("favorite"):
                # Execute favorite
                favorites = self.command_history.get_favorites()
                if favorites:
                    # Use most recent favorite
                    text = favorites[-1]["command"]
                    print(f"Using favorite: {text}")
            
            # Get response from orchestrator (with error handling)
            try:
                response = self.orchestrator.process(
                    text,
                    context={"memory": self.context_memory[-5:]}
                )
                success = True
            except Exception as e:
                response = self.error_handler.handle_error(
                    e,
                    context={"user_input": text},
                    retry=True
                ) or "I encountered an error. Let me try again."
                success = False
            
            # Save to history
            self.command_history.add(text, response, success)
            
            # Add proactive suggestions if appropriate
            suggestions = self.proactive.suggest_next_action(text)
            if suggestions and len(response) < 100:
                response += f" [Suggestions: {', '.join(suggestions[:2])}]"
            
            # Update memory
            self.context_memory.append({"user": text, "assistant": response})
            if len(self.context_memory) > config.PiConfig.CONTEXT_MEMORY_SIZE:
                self.context_memory = self.context_memory[-config.PiConfig.CONTEXT_MEMORY_SIZE:]
            
            print(f"JARVIS: {response}")
            
            # Speak response (streaming if available)
            if self.streaming_llm and len(response) > 50:
                try:
                    self._speak_streaming(response)
                except:
                    # Fallback to normal speech
                    self._speak(response)
            else:
                self._speak(response)
                
        except Exception as e:
            self.error_handler.handle_error(e, context={"audio_data_length": len(audio_data)})
    
    def _speak_streaming(self, text: str):
        """Speak with streaming TTS"""
        def on_chunk(chunk: str):
            # Speak chunk immediately if not interrupted
            if not self.interrupted:
                try:
                    audio = self.tts.speak(chunk)
                    if not self.interrupted:
                        self.audio_output.play_audio(audio)
                except:
                    pass
        
        # Stream response and speak chunks
        try:
            full_response = self.streaming_llm.stream_with_callback(
                text,
                on_chunk
            )
        except:
            # Fallback to normal speech
            self._speak(text)
    
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
