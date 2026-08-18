"""
JARVIS voice entry — mic, Vosk STT, Ollama, pyttsx3 TTS.

Optional Slack/plugins/analytics are not loaded here so Windows can actually start.
Text chat is still: python run_jarvis.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

import utils.optimized_imports  # noqa: F401
import config_pi as config
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM
from voice.audio_pi import PiAudioCapture, PiAudioOutput
from voice.stt_pi import PiSTT
from voice.tts_pi import PiTTS

WAKE = config.PiConfig.WAKE_WORD.lower()
# webrtcvad needs 10/20/30 ms frames. 320 samples @ 16 kHz = 20 ms.
MIN_UTTERANCE_BYTES = int(config.PiConfig.SAMPLE_RATE * 2 * 0.4)
SILENCE_FRAMES_END = 25  # ~0.5 s at 20 ms/frame
ENERGY_SPEECH = 400.0


def _is_loud(chunk: bytes) -> bool:
    if len(chunk) < 2:
        return False
    samples = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)
    rms = float(np.sqrt(np.mean(samples * samples)))
    return rms >= ENERGY_SPEECH


class JarvisPi:
    def __init__(self):
        self.audio_capture = PiAudioCapture()
        self.audio_output = PiAudioOutput()
        self.stt = PiSTT()
        self.tts = PiTTS()
        self._llm = LocalLLM()
        self._orchestrator = None
        self.context_memory = []
        self.awake = False
        self.is_speaking = False
        self.interrupted = False

    @property
    def llm(self):
        return self._llm

    @property
    def orchestrator(self):
        if self._orchestrator is None:
            self._orchestrator = PiOrchestrator(
                local_llm=self._llm,
                prefer_cloud=config.PiConfig.PREFER_CLOUD_LLM,
            )
        return self._orchestrator

    def start(self):
        print("JARVIS starting (voice, Ollama, no PyAudio required)...")
        try:
            print(self._llm.ensure_ready())
        except RuntimeError as exc:
            print(exc)
            return
        if not self.stt.recognizer:
            print("Vosk did not load. Check models/vosk-model-small-en-us-0.15")
            return

        self.audio_capture.start_stream()
        print(f"Ready. Say '{config.PiConfig.WAKE_WORD}' then your command.")
        print("Press Ctrl+C to exit")
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()

    def _main_loop(self):
        audio_buffer = b""
        silence_frames = 0
        while True:
            chunk = self.audio_capture.read_chunk()
            speech = self.audio_capture.is_speech(chunk) or _is_loud(chunk)
            if speech:
                audio_buffer += chunk
                silence_frames = 0
                continue
            silence_frames += 1
            if audio_buffer and silence_frames >= SILENCE_FRAMES_END:
                if len(audio_buffer) >= MIN_UTTERANCE_BYTES:
                    self._process_audio(audio_buffer)
                audio_buffer = b""
                silence_frames = 0

    def _process_audio(self, audio_data: bytes):
        text = self.stt.transcribe(audio_data) or ""
        text = text.strip()
        if len(text) < 2:
            return

        lowered = text.lower()
        print(f"You: {text}")

        if not self.awake:
            if WAKE not in lowered:
                return
            self.awake = True
            after = lowered.split(WAKE, 1)[-1].strip(" ,.-")
            if len(after) < 2:
                self._speak("Yes?")
                return
            text = after

        try:
            reply = self.orchestrator.process(
                text,
                context={"memory": self.context_memory[-5:]},
            )
        except Exception as exc:
            reply = f"Something went wrong: {exc}"

        self.context_memory.append({"user": text, "assistant": reply})
        if len(self.context_memory) > config.PiConfig.CONTEXT_MEMORY_SIZE:
            self.context_memory = self.context_memory[-config.PiConfig.CONTEXT_MEMORY_SIZE :]

        print(f"JARVIS: {reply}")
        self._speak(reply)
        self.awake = False

    def _speak(self, text: str):
        self.is_speaking = True
        try:
            self.tts.speak_aloud(text)
        finally:
            self.is_speaking = False

    def interrupt(self):
        self.interrupted = True
        self.audio_output.stop()
        self.tts.stop()

    def cleanup(self):
        self.audio_capture.cleanup()
        self.audio_output.cleanup()


def main():
    JarvisPi().start()


if __name__ == "__main__":
    main()
