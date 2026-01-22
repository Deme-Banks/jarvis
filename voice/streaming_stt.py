"""
Streaming Speech-to-Text for Real-time Transcription
"""
import queue
import threading
from typing import Optional, Callable
from voice.stt_pi import PiSTT
import config_pi as config


class StreamingSTT:
    """Streaming STT for real-time transcription"""
    
    def __init__(self, stt: Optional[PiSTT] = None):
        self.stt = stt or PiSTT()
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.is_streaming = False
        self.stream_thread = None
        self.callback: Optional[Callable] = None
    
    def start_streaming(self, callback: Optional[Callable[[str], None]] = None):
        """Start streaming transcription"""
        self.callback = callback
        self.is_streaming = True
        self.stream_thread = threading.Thread(target=self._stream_worker, daemon=True)
        self.stream_thread.start()
    
    def stop_streaming(self):
        """Stop streaming transcription"""
        self.is_streaming = False
        if self.stream_thread:
            self.stream_thread.join(timeout=1)
    
    def feed_audio(self, audio_data: bytes):
        """Feed audio data to streaming STT"""
        if self.is_streaming:
            self.audio_queue.put(audio_data)
    
    def _stream_worker(self):
        """Worker thread for streaming transcription"""
        buffer = b''
        
        while self.is_streaming:
            try:
                # Get audio chunk with timeout
                audio_chunk = self.audio_queue.get(timeout=0.1)
                buffer += audio_chunk
                
                # Process when buffer is large enough
                if len(buffer) >= config.PiConfig.CHUNK_SIZE * 2:
                    # Try to transcribe
                    text = self.stt.transcribe(buffer)
                    
                    if text and text.strip():
                        # Send to callback or queue
                        if self.callback:
                            self.callback(text)
                        else:
                            self.text_queue.put(text)
                        
                        # Clear buffer
                        buffer = b''
                
            except queue.Empty:
                # Process remaining buffer
                if buffer:
                    text = self.stt.transcribe(buffer)
                    if text and text.strip():
                        if self.callback:
                            self.callback(text)
                        else:
                            self.text_queue.put(text)
                    buffer = b''
                continue
            except Exception as e:
                print(f"Streaming STT error: {e}")
                break
    
    def get_text(self, timeout: float = 1.0) -> Optional[str]:
        """Get transcribed text from queue"""
        try:
            return self.text_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_all_text(self) -> list:
        """Get all pending transcribed text"""
        texts = []
        while not self.text_queue.empty():
            try:
                texts.append(self.text_queue.get_nowait())
            except queue.Empty:
                break
        return texts
