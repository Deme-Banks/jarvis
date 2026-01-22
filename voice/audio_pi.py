"""
Raspberry Pi Optimized Audio Pipeline
"""
import pyaudio
import webrtcvad
import numpy as np
from typing import Optional, Callable, Generator
import config_pi as config


class PiAudioCapture:
    """Lightweight audio capture for Raspberry Pi"""
    
    def __init__(self):
        self.sample_rate = config.PiConfig.SAMPLE_RATE
        self.chunk_size = config.PiConfig.CHUNK_SIZE
        self.vad = webrtcvad.Vad(config.PiConfig.VAD_AGGRESSIVENESS)
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        
    def start_stream(self, device_index: Optional[int] = None):
        """Start audio stream"""
        device_index = device_index or config.PiConfig.INPUT_DEVICE_INDEX
        
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=device_index
        )
    
    def read_chunk(self) -> bytes:
        """Read audio chunk"""
        if not self.stream:
            raise RuntimeError("Stream not started")
        return self.stream.read(self.chunk_size, exception_on_overflow=False)
    
    def is_speech(self, audio_data: bytes) -> bool:
        """Detect if audio contains speech using VAD"""
        try:
            return self.vad.is_speech(audio_data, self.sample_rate)
        except:
            return False
    
    def stop_stream(self):
        """Stop audio stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_stream()
        self.audio.terminate()
    
    def list_devices(self):
        """List available audio devices"""
        print("Available audio devices:")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  {i}: {info['name']}")


class PiAudioOutput:
    """Lightweight audio output for Raspberry Pi"""
    
    def __init__(self):
        self.sample_rate = 22050  # Standard for TTS
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.is_speaking = False
    
    def start_stream(self, device_index: Optional[int] = None):
        """Start output stream"""
        device_index = device_index or config.PiConfig.OUTPUT_DEVICE_INDEX
        
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=True,
            output_device_index=device_index
        )
    
    def play_audio(self, audio_data: bytes):
        """Play audio data"""
        if not self.stream:
            self.start_stream()
        
        self.is_speaking = True
        self.stream.write(audio_data)
        self.is_speaking = False
    
    def stop(self):
        """Stop audio output immediately (for interruption)"""
        if self.stream and self.is_speaking:
            self.stream.stop_stream()
            self.stream.start_stream()
            self.is_speaking = False
    
    def cleanup(self):
        """Cleanup resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
