"""
Audio capture/playback.

Prefers PyAudio when it exists. On Windows Python 3.14 there is no PyAudio
wheel, so this falls back to sounddevice (PortAudio) which does install.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import webrtcvad

import config_pi as config

try:
    import pyaudio

    HAS_PYAUDIO = True
except ImportError:
    pyaudio = None  # type: ignore
    HAS_PYAUDIO = False

try:
    import sounddevice as sd

    HAS_SOUNDDEVICE = True
except ImportError:
    sd = None  # type: ignore
    HAS_SOUNDDEVICE = False


def _require_backend() -> str:
    if HAS_PYAUDIO:
        return "pyaudio"
    if HAS_SOUNDDEVICE:
        return "sounddevice"
    raise RuntimeError(
        "No audio backend. Install sounddevice (Python 3.14) or PyAudio (Python 3.12)."
    )


class PiAudioCapture:
    """Mic capture as 16-bit PCM chunks."""

    def __init__(self):
        self.sample_rate = config.PiConfig.SAMPLE_RATE
        self.chunk_size = config.PiConfig.CHUNK_SIZE
        self.vad = webrtcvad.Vad(config.PiConfig.VAD_AGGRESSIVENESS)
        self.backend = _require_backend()
        self.stream = None
        self._pa = None
        if self.backend == "pyaudio":
            self._pa = pyaudio.PyAudio()

    def start_stream(self, device_index: Optional[int] = None):
        device_index = device_index if device_index is not None else config.PiConfig.INPUT_DEVICE_INDEX
        if self.backend == "pyaudio":
            self.stream = self._pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                input_device_index=device_index,
            )
            return
        kwargs = {
            "samplerate": self.sample_rate,
            "channels": 1,
            "dtype": "int16",
            "blocksize": self.chunk_size,
        }
        if device_index is not None:
            kwargs["device"] = device_index
        self.stream = sd.RawInputStream(**kwargs)
        self.stream.start()

    def read_chunk(self) -> bytes:
        if not self.stream:
            raise RuntimeError("Stream not started")
        if self.backend == "pyaudio":
            return self.stream.read(self.chunk_size, exception_on_overflow=False)
        data, _overflowed = self.stream.read(self.chunk_size)
        return bytes(data)

    def is_speech(self, audio_data: bytes) -> bool:
        try:
            return self.vad.is_speech(audio_data, self.sample_rate)
        except Exception:
            return False

    def stop_stream(self):
        if not self.stream:
            return
        if self.backend == "pyaudio":
            self.stream.stop_stream()
            self.stream.close()
        else:
            self.stream.stop()
            self.stream.close()
        self.stream = None

    def cleanup(self):
        self.stop_stream()
        if self._pa is not None:
            self._pa.terminate()
            self._pa = None

    def list_devices(self):
        print("Available audio devices:")
        if self.backend == "pyaudio":
            for i in range(self._pa.get_device_count()):
                info = self._pa.get_device_info_by_index(i)
                if info["maxInputChannels"] > 0:
                    print(f"  {i}: {info['name']}")
            return
        devices = sd.query_devices()
        for i, info in enumerate(devices):
            if info.get("max_input_channels", 0) > 0:
                print(f"  {i}: {info['name']}")


class PiAudioOutput:
    """Playback of 16-bit PCM."""

    def __init__(self):
        self.sample_rate = 22050
        self.backend = _require_backend()
        self.stream = None
        self._pa = None
        self.is_speaking = False
        if self.backend == "pyaudio":
            self._pa = pyaudio.PyAudio()

    def start_stream(self, device_index: Optional[int] = None):
        device_index = device_index if device_index is not None else config.PiConfig.OUTPUT_DEVICE_INDEX
        if self.backend == "pyaudio":
            self.stream = self._pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                output=True,
                output_device_index=device_index,
            )
            return
        kwargs = {
            "samplerate": self.sample_rate,
            "channels": 1,
            "dtype": "int16",
        }
        if device_index is not None:
            kwargs["device"] = device_index
        self.stream = sd.RawOutputStream(**kwargs)
        self.stream.start()

    def play_audio(self, audio_data: bytes):
        if not audio_data:
            return
        self.is_speaking = True
        try:
            if self.backend == "pyaudio":
                if not self.stream:
                    self.start_stream()
                self.stream.write(audio_data)
            else:
                samples = np.frombuffer(audio_data, dtype=np.int16)
                sd.play(samples, self.sample_rate)
                sd.wait()
        finally:
            self.is_speaking = False

    def stop(self):
        if self.backend == "pyaudio":
            if self.stream and self.is_speaking:
                self.stream.stop_stream()
                self.stream.start_stream()
        elif HAS_SOUNDDEVICE:
            sd.stop()
        self.is_speaking = False

    def cleanup(self):
        self.stop()
        if self.stream is not None:
            if self.backend == "pyaudio":
                self.stream.stop_stream()
                self.stream.close()
            else:
                self.stream.stop()
                self.stream.close()
            self.stream = None
        if self._pa is not None:
            self._pa.terminate()
            self._pa = None
